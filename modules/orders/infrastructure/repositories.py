from uuid import UUID
from modules.orders.domain.entities import OrderV2
from .dtos import OrderDTO


class OrdersRepositorySQLAlchemy:

    def __init__(self, db) -> None:
        self.db = db

    def get_by_id(self, id: UUID) -> OrderV2:
        order_dto = self.db.query(OrderDTO).filter_by(order_id=str(id)).one()
        return OrderV2(**order_dto.to_dict())

    def create(self, order: OrderV2):
        order_dto = OrderDTO(**order.to_dict())
        self.db.add(order_dto)
        self.db.commit()
        self.db.refresh(order_dto)
        return order_dto

    def update(self, order: OrderV2):
        order_dto = self.db.query(OrderDTO).filter_by(order_id=str(order.order_id)).one()
        order_dto = order_dto.update(order)
        self.db.commit()
        return order_dto

    def delete(self, id: UUID):
        order_dto = self.db.query(OrderDTO).filter_by(order_id=str(id)).one()
        order_dto.delete()
        self.db.commit()
        return order_dto
