from pulsar.schema import *
from utils import time_millis
import uuid


class CheckInventoryPayload(Record):
    order_id = String()
    customer_id = String()
    order_date = String()
    order_status = String()
    order_items = String()
    order_total = Float()
    order_version = Long()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id":self.customer_id,
            "order_date": self.order_date,
            "order_status": self.order_status,
            "order_items": self.order_items,
            "order_total": self.order_total,
            "order_version": self.order_version
        }


class CommandCheckInventoryOrder(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v2")
    type = String(default="CommandCheckInventory")
    datacontenttype = String()
    service_name = String(default="inbound.entregasalpes")
    data_payload = CheckInventoryPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
