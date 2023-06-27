import re
import pytest
from src.vidimera import assert_implements, Behaviour


def test_assert_implements(interface, implementation, partial_implementation):
    assert_implements(implementation, interface)
    expected_message = re.escape("Missing behaviour:\n  method(self, a, b)")
    with pytest.raises(AssertionError, match=expected_message):
        assert_implements(partial_implementation, interface)


def test_assert_implements_honours_scopes(interface, different_constructor):
    assert_implements(different_constructor, interface, scope=Behaviour.PUBLIC)
    expected_message = re.escape("Missing behaviour:\n  __init__(self, arg, keyword='default')")
    with pytest.raises(AssertionError, match=expected_message):
        assert_implements(different_constructor, interface)
