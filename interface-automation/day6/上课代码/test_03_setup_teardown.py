class Test_mode:
    def setup_class(self):
        print('类级setup')

    def teardown_class(self):
        print('类级teardown')

    def setup(self):
        print('方法setup')

    def teardown(self):
        print('方法teardown')

    def test_demo1(self):
        print("demo1")

    def test_demo2(self):
        print("demo2")
