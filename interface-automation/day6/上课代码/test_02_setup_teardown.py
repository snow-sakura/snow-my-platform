def setup_module():
    print('这是模块级setup')


def setup_function():
    print('函数级setup')


def teardown_function():
    print('函数级teardown')


def teardown_module():
    print('这是模块级别teardown')


def test_demo1():
    print("demo1")


def test_demo2():
    print("demo2")
