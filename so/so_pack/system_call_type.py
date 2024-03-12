from enum import Enum


class SystemCallType(Enum):
    CREATE_PROCESS = 1
    WRITE_PROCESS = 2
    READ_PROCESS = 3
    DELETE_PROCESS = 4
