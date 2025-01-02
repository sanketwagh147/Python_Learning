from enum import Enum


class ExceptionMsgEnum(str, Enum):
    EMPTY_STACK = "The Stack is empty"
    NODE_INVALID_STATE = "The Node is in invalid state"
