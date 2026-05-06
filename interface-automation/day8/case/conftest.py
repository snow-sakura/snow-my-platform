import os

import pytest

from db.db import DB
from interface.memberInterface import MemberInterface
from utils.Jsonpath import GetKeyword

data = {"username": "admin987", "password": "123456"}


# 在fixture中,1.fixture之间可以相互引用;
# 2.低级别的fixture可以引用高级别的fixture;高级别的fixture不能引用低级别的fixture


@pytest.fixture(scope="session")
def url(url="http://47.108.206.100:8085"):
    return url


@pytest.fixture(scope="session")
def headers(url):
    return MemberInterface(url).get_token(data)


@pytest.fixture(scope="session")
def keyword():
    data = DB().read(
        'select id from oms_cart_item where member_id=1826 order by id desc;')
    return GetKeyword.git_keyword(data[1], 'id')
