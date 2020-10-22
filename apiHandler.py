import requests

from configHandler import getAuth

from Exceptions import TitleTooLongException
from Exceptions import ConnectionFailedError
from Exceptions import InternalTwitchError
from Exceptions import AuthorizationError
from Exceptions import UnknownError
from Exceptions import StreamNotFoundException

from requests.exceptions import ConnectionError

from json.decoder import JSONDecodeError


def twitchAPI(string):
    if string.startswith("/"):
        return f"https://api.twitch.tv{string}"
    else:
        return f"https://api.twitch.tv/{string}"


def getStream(channel_id=None, channel_name=None):
    # Param checking
    if channel_id is None and channel_name is None:
        raise ValueError("You need to pass either a channel_id or a channel_name")
    if channel_id is not None and channel_name is not None:
        raise ValueError("You can only pass either a channel_id or a channel_name")

    # Prepare the request
    url = twitchAPI("/helix/streams")

    clid = getAuth()["clientid"]
    oauth = getAuth()["oauth"]
    headers = {
        "client-id": clid,
        "Authorization": f"Bearer {oauth}"
    }

    if channel_id is not None:
        params = { "user_id": channel_id }
    if channel_name is not None:
        params = { "user_login": channel_name }

    response = requests.get(url, headers=headers, params=params)

    try:
        json = response.json()
        results = json["data"]
    except JSONDecodeError:  # No JSON was returned
        raise InternalTwitchError("Didn't get JSON response for request!")
    except KeyError:  # field "data" doesn't exists
        try:
            # Check status code to see why the request failed
            status = json["status"]

            if status == 200:  # 200 - OK
                raise UnknownError("Got 200 but bad response")
            elif status == 401:  # 401 - Unauthorized
                raise AuthorizationError("Got 401 from Twitch")
            elif status == 500:  # 500 - Internal Error
                raise InternalTwitchError("Got 500 from Twitch")
            elif status == 502:  # 502 - Bad Gateway
                raise ConnectionFailedError("Got 502 after API call")

            # None of the default errors apply
            error = json["error"]
            message = json["message"]
            msg = f"Error while checking viewer number: {status}: {error} - {message}"
            raise UnknownError(msg)
        except KeyError:  # Typical error fields don't exist aswell
            code = response.status_code
            raise UnknownError(f"Got {code}, wanted stream info as JSON")

    stream = None  # The result we were searching for, default to None
    for result in results:
        if result["user_id"] == channel_id or result["user_name"] == channel_name:
            stream = result
            break

    if stream is not None:
        return stream
    else:
        raise StreamNotFoundException("That channel is not live right now!")


def getFollowerNumber(channelID):
    oauthToken = getAuth()["oauth"]
    authString = f"Bearer {oauthToken}"

    parameters = {"to_id": channelID}
    headers = {
        "client-id": getAuth()["clientid"],
        "Authorization": authString
    }

    try:
        request = requests.get(twitchAPI("/helix/users/follows"), headers=headers, params=parameters)
    except ConnectionError:
        raise ConnectionFailedError("Couldn't connect to TwitchAPI!")

    try:
        result = request.json()["total"]
        return result
    except KeyError:
        error = request.json()["error"]
        status = request.json()["status"]
        message = request.json()["message"]
        print(f"Error while checking follower number: {status}: {error} - {message}")
        return


def searchChannel(searchQuery):
    searchQuery = searchQuery.lower()

    oauthToken = getAuth()["oauth"]
    authString = f"Bearer {oauthToken}"

    parameters = {"query": searchQuery}
    headers = {
        "client-id": getAuth()["clientid"],
        "Authorization": authString
    }

    try:
        request = requests.get(twitchAPI("/helix/search/channels"), headers=headers, params=parameters)
    except ConnectionError:
        raise ConnectionFailedError("Couldn't connect to TwitchAPI!")

    try:
        results = request.json()["data"]
    except KeyError:
        error = request.json()["error"]
        status = request.json()["status"]
        message = request.json()["message"]
        print(f"Error while searching for channels: {status}: {error} - {message}")
        return

    for result in results:
        if result["display_name"].lower() == searchQuery:  # Matching while ignoring capitalization
            channelID = result["id"]
            follower_number = getFollowerNumber(channelID)

            returnStruct = {
                "display_name": result["display_name"],
                "is_live": result["is_live"],
                "title": result["title"],
                "follower_number": follower_number
            }

            return returnStruct
        print(f"No channel with the specific name {searchQuery} was found!")
        return


def getSelf():
    oauthToken = getAuth()["oauth"]
    authString = f"Bearer {oauthToken}"

    headers = {"Authorization": authString}

    try:
        request = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)
    except ConnectionError:
        raise ConnectionFailedError("Couldn't connect to TwitchAPI!")

    response = request.json()

    try:
        clientID = response["client_id"]
        myName = response["login"]
        scopes = response["scopes"]
        myID = response["user_id"]
        oAuthExpiresIn = response["expires_in"]
    except KeyError:
        status = request.json()["status"]
        message = request.json()["message"]
        print(f"Error while searching for channels: {status}: {error} - {message}")
        return

    returnStruct = {
        "clientid": clientID,
        "username": myName,
        "scopes": scopes,
        "userid": myID,
        "auth_expiry": oAuthExpiresIn
    }
    return returnStruct


def setTitle(new_title):
    if len(new_title) > 140:  # 140 is the max length for Twitch titles
        raise TitleTooLongException("Stream titles can only have up to 140 characters!")

    myID = getSelf()["userid"]

    oauthToken = getAuth()["oauth"]
    authString = f"Bearer {oauthToken}"

    headers = {
        "client-id": getAuth()["clientid"],
        "Authorization": authString
    }
    parameters = {
        "broadcaster_id": myID,
        "title": new_title
    }

    try:
        request = requests.patch(twitchAPI("/helix/channels"), headers=headers, params=parameters)
    except ConnectionError:
        raise ConnectionFailedError("Couldn't connect to TwitchAPI!")

    if request.status_code != 204:  # 204 is returned when the change worked
        raise Exception("An Unknown Error occured while trying to change the title of the stream!")
