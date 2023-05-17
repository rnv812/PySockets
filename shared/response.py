from dataclasses import dataclass


@dataclass
class Response:
    status: bool
    message: str
    content: str
