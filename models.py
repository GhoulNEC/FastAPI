from typing import List, Union
from pydantic import BaseModel


class Desk(BaseModel):
    services: List[int]
    queue: List[int]
    in_service: Union[int, None] = None
    is_open: bool = True

    class Config:
        schema_extra = {
            "example": {
                "services": [
                    1
                ],
                "queue": [],
                "in_service": None,
                "is_open": True
            }
        }


class Ticket(BaseModel):
    queue_place: int
    service: Union[str, None] = None


class Service(BaseModel):
    name: str
