import pymysql
import pytest
import os

from db.db import DB
from interface.memberInterface import MemberInterface
from utils.Jsonpath import GetKeyword
from utils.OperationJson import OperationJson

jsonpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data/login_json.json'
path = OperationJson.operationjson(jsonpath)


class TestLogin:
    @pytest.mark.parametrize('test_data', path)
    def test_login(self, test_data):
        url = 'http://47.108.206.100:8085'
        payload = {
            "username": test_data['username'],
            "password": test_data['password']
        }
        response = MemberInterface(url).login(data=payload)
        assert GetKeyword.git_keyword(response, 'code') == test_data['code']

        print('*' * 100)
        print(response)
        data = DB().read(
            'select id from oms_cart_item where member_id=1826 order by id desc;')
        print(data[1])
        print(GetKeyword.git_keyword(data[1], 'id'))
