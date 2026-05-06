import pymysql


# 数据库操作模块
# 封装一个数据库操作类 DB
# 读方法 read(sql) return 受影响行数, 结果集
# 写方法 write(sql) return 受影响行数

class DB:
    def __init__(self, database='mall', host='47.108.206.100', user='student', password='stu2022', port=3306, charset='utf8',
                 cursor_type=pymysql.cursors.DictCursor): # 初始化 格式是字典还是 元组 pymysql.cursors.cursor
        # 初始化连接对象
        self.__conn = pymysql.connect(host=host, user=user, password=password, port=port, charset=charset,
                                      database=database)
        # 初始化游标对象
        # 游标类型: 元组, 字典
        self.__cursor = self.__conn.cursor(cursor_type)

    def read(self, sql, params_list=[]):
        try:
            # 执行sql语句
            rows = self.__cursor.execute(sql, params_list)
            # 获取结果集
            data = self.__cursor.fetchone()  # 单条用fetchone  多条用fetchall()
        except Exception as e:
            print('sql语句有问题')
            return None, 'No Data'
        return rows, data

    def write(self, sql):
        try:
            # 执行sql语句
            rows = self.__cursor.execute(sql)
        except Exception as e:
            # 回滚
            self.__conn.rollback()
            return 0
        else:
            # 提交
            self.__conn.commit()
        return rows

    def __del__(self):
        # 对象销毁后执行的方法
        self.__cursor.close()
        self.__conn.close()


if __name__ == '__main__':
    # db = DB('advanced', cursor_type=pymysql.cursors.DictCursor)
    # rows, data = db.read('select * from student')
    # print(data)
    # name = input('name:')
    # rows, data = db.read(f'select * from student where stu_name=%s', [name])
    # print(data)

    db = DB('mall', cursor_type=pymysql.cursors.DictCursor)
    # 读操作
    rows, data = db.read('select stock from pms_sku_stock where id=98')
    if rows:
        print(rows, data)

    # 写操作
    # rows = db.write("INSERT INTO student(stu_no, stu_name) VALUES('itsrc-017', '周杰伦1')")
    #
    # if rows:
    #     print('写入成功')
    # """
