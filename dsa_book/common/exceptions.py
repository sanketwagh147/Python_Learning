from dsa_book.common.msg_enums import ExceptionMsgEnum


class StackException(Exception): ...


class EmptyStackException(StackException):
    _EMPTY_STACK_MSG = ExceptionMsgEnum.EMPTY_STACK

    def __init__(self, msg: str = _EMPTY_STACK_MSG, *args) -> None:
        super().__init__(msg, *args)
