import pytest
import random

sex = random.randint(0, 1)
print(sex)


@pytest.mark.skipif(sex == 1, reason='没钱~~~~~~~~~~~~~~~~~')
def test_add_cart():
    print('添加购物车')


@pytest.mark.skipif(sex == 0, reason='有钱~~~~~~~~~~~~~~~~~~')
def test_balance():
    print('查看余额')
