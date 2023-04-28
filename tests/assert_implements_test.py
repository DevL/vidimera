import re
import pytest
from src.vidimera import assert_implements


def test_assert_implements(interface, implementation, partial_implementation):
    assert_implements(implementation, interface)
    expected_message = re.escape("Missing behaviour:\n  method(self, a, b)")
    with pytest.raises(AssertionError, match=expected_message):
        assert_implements(partial_implementation, interface)
