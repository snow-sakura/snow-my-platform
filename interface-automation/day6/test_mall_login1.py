import pytest
import requests


class TestLogin:
    data = [{
        "login_data": {"username": "admin", "password": "macro123"},
        "code": 200,
        "desc": "正确的用户名和密码"
    },
        {
            "login_data": {"username": "admin", "password": "macro12"},
            "code": 500,
            "desc": "错误的密码"
        }]

    @pytest.mark.parametrize('body', data)
    def test_login(self, body):
        url = "http://47.108.206.100:8080/admin/login"
        json = body.get('login_data')
        print('*' * 100)
        resp = requests.post(url=url, json=json)
        result = resp.json()
        print(result)

        assert resp.status_code == body.get('code')


