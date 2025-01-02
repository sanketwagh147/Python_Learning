from dsa_book.common.msg_enums import ExceptionMsgEnum


class StackException(Exception): ...


class QueueException(Exception): ...


class CommonExceptions(Exception): ...


class EmptyException(Exception): ...


class EmptyStackException(StackException):
    _EMPTY_STACK_MSG = ExceptionMsgEnum.EMPTY_STACK

    def __init__(self, msg: str = ExceptionMsgEnum.EMPTY_STACK, *args) -> None:
        super().__init__(msg, *args)


class InvalidNodeException(StackException):

    def __init__(self, msg: str = ExceptionMsgEnum.NODE_INVALID_STATE, *args) -> None:
        super().__init__(msg, *args)
