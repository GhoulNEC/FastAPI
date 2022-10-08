from models import Desk, Service, Ticket


class Database:
    services = {
        1: Service(name="Кредит/Ипотека"),
        2: Service(name="Выдача карт"),
        3: Service(name="Внесение/Снятие наличных"),
        4: Service(name="Переводы"),
        5: Service(name="Оплата счетов"),
        6: Service(name="Справки"),
    }
    desks = {
        1: Desk(
            services=[1, 2],
            queue=[],
        ),
        2: Desk(
            services=[1, 2],
            queue=[],
        ),
        3: Desk(
            services=[3, 4, 5],
            queue=[],
        ),
        4: Desk(
            services=[3, 4, 5],
            queue=[],
        ),
        5: Desk(
            services=[6],
            queue=[],
        )
    }
    ticket = Ticket(
        queue_place=0,
    )

    def get_service(self, service_id):
        return self.services[service_id]

    def get_service_desks(self, service_id):
        if desks := [key for key, desk in self.desks.items()
                     if service_id in desk.services and desk.is_open]:
            return desks
        self.ticket.queue_place -= 1
        raise ValueError("Empty list")

    def get_desk(self, desk_id):
        return self.desks[desk_id]

    def get_desk_info(self):
        return {key: {"in service": desk.in_service, "queue": desk.queue}
                for key, desk in self.desks.items()}

    def get_new_service_key(self):
        return max(list(self.services.keys())) + 1

    def get_new_desk_key(self):
        return max(list(self.desks.keys())) + 1

    def get_sum_queue_tickets(self):
        return sum(
            len(desk.queue) + 1 if desk.in_service is not None
            else len(desk.queue) for desk in self.desks.values()
        )

    def get_opened_desks_amount(self):
        return sum(desk.is_open for desk in self.desks.values())
