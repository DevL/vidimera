def test_an_empty_missing_behaviour_is_truthy(empty_missing_behaviour):
    assert empty_missing_behaviour


def test_a_non_empty_missing_behaviour_is_falsy(missing_behaviour):
    assert not missing_behaviour


def test_str_of_an_empty_missing_behaviour(empty_missing_behaviour):
    expected = "No missing behaviour"
    assert str(empty_missing_behaviour) == expected


def test_str_of_a_missing_behaviour(missing_behaviour):
    expected = "Missing behaviour:" "\n  add_one(x)" "\n  func(x, y, /, z=0, **kwargs)"
    assert str(missing_behaviour) == expected


def missing_function(x, y, /, z=0, **kwargs):
    return x + y + z
