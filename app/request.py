from dataclasses import dataclass
from enum import Enum


class Actions(Enum):
    REGISTER = 0
    GET_BALANCE = 1
    WITHDRAW = 2
    DEPOSIT = 3


@dataclass
class Request:
    action: int
    username: str
    password: str
    content: str
