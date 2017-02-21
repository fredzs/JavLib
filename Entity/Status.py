from enum import Enum


class Status(Enum):
    ERROR = 0
    SUCCESS = 1
    DUPLICATE = 2
    SAVE_FAILED = 3
    REQUEST_FAILED = 4
    CODE_NOT_EXIST = 5
    PARSE_ERROR = 6
