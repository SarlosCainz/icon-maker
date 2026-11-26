import pytest

import util


def test_get_param_returns_value():
    """U1"""
    assert util.get_param({"a": "1"}, "a", "x") == "1"


def test_get_param_returns_default():
    """U2"""
    assert util.get_param({}, "a", "x") == "x"


def test_get_int_param_converts_string():
    """U3"""
    assert util.get_int_param({"a": "42"}, "a", 0) == 42


def test_get_int_param_uses_default():
    """U4"""
    assert util.get_int_param({}, "a", "7") == 7


def test_get_int_param_doubles_for_web():
    """U5"""
    assert util.get_int_param({"a": "10"}, "a", 0, 0, 1) == 20


def test_get_int_param_quadruples_for_ios():
    """U6"""
    assert util.get_int_param({"a": "10"}, "a", 0, 1, 0) == 40


def test_get_int_param_prefers_for_ios():
    """U7 for_ios と for_web を同時に指定したら for_ios が優先される"""
    assert util.get_int_param({"a": "10"}, "a", 0, 1, 1) == 40


def test_get_int_param_rejects_non_number():
    """U8"""
    with pytest.raises(util.InvalidParam) as e:
        util.get_int_param({"a": "abc"}, "a", 0)
    assert e.value.param == "a"
    assert e.value.reason == "整数で指定する"


def test_get_int_param_accepts_value_in_range():
    """U9"""
    assert util.get_int_param({"a": "5"}, "a", 0, minimum=0, maximum=5) == 5


@pytest.mark.parametrize("value", ["-1", "6"])
def test_get_int_param_rejects_value_out_of_range(value):
    """U10"""
    with pytest.raises(util.InvalidParam) as e:
        util.get_int_param({"a": value}, "a", 0, minimum=0, maximum=5)
    assert e.value.param == "a"
    assert e.value.reason == "0 以上 5 以下の整数で指定する"


def test_get_int_param_checks_range_before_scaling():
    """U11 範囲の検証は倍率をかける前の値に対して行う"""
    assert util.get_int_param({"a": "400"}, "a", 0, 1, 0, minimum=1, maximum=400) == 1600


def test_get_choice_param_accepts_choice():
    """U12"""
    assert util.get_choice_param({"a": "ja"}, "a", "en", ["en", "ja"]) == "ja"


def test_get_choice_param_rejects_unknown():
    """U12"""
    with pytest.raises(util.InvalidParam) as e:
        util.get_choice_param({"a": "xx"}, "a", "en", ["en", "ja"])
    assert e.value.param == "a"
    assert "en, ja" in e.value.reason


def test_get_choice_param_uses_default():
    """U12 キーが無ければ既定値が選択肢として検証される"""
    assert util.get_choice_param({}, "a", "en", ["en", "ja"]) == "en"
