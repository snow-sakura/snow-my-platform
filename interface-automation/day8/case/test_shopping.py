import pytest
from db.db import DB
from interface.cartInterface import CartInterface
from interface.orderInterface import OrderInterface
from utils.Jsonpath import GetKeyword


class Test_Process:
    # 查询购买前商品的库存
    def test_01_before(self):
        rows, data = DB().read('select stock from pms_sku_stock where id=106')
        keyword = GetKeyword.git_keyword(data, 'stock')
        print(f'购买前的库存{keyword}')
        # 断言
        pytest.assume(keyword > 0)

    # 添加购物车
    def test_02_face(self, url, headers):
        data = {
            "createDate": "2022-06-10T02:01:35.734Z",
            "deleteStatus": 0,
            "id": 0,
            "memberId": 1826,
            "memberNickname": "tom",
            "modifyDate": "2022-06-10T04:01:35.734Z",
            "price": 5499,
            "productAttr": '[{"key":"颜色","value":"金色"},{"key":"容量","value":"32G"}]',
            "productBrand": "苹果",
            "productCategoryId": 19,
            "productId": 29,
            "productName": "Apple iPhone 8 Plus 64GB 红色特别版 移动联通电信4G手机",
            "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5acc5248N6a5f81cd.jpg",
            "productSkuCode": "201808270029001",
            "productSkuId": 106,
            "productSn": "7437799",
            "productSubTitle": "【限时限量抢购】Apple产品年中狂欢节，好物尽享，美在智慧！速来 >> 勾选[保障服务][原厂保2年]，获得AppleCare+全方位服务计划，原厂延保售后无忧。",
            "quantity": 1
        }
        CartInterface(url=url, headers=headers).cart_add(data)
        data = DB().read('select id from oms_cart_item where member_id=1826 order by id desc;')
        keyword = GetKeyword.git_keyword(data[1], 'id')
        rows, data = DB().read(f'select delete_status from oms_cart_item where id ={keyword};')
        delete_status = GetKeyword.git_keyword(data, 'delete_status')
        # 断言
        assert delete_status == 0

        # 确认订单

    def test_03_confirm(self, url, headers, keyword):
        confirm_result = OrderInterface(url=url, headers=headers).confirm_order(keyword)
        cartpromotionitemlist = GetKeyword.git_keyword(confirm_result, 'cartPromotionItemList')
        assert cartpromotionitemlist is not None  # 断言购物车列表不为空
        memberReceiveAddressList = GetKeyword.git_keyword(confirm_result, 'memberReceiveAddressList')
        assert memberReceiveAddressList is not None  # 断言收货地址列表不为空

        # 生成订单

    def test_04_generate(self, url, headers, keyword):
        OrderInterface(url=url, headers=headers).generate_order(keyword, 2549, 1)
        rows, data = DB().read('select status from oms_order where member_id=1826 order by id desc;')
        status_before = GetKeyword.git_keyword(data, 'status')

        # 断言
        assert status_before == 0

        # 支付返回

    def test_05_pay(self, url, headers):
        data = DB().read('select id from oms_order where member_id=1826 order by id desc;')
        keyword1 = GetKeyword.git_keyword(data[1], 'id')
        data = OrderInterface(url=url, headers=headers).pay_success(keyword1, 1)
        success = GetKeyword.git_keyword(data, 'data')

        # 断言
        assert success == 1

    # 查询购买后的产品数
    def test_06_behind(self):
        rows, data = DB().read('select stock from pms_sku_stock where id=106')
        keyword = GetKeyword.git_keyword(data, 'stock')
        print()
        print(f'购买后的库存{keyword}')
