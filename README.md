# FastAPI
***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Описание</summary>

Реализована система выдачи талончиков Сбербанка через FastApi. 
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Технологии</summary>

* Python 3.9.6
* fastapi
* uvicorn

С полным списком технологий можно ознакомиться в файле requirements.txt
</details>

***
<details>
     <summary style="font-size: 16pt; font-weight: bold">Документация</summary>

С документацией проекта можно ознакомиться по [ссылке](http://127.0.0.1:8000/redoc/) после запуска проекта.
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Запуск проекта</summary>

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/GhoulNEC/FastAPI.git
```

```
cd FastAPI
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Запустить сервер
```
uvicorn fast_api:app
```

</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Пример получения API</summary>

#### Управление API

`GET /` - Приветственный экран. 

`GET /services/` - Получение списка услуг.

`GET /services/{service_id}/` - Получение информации о сервисе по id

`GET /desk_info/` - Получение информации о кассах: какой талон сейчас обслуживается и какие талоны в очереди на эту кассу.

`POST /services/{service_id}/confirm/` - Получение талончика в очередь с распределением по кассам в зависимости от их загруженности и возможности предоставления услуги.

`POST /{desk_id}/done/` - Опция для кассира. Услуга оказана, переход к следующему талону.

`POST /{desk_id}/close/` - Закрытие кассы с распределением талонов в очереди между свободными кассами работающими с такими же услугами.

`POST /{desk_id}/open/` - Открыть кассу.

`POST /new_service/` - Добавление нового сервиса.

Нужно указать название нового сервиса и номера касс, которые будет обслуживать новый сервис.

```json
{
  "service": {
    "name": "string"
  },
  "desk_keys": [
    "string"
  ]
}
```

`POST /new_desk/` - Добавление новой кассы. Нужно заполнить id сервисов, которые касса будет обслуживать.

```json
{
  "services": [
    "string"
  ],
  "queue": [
    "string"
  ],
  "in_service": 0,
  "is_open": true
}
```

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Автор</summary>

* [Роман Евстафьев](https://github.com/GhoulNEC)
</details>

***