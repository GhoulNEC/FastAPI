from typing import List, Union
# Хорошо что используешь pydantic 
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

"""
Я не поняла назначение этого класса
Предполагается что мы заказываем талон на услугу, 
генерируем его номер (в зависимости от услуги) и талон помещаем в очередь конкретной кассы 

Помещать в очередь можно доверить какому-нибудь классу-менеджеру
"""
class Ticket(BaseModel):
    queue_place: int
    service: Union[str, None] = None


class Service(BaseModel):
    name: str
