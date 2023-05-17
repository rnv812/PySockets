from dataclasses import dataclass
from enum import Enum


class Actions(Enum):
    GET_BALANCE = 0
    WITHDRAW = 1
    DEPOSIT = 2


@dataclass
class Request:
    action: int
    username: str
    password: str
