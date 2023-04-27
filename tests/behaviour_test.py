from functools import partial
from inspect import Parameter, Signature
from src.vidimera import Behaviour
from .assets import SimpleObject


def test_repr():
    assert repr(Behaviour(object)) == "<Behaviour of <class 'object'>>"


def test_signatures():
    expected_signatures = set(
        [
            signature("A_CALLABLE_CONTSTANT", "value"),
            defined("__call__", "func"),
            no_signature("__class__"),
            inherited("__delattr__", "name"),
            inherited("__dir__"),
            defined("__eq__", "other"),
            inherited("__format__", "format_spec"),
            inherited("__ge__", "value"),
            inherited("__getattribute__", "name"),
            inherited("__gt__", "value"),
            defined("__init__", "value"),
            no_signature("__init_subclass__"),
            inherited("__le__", "value"),
            inherited("__lt__", "value"),
            inherited("__ne__", "value"),
            signature("__new__", "*args", "**kwargs"),
            inherited("__reduce__"),
            inherited("__reduce_ex__", "protocol"),
            inherited("__repr__"),
            inherited("__setattr__", "name", "value"),
            inherited("__sizeof__"),
            inherited("__str__"),
            no_signature("__subclasshook__"),
            defined("public_method", "*args", "**kwargs"),
        ]
    )
    behaviour = Behaviour(SimpleObject)
    assert behaviour.signatures() >= expected_signatures


def defined(name, *params):
    return signature(name, "self", *params, kind=Parameter.POSITIONAL_OR_KEYWORD)


def inherited(name, *params):
    return signature(name, "self", *params, kind=Parameter.POSITIONAL_ONLY)


def no_signature(name):
    return name, Behaviour.NO_SIGNATURE


def signature(name, *params, kind=Parameter.POSITIONAL_OR_KEYWORD):
    return name, Signature(parameters=map(partial(_param, kind), params))


def _param(kind, name):
    if name.startswith("**"):
        return Parameter(name[2:], Parameter.VAR_KEYWORD)
    if name.startswith("*"):
        return Parameter(name[1:], Parameter.VAR_POSITIONAL)
    return Parameter(name, kind)
