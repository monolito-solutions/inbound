from modules.orders.infrastructure.factory import factory_get_order
from sqlalchemy.exc import IntegrityError
from errors.exceptions import InboundException
from modules.orders.application.events.events import EventOrderCreated, OrderCreatedPayload
from modules.orders.application.commands.commands import CommandCheckInventoryOrder, CheckInventoryPayload
from modules.orders.infrastructure.repositories import OrdersRepositorySQLAlchemy
from infrastructure.dispatchers import Dispatcher
from config.db import get_db
import utils
import json
import traceback
import uuid
def create_order(order):
    order.order_id = str(uuid.uuid4())
    db = get_db()
    order = factory_get_order(order)
    try:
        repository = OrdersRepositorySQLAlchemy(db)
        repository.create(order)
    except IntegrityError:
        dispatcher = Dispatcher()
        event_payload = OrderCreatedPayload(
            order_id = str(order.order_id),
            customer_id = str(order.customer_id),
            order_date = str(order.order_date),
            order_status = "Failed To Create: Duplicate order entry",
            order_items = json.dumps(order.order_items) if type(order.order_items != str) else order.order_items,
            order_total = float(order.order_total),
            order_version = int(order.order_version)
        )

        event = EventOrderCreated(
            time = utils.time_millis(),
            ingestion = utils.time_millis(),
            datacontenttype = OrderCreatedPayload.__name__,
            data_payload = event_payload,
            type = ""
        )
        dispatcher.publish_message(event, "order-events")
        return
    except Exception as e:
        raise InboundException(f"Error creating order: {e}", 500)
    finally:
        db.close()

    event_payload = OrderCreatedPayload(
        order_id = str(order.order_id),
        customer_id = str(order.customer_id),
        order_date = str(order.order_date),
        order_status = str(order.order_status),
        order_items = json.dumps(order.order_items) if type(order.order_items != str) else order.order_items,
        order_total = float(order.order_total),
        order_version = int(order.order_version)
    )

    event = EventOrderCreated(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = OrderCreatedPayload.__name__,
        data_payload = event_payload
    )

    command_payload = CheckInventoryPayload(**event_payload.to_dict())
    command_payload.order_status = "Ready to check inventory"

    command = CommandCheckInventoryOrder(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = CheckInventoryPayload.__name__,
        data_payload = command_payload
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "order-events")
    dispatcher.publish_message(command, "order-commands")

def cancel_order(order):
    db = get_db()
    order_obj = factory_get_order(order)
    order_obj.order_status = "Canceled"
    try:
        repository = OrdersRepositorySQLAlchemy(db)
        res = repository.update(order_obj)
    except Exception as e:
        traceback.print_exc(e)
    finally:
        db.close()