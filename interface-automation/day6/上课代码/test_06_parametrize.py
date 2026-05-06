import pytest


@pytest.mark.parametrize('phone', ['13476540127', '15171019064', '13967640493'])
def test_01(phone):
    print(f'我的手机号是{phone}')


data = [[13476540127, 123456], [15171019064, 123456], [13456788443, 133553]]


@pytest.mark.parametrize('phone,code', data)
def test_02(phone, code):
    print(f'手机号是{phone},验证码是{code}')
