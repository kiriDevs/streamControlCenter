class ChannelNotFoundException(Exception):
    pass


class IllegalChannelNameException(Exception):
    pass


class InvalidTitleException(Exception):
    pass


class TitleTooLongException(InvalidTitleException):
    pass
