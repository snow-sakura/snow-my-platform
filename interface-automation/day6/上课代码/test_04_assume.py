import pytest


def test_get_event():
    print('查询发布会')
    actual_name = '小米'
    expected_name = '小米发布会'
    assert actual_name in expected_name


def test_equal():
    pytest.assume("abc" == "abc")
    pytest.assume(200 == 200)
    print('1111')
    pytest.assume(True is True)
