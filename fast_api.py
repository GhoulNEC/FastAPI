import uvicorn
from fastapi import Depends, FastAPI

from typing import List

from models import Desk, Service

app = FastAPI()

MAX_QUEUE_LENGTH = 100


def get_database():
    from fast_api_db import Database
    return Database()


def get_desk_place(database, service_id, ticket):
    queue_size = [0, MAX_QUEUE_LENGTH]
    for desk_id in database.get_service_desks(service_id):
        db_queue_size = len(database.get_desk(desk_id).queue)
        if database.get_desk(desk_id).is_open:
            if database.get_desk(desk_id).in_service is None:
                database.get_desk(desk_id).in_service = ticket
                queue_size = [0, MAX_QUEUE_LENGTH]
                break
            elif db_queue_size < queue_size[1]:
                queue_size[0], queue_size[1] = desk_id, db_queue_size
    if queue_size[0] > 0:
        database.get_desk(queue_size[0]).queue.append(ticket)


@app.get("/")
async def root():
    """
    Не понятно для чего этот метод
    Если делаешь заглушку, то тогда можешь выводить какую-то статистику по кол-ву услуг, касс, талончиков
    чтобы метод нес какую-то пользу
    """
    return {"message": "Выберите услугу"}


@app.get("/services/")
async def get_services(database=Depends(get_database)):
    return database.services


@app.get("/services/{service_id}/")
async def get_service_info(service_id: int, database=Depends(get_database)):
    return {"service_id": service_id,
            "service": database.get_service(service_id)}


@app.post("/services/{service_id}/confirm/")
async def get_in_queue(service_id: int, database=Depends(get_database)):
    """
    Название метода совсем не дает понять что он делает.
    Если мы выдаем талон на услугу то надо так и написать
    /tickets/new/ а в тело передовать информацию об услуге (и возможно что-то еще)

    не понятно почему талончик только один и как он помещается в очередь
    """
    try:
        ticket = database.ticket
        service = database.get_service(service_id)
        if ticket.queue_place == MAX_QUEUE_LENGTH:
            ticket.queue_place = 0
        ticket.queue_place += 1
        ticket.service = service
        get_desk_place(database, service_id, ticket.queue_place)
    except ValueError:
        return {"message": "Все кассы закрыты"}
    return {"place": ticket.queue_place, "service": ticket.service}

#точка входа не по REST
@app.get("/desk_info/")
async def get_desk_info(database=Depends(get_database)):
    """
    Мне тут не хватает информации о том кто стоит в очередь в эту кассу
    """
    return database.get_desk_info()

#точка входа не по REST
@app.post("/{desk_id}/done/")
async def go_to_next_ticket(desk_id: int, database=Depends(get_database)):
    queue = database.get_desk(desk_id).queue
    if len(queue) > 0:
        database.get_desk(desk_id).in_service = queue[0]
        database.get_desk(desk_id).queue.pop(0)
    else:
        database.get_desk(desk_id).in_service = None
    return {"ticket": database.get_desk(desk_id).in_service}

#точка входа не по REST
@app.post("/{desk_id}/close/}")
async def close_desk(desk_id: int, database=Depends(get_database)):
    try:
        database.get_desk(desk_id).is_open = False
        queue = database.get_desk(desk_id).queue
        services = database.get_desk(desk_id).services
        for place in queue:
            get_desk_place(database, services[0], place)
        queue.clear()
    except ValueError:
        return {"message": "Все кассы закрыты"}
    # тут в сообщении можно добавить какая конкретно касса закрыта 
    return {"message": "Касса закрыта"}

#точка входа не по REST
@app.post("/{desk_id}/open/")
async def open_desk(desk_id: int, database=Depends(get_database)):
    database.get_desk(desk_id).is_open = True
    return {"message": "Касса открыта"}

#точка входа не по REST
@app.post("/new_service/")
async def add_new_service(service: Service, desk_keys: List[int],
                          database=Depends(get_database)):
    service_key = database.get_new_service_key()
    database.services[service_key] = service
    for desk_key in desk_keys:
        database.desks[desk_key].services.append(service_key)
    # тут надо вернуть сам созданный объект, можно и с сообщением об успехе 
    return {"message": "Сервис успешно добавлен"}


#точка входа не по REST
@app.post("/new_desk/")
async def add_new_desk(desk: Desk, database=Depends(get_database)):
    desk_key = database.get_new_desk_key()
    database.desks[desk_key] = desk
    # тут надо вернуть сам созданный объект, можно и с сообщением об успехе
    return {"message": "Касса успешно добавлена"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
