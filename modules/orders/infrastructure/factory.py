from modules.orders.domain.entities import OrderV1, OrderV2
from errors.exceptions import InboundException
import json

def factory_get_order(order):
    """Detects the version of the order and returns the corresponding object."""
    try:
        return OrderV2(**order.to_dict())
    except TypeError:
        try:
            return OrderV1(**order.to_dict()).upscale()
        except TypeError:
            raise InboundException("Order version not supported")
    except KeyError:
        raise InboundException("Order version not supported")