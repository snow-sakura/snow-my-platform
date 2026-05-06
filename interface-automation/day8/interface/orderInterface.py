

from interface.memberInterface import MemberInterface
from utils.SendMethod import SendMethod


class OrderInterface:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

        # 确认订单

    def confirm_order(self, data):
        url = self.url + "/order/generateConfirmOrder"
        return SendMethod.send_method(method='post', url=url, json=[data], headers=self.headers)

        # 生成订单

    def generate_order(self, cat_id, address_id, type_id):
        url = self.url + "/order/generateOrder"
        data = {
            "cartIds": [
                cat_id
            ],
            "memberReceiveAddressId": address_id,
            "payType": type_id,

        }
        return SendMethod.send_method(method='post', url=url, json=data, headers=self.headers)

        # 添加收货地址

    def address_add(self):
        url = self.url + '/member/address/add'
        data = {
            "city": "武汉",
            "defaultStatus": 0,
            "detailAddress": "源码黑马",
            "id": 0,
            "memberId": 1826,
            "name": "沙漠死神吃西瓜",
            "phoneNumber": "13012345678",
            "postCode": "432000",
            "province": "湖北省",
            "region": "洪山区"
        }
        return SendMethod.send_method(method='post', url=url, json=data, headers=self.headers)

        # 查看地址信息

    def get_address_id(self, params):
        url = self.url + f"/member/address/{params}"
        return SendMethod.send_method(method='get', url=url, headers=self.headers)

        # 支付回调

    def pay_success(self,order_id,num):
        url = self.url + '/order/paySuccess'
        data = {
            "orderId": order_id,
            "payType": num
        }
        return SendMethod.send_method(method='post', url=url, data=data, headers=self.headers)


if __name__ == '__main__':
    url = 'http://47.108.206.100:8085'
    keyword = {
        "username": "admin987",
        "password": "123456"
    }
    headers = MemberInterface(url).get_token(keyword)
    order = OrderInterface(url, headers)
    # print(order.confirm_order(2984))
    # print('*' * 100)
    # print(order.generate_order(2984, 2457, 1))
    print(order.address_add())
    # print(order.get_address_id(2457))
    # print(order.pay_success(2984, 1))
