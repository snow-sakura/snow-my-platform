import pytest
from db.db import DB
from interface.cartInterface import CartInterface
from interface.memberInterface import MemberInterface
from interface.orderInterface import OrderInterface
from utils.Jsonpath import GetKeyword


class Test_Process:

    #  登录
    def setup(self):
        data = {
            "username": "admin987",
            "password": "123456"
        }
        self.url = 'http://47.108.206.100:8085'
        self.headers = MemberInterface(self.url).get_token(data)
        MemberInterface(url=self.url).login(data)
        self.order = OrderInterface(url=self.url, headers=self.headers)

        data = DB().read('select id from oms_cart_item where member_id=1826 order by id desc;')
        self.keyword = GetKeyword.git_keyword(data[1], 'id')

        # 查询购买前商品的库存

    def test_01_before(self):
        rows, data = DB().read('select stock from pms_sku_stock where id=98')
        keyword = GetKeyword.git_keyword(data, 'stock')
        print()
        print(f'购买前的库存{keyword}')
        # 断言
        pytest.assume(keyword > 0)
        # 添加购物车

    def test_02_face(self):
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
        CartInterface(url=self.url, headers=self.headers).cart_add(data)
        data = DB().read('select id from oms_cart_item where member_id=1826 order by id desc;')
        self.keyword = GetKeyword.git_keyword(data[1], 'id')
        rows, data = DB().read(f'SELECT delete_status FROM oms_cart_item WHERE id ={self.keyword};')
        delete_status = GetKeyword.git_keyword(data, 'delete_status')
        # 断言
        assert delete_status == 0

        # 确认订单

    def test_03_confirm(self):
        confirm_result = self.order.confirm_order(self.keyword)
        cartpromotionitemlist = GetKeyword.git_keyword(confirm_result, 'cartPromotionItemList')
        assert cartpromotionitemlist is not None  # 断言购物车列表不为空
        memberReceiveAddressList = GetKeyword.git_keyword(confirm_result, 'memberReceiveAddressList')
        assert memberReceiveAddressList is not None  # 断言收货地址列表不为空

        # 生成订单

    def test_04_generate(self):
        self.order.generate_order(self.keyword, 2549, 1)
        rows, data = DB().read('select status from oms_order where member_id=1826 order by id desc;')
        status_before = GetKeyword.git_keyword(data, 'status')

        # 断言
        assert status_before == 0

        # 支付返回

    def test_05_pay(self):
        data = DB().read('select id from oms_order where member_id=1826 order by id desc;')
        keyword1 = GetKeyword.git_keyword(data[1], 'id')
        data = self.order.pay_success(keyword1, 1)
        success = GetKeyword.git_keyword(data, 'data')

        # 断言
        assert success == 1

    # 查询购买后的产品数
        rows, data = DB().read('select stock from pms_sku_stock where id=98')
        keyword = GetKeyword.git_keyword(data, 'stock')
        print()
        print(f'购买后的库存{keyword}')
