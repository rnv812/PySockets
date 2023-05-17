from dataclasses import dataclass


@dataclass
class Request:
    status: bool
    message: str
    content: str
