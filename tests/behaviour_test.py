import pytest
from functools import partial
from inspect import Parameter, Signature
from sys import version_info
from src.vidimera import Behaviour, MissingBehaviour
from .assets import Interface, Implementation, PartialImplementation

require_python_3_12_or_lower = pytest.mark.skipif(
    version_info > (3, 12), reason="invalid for Python 3.13 or higher"
)

require_python_3_13_or_higher = pytest.mark.skipif(
    version_info < (3, 13), reason="invalid for Python 3.12 and lower"
)


def test_repr():
    assert repr(Behaviour(object)) == "<Behaviour of <class 'object'>>"


def test_creating_a_behaviour_of_another_behaviour_returns_it_unchanged(behaviour):
    expected_signatures = behaviour.signatures()
    assert Behaviour(behaviour) is behaviour
    assert Behaviour(behaviour).signatures() == expected_signatures


@require_python_3_13_or_higher
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
            inherited("__getstate__"),
            inherited("__gt__", "value"),
            defined("__init__", "value"),
            signature("__init_subclass__"),
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
            signature("__subclasshook__", "object", kind=Parameter.POSITIONAL_ONLY),
            defined("public_method", "*args", "**kwargs"),
        ]
    )
    assert behaviour.signatures() >= expected_signatures


@require_python_3_12_or_lower
def test_signatures_for_python_3_12_and_older(behaviour):
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


@require_python_3_13_or_higher
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
            inherited("__getstate__"),
            inherited("__gt__", "value"),
            defined("__init__", "value"),
            # no_signature("__init_subclass__"),
            signature("__init_subclass__"),
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
            # no_signature("__subclasshook__"),
            signature("__subclasshook__", "object", kind=Parameter.POSITIONAL_ONLY),
        ]
    )
    assert behaviour.signatures(scope=Behaviour.SPECIAL) >= expected_signatures


@require_python_3_12_or_lower
def test_special_signatures_for_python_3_12_and_older(behaviour):
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


def test_implemented_by(interface, implementation, partial_implementation, different_constructor):
    assert interface.implemented_by(Implementation)
    assert interface.implemented_by(implementation)
    assert interface.implemented_by(different_constructor, scope=Behaviour.PUBLIC)
    assert not interface.implemented_by(PartialImplementation)
    assert not interface.implemented_by(partial_implementation)
    assert not interface.implemented_by(different_constructor)


def test_implements(interface, implementation, partial_implementation, different_constructor):
    assert implementation.implements(Interface)
    assert implementation.implements(interface)
    assert not partial_implementation.implements(Interface)
    assert not partial_implementation.implements(interface)
    assert not different_constructor.implements(Interface)
    assert different_constructor.implements(Interface, scope=Behaviour.PUBLIC)
    assert isinstance(partial_implementation.implements(Interface), MissingBehaviour)


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
