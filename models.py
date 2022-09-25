from typing import Union

from pydantic import BaseModel


class Desk(BaseModel):
    services: list
    queue: list = None
    in_service: Union[int, None] = None
    is_open: bool = True


class Ticket(BaseModel):
    queue_place: int
    service: Union[str, None] = None


class Service(BaseModel):
    name: str
