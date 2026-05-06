from day3.utils.SendMethod import SendMethod
from day3.utils.Jsonpath import GetKeyword


class MemberInterface:
    def __init__(self, url):
        self.url = url

    # 获取验证码
    def get_code(self, params):
        url = self.url + '/sso/getAuthCode'
        return SendMethod.send_method(method='get', url=url, params=params)

    # 提取验证码
    def extract_code(self, params):
        resp = self.get_code(params)
        return GetKeyword.git_keyword(resp, 'data')

    # 注册
    def register(self, data):
        url = self.url + '/sso/register'
        return SendMethod.send_method(method='post', url=url, data=data)

    # 登录
    def login(self, data):
        url = self.url + '/sso/login'
        return SendMethod.send_method(method='post', url=url, data=data)

    # 获取token
    def get_token(self, data):
        resp = self.login(data)
        token = GetKeyword.git_keyword(resp, 'token')
        return {'Authorization': f'Bearer {token}'}

    # 修改密码
    def change_password(self, data):
        url = self.url + '/sso/updatePassword'
        return SendMethod.send_method(method='post', url=url, data=data)

    # 获取会员信息
    def get_info(self, params):
        resp = self.get_token(data)
        url = self.url + '/sso/info'
        return SendMethod.send_method(method='get', url=url, params=params, headers=resp)


if __name__ == '__main__':
    url = 'http://47.108.206.100:8085'
    m1 = MemberInterface(url)
    # telephone = '13476540139'
    # payload = {
    #     "username": "admin987",
    #     "password": "123456",
    #     "telephone": telephone,
    #     "authCode": m1.extract_code(params={"telephone": telephone})
    #
    # }
    # print(m1.register(payload))
    data = {
        "username": "admin987",
        "password": "123456"
    }
    # print(m1.login(data=data))
    print(m1.get_info(params='admin987'))
    # print(m1.get_token(data))
    # telephone = 13476540139
    # data = {
    #     "password": "123456",
    #     "telephone": telephone,
    #     "authCode": m1.extract_code(params={"telephone": telephone})
    # }
    # print(m1.change_password(data))
