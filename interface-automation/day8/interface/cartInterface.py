from interface.memberInterface import MemberInterface
from utils.SendMethod import SendMethod
import pymysql


class CartInterface:
    # 添加购物车
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def cart_add(self, data):
        url = self.url + '/cart/add'
        return SendMethod.send_method(method='post', url=url, json=data, headers=self.headers)


if __name__ == '__main__':
    url = 'http://47.108.206.100:8085'
    keyword = {
        "username": "admin987",
        "password": "123456"
    }
    headers = MemberInterface(url).get_token(keyword)
    print(headers)

    data = {
        "createDate": "2022-06-10T02:01:35.734Z",
        "deleteStatus": 0,
        "id": 0,
        "memberId": 1826,
        "memberNickname": "tom",
        "modifyDate": "2022-06-10T04:01:35.734Z",
        "price": 2699,
        "productAttr": '[{"key":"颜色","value":"黑色"},{"key":"容量","value":"32G"}]',
        "productBrand": "小米",
        "productCategoryId": 19,
        "productId": 27,
        "productName": "小米8 全面屏游戏智能手机 6GB+64GB 黑色 全网通4G 双卡双待",
        "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/xiaomi.jpg",
        "productSkuCode": "201808270027001",
        "productSkuId": 98,
        "productSn": "7437788",
        "productSubTitle": "骁龙845处理器，红外人脸解锁，AI变焦双摄，AI语音助手小米6X低至1299，点击抢购",
        "quantity": 1
    }
    print(CartInterface(url, headers).cart_add(data))
    # conn = pymysql.connect(host='47.108.206.100', port=3306, user='student', password='stu2022', database='mall',
    #                        charset='utf8')
    # cursor = conn.cursor()
    # sql = 'SELECT delete_status FROM oms_cart_item WHERE id =2700;'
    # cursor.execute(sql)
    # result = cursor.fetchone()
    # print(result)
    # cursor.close()
    # conn.close()
    # assert result.index(0) == 0
