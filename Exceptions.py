class ChannelNotFoundException(Exception):
    pass


class StreamNotFoundException(Exception):
    pass
    

class IllegalChannelNameException(Exception):
    pass


class InvalidTitleException(Exception):
    pass


class TitleTooLongException(InvalidTitleException):
    pass


class InternalTwitchError(Exception):
    pass


class ConnectionFailedError(Exception):
    pass


class UnknownError(Exception):
    pass


class AuthorizationError(Exception):
    pass
