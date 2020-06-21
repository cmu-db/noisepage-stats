from functools import partial
from typing import Any, Dict
from datetime import datetime
from time import mktime
from decimal import Decimal

from factory import Factory
from factory.base import StubObject


def generate_dict_factory(factory: Factory):
    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
            if isinstance(value, Decimal):
                stub_dict[key] = float(value)
            if isinstance(value, datetime):
                stub_dict[key] = int(
                    mktime(value.timetuple())*1e3 +
                    value.microsecond/1e3
                )
            if isinstance(value, list):
                converted_list = []
                for item in value:
                    converted_item = convert_dict_from_stub(item)
                    converted_list.append(converted_item)
                stub_dict[key] = converted_list
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)