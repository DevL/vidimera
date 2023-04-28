import pytest
from inspect import signature
from src.vidimera import Behaviour, MissingBehaviour
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


@pytest.fixture
def empty_missing_behaviour():
    return MissingBehaviour(set())


@pytest.fixture
def missing_behaviour():
    return MissingBehaviour(
        set(
            {
                "func": signature(missing_function),
                "add_one": signature(lambda x: x + 1),
            }.items()
        )
    )


def missing_function(x, y, /, z=0, **kwargs):
    return x + y + z
