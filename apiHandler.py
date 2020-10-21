import requests

from configHandler import getAuth

from Exceptions import TitleTooLongException
from Exceptions import ConnectionFailedError

from requests.exceptions import ConnectionError


def twitchAPI(string):
    if string.startswith("/"):
        return f"https://api.twitch.tv{string}"
    else:
        return f"https://api.twitch.tv/{string}"


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
