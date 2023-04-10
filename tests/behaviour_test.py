from functools import partial
from inspect import Parameter, Signature
from src.vidimera import Behaviour
from .assets import SimpleObject


def test_repr():
    assert repr(Behaviour(object)) == "<Behaviour of <class 'object'>>"


def test_signatures():
    expected_signatures = set(
        [
            ("A_CALLABLE_CONTSTANT", _signature("value", kind=Parameter.POSITIONAL_OR_KEYWORD)),
            ("__call__", _method("func", kind=Parameter.POSITIONAL_OR_KEYWORD)),
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
    behaviour = Behaviour(SimpleObject)
    assert behaviour.signatures() >= expected_signatures


def _method(*params, kind=Parameter.POSITIONAL_ONLY):
    return _signature("self", *params, kind=kind)


def _signature(*params, kind=Parameter.POSITIONAL_ONLY):
    return Signature(parameters=map(partial(_param, kind), params))


def _param(kind, name):
    if name.startswith("**"):
        return Parameter(name[2:], Parameter.VAR_KEYWORD)
    if name.startswith("*"):
        return Parameter(name[1:], Parameter.VAR_POSITIONAL)
    return Parameter(name, kind)
