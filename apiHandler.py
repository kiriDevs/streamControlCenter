import requests

from configHandler import getAuth


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

    request = requests.get(twitchAPI("/helix/users/follows"), headers=headers, params=parameters)
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

    request = requests.get(twitchAPI("/helix/search/channels"), headers=headers, params=parameters)
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
    request = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)
    response = request.json()

    try:
        myName = response["login"]
        myID = response["user_id"]
    except KeyError:
        error = request.json()["error"]
        status = request.json()["status"]
        message = request.json()["message"]
        print(f"Error while searching for channels: {status}: {error} - {message}")
        return

    returnStruct = {
        "name": myName,
        "id": myID
    }
    return returnStruct
