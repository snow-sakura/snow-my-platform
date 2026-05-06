import pytest
import requests

url = "http://47.108.206.100:8080/admin/login"

data = [{"username": "admin", "password": "macro123"},
        {"username": "admin", "password": "macro1234"}]


@pytest.mark.parametrize("body", data)
def test_login(body):
    url = "http://47.108.206.100:8080/admin/login"
    print('*' * 100)
    resp = requests.post(url=url, json=body)
    result = resp.json()
    print(result)

    code = resp.status_code
    message = result.get("message")
    bearer = result.get("data").get("tokenHead")
    assert message == "操作成功"
    assert bearer == "Bearer "
    assert code == 200
