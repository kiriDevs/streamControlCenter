import re

import apiHandler

from Exceptions import ChannelNotFoundException
from Exceptions import IllegalChannelNameException
from Exceptions import StreamNotFoundException


def changeEntryText(forEntryField, toValue):
    contentLength = len(forEntryField.get())
    forEntryField.delete(0, contentLength)  # Deleting current content
    forEntryField.insert(0, toValue)  # Writing new string


def isAllowedUserName(string):
    if not re.match("[a-zA-Z0-9_]", string):
        return False

    if not len(string) in range(4, 26):  # Usernames can range from 4 to 25 chars, range(x, y) doesn't include y
        return False

    if string[0] == '_':
        return False

    return True


def searchChannel(query):
    if not isAllowedUserName(query):
        raise IllegalChannelNameException(f"{query} is not a channel name!")

    result = apiHandler.searchChannel(query)

    if result is None:
        raise ChannelNotFoundException(f"Channel {query} wasn't found!")

    try:
        viewers = apiHandler.getStream(channel_name=query)["viewer_count"]
    except StreamNotFoundException:
        viewers = None

    result["viewers"] = viewers

    return result
