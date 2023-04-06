from functools import partial
from inspect import Signature, Parameter
from src.vidimera import Behaviour


def test_createing_a_behaviour():
    assert Behaviour(SimpleObject)
    behaviour = Behaviour(SimpleObject)
    assert repr(behaviour) == "<Behaviour of <class 'tests.behaviour_test.SimpleObject'>>"
    expected_signatures = set(
        [
            ("__class__", Behaviour.NO_SIGNATURE),
            ("__delattr__", _method("name")),
            ("__dir__", _method()),
            ("__eq__", _method("other", kind=Parameter.POSITIONAL_OR_KEYWORD)),
            ("__format__", _method("format_spec")),
            ("__ge__", _method("value")),
            ("__getattribute__", _method("name")),
            ("__gt__", _method("value")),
            ("__init__", _method("value", kind=Parameter.POSITIONAL_OR_KEYWORD)),
            ("__init_subclass__", Behaviour.NO_SIGNATURE),
            ("__le__", _method("value")),
            ("__lt__", _method("value")),
            ("__ne__", _method("value")),
            ("__new__", _signature("*args", "**kwargs")),
            ("__reduce__", _method()),
            ("__reduce_ex__", _method("protocol")),
            ("__repr__", _method()),
            ("__setattr__", _method("name", "value")),
            ("__sizeof__", _method()),
            ("__str__", _method()),
            ("__subclasshook__", Behaviour.NO_SIGNATURE),
            (
                "public_method",
                _method("*args", "**kwargs", kind=Parameter.POSITIONAL_OR_KEYWORD),
            ),
        ]
    )
    assert behaviour.signatures() == expected_signatures


class SimpleObject:
    def __init__(self, value):
        self.value = value

    def public_method(self, *args, **kwargs):
        pass

    def _private_method(self):
        pass

    def __eq__(self, other):
        return self.value == other


def _method(*params, kind=Parameter.POSITIONAL_ONLY):
    return _signature("self", *params, kind=kind)


def _signature(*params, kind=Parameter.POSITIONAL_ONLY):
    to_param = partial(_param, kind)
    return Signature(parameters=map(to_param, params))


def _param(kind, name):
    if name.startswith("**"):
        return Parameter(name[2:], Parameter.VAR_KEYWORD)
    if name.startswith("*"):
        return Parameter(name[1:], Parameter.VAR_POSITIONAL)
    return Parameter(name, kind)
