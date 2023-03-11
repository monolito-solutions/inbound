from sqlalchemy import String, Column, Float, Integer, Text
from config.db import Base

class OrderDTO(Base):
    __tablename__ = "orders"

    order_id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(36), index=True)
    order_date = Column(String(100), index=True)
    order_status = Column(String(100), index=True)
    order_items = Column(Text(1000000), index=True)
    order_total = Column(Float, index=True)
    order_version = Column(Integer, index=True)

    def to_dict(self):
        return {
            "order_id" : self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "order_status": self.order_status,
            "order_items": self.order_items,
            "order_total": self.order_total,
            "order_version": self.order_version
        }

    def update(self, order):
        self.order_id = order.order_id
        self.customer_id = order.customer_id
        self.order_date = order.order_date
        self.order_status = order.order_status
        self.order_items = order.order_items
        self.order_total = order.order_total
        self.order_version = order.order_version