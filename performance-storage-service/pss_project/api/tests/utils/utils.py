from functools import partial
from typing import Any, Dict
from datetime import datetime
from time import mktime
from decimal import Decimal

from factory import Factory
from factory.base import StubObject


def generate_dict_factory(factory: Factory):
    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__ if not isinstance(stub,dict) else stub
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
            elif isinstance(value, Decimal):
                stub_dict[key] = float(value)
            elif isinstance(value, datetime):
                stub_dict[key] = int(
                    mktime(value.timetuple())*1e3 +
                    value.microsecond/1e3
                )
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)