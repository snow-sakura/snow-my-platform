import pytest


@pytest.fixture()
def login():
    print('登录成功')


def test_add_cart(login):
    print('添加购物车')


def test_balance(login):
    print('查看余额')


def test_show_goods():
    print('查看商品')
