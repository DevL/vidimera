import pytest
from functools import partial
from inspect import Parameter, Signature
from src.vidimera import Behaviour
from .assets import Interface, Implementation, PartialImplementation, SimpleObject


@pytest.fixture
def behaviour():
    return Behaviour(SimpleObject)


@pytest.fixture
def interface():
    return Behaviour(Interface)


@pytest.fixture
def implementation():
    return Behaviour(Implementation)


@pytest.fixture
def partial_implementation():
    return Behaviour(PartialImplementation)


def test_repr():
    assert repr(Behaviour(object)) == "<Behaviour of <class 'object'>>"


def test_creating_a_behaviour_of_another_behaviour_returns_it_unchanged(behaviour):
    expected_signatures = behaviour.signatures()
    assert Behaviour(behaviour) is behaviour
    assert Behaviour(behaviour).signatures() == expected_signatures


def test_signatures(behaviour):
    expected_signatures = set(
        [
            signature("A_CALLABLE_CONTSTANT", "value"),
            signature("A_LAMBDA", "x", "y"),
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
    assert behaviour.signatures() >= expected_signatures


def test_public_signatures(behaviour):
    expected_signatures = set(
        [
            signature("A_CALLABLE_CONTSTANT", "value"),
            signature("A_LAMBDA", "x", "y"),
            defined("public_method", "*args", "**kwargs"),
        ]
    )
    assert behaviour.signatures(scope=Behaviour.PUBLIC) >= expected_signatures


def test_private_signatures(behaviour):
    expected_signatures = set([defined("_private_method")])
    assert behaviour.signatures(scope=Behaviour.PRIVATE) >= expected_signatures


def test_special_signatures(behaviour):
    expected_signatures = set(
        [
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
        ]
    )
    assert behaviour.signatures(scope=Behaviour.SPECIAL) >= expected_signatures


def test_signatures_default_to_both_public_and_special(behaviour):
    assert behaviour.signatures() == behaviour.signatures(scope=Behaviour.PUBLIC_AND_SPECIAL)


def test_signatures_with_a_custom_selection_pattern(behaviour):
    expected_signatures = set(
        [
            defined("__eq__", "other"),
            inherited("__ge__", "value"),
            inherited("__gt__", "value"),
            inherited("__le__", "value"),
            inherited("__lt__", "value"),
            inherited("__ne__", "value"),
        ]
    )
    pattern = r"__[a-z]{2}__"
    assert behaviour.signatures(pattern) == expected_signatures


def test_comparing_signatures():
    interface = Behaviour(Interface).signatures()
    implementation = Behaviour(Implementation).signatures()
    partial_implementation = Behaviour(PartialImplementation).signatures()

    assert implementation > interface
    assert implementation - interface == {defined("additional_instance_method")}
    assert implementation - interface == partial_implementation - interface

    assert implementation > partial_implementation
    assert implementation - partial_implementation == {defined("method", "a", "b")}
    assert implementation - partial_implementation == interface - partial_implementation


def test_implemented_by(interface, implementation, partial_implementation):
    assert interface.implemented_by(Implementation)
    assert interface.implemented_by(implementation)
    assert not interface.implemented_by(PartialImplementation)
    assert not interface.implemented_by(partial_implementation)


def test_implements(interface, implementation, partial_implementation):
    assert implementation.implements(Interface)
    assert implementation.implements(interface)
    assert not partial_implementation.implements(Interface)
    assert not partial_implementation.implements(interface)


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
