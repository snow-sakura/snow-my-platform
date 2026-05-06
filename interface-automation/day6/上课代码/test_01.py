import pytest


class TestDemo:
    def test_demo1(self):
        print("demo1")

    def test_demo2(self):
        print("demo2")


if __name__ == '__main__':
    pytest.mian(['-s', 'test_01.py'])
