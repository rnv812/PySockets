from dataclasses import dataclass
from enum import Enum


class Messages(Enum):
    REGISTERED = "User successfully created"
    USER_ALREADY_EXISTS = "Username already taken"
    INVALID_CREDENTIALS = "Invalid username or password"
    BALANCE_UPDATED = "Balance updated"
    BALANCE_TOO_LOW = "Balance is too low"
    PERFORMED = "Performed"


@dataclass
class Response:
    status: bool
    message: str
    content: str
