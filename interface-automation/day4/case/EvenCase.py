from interface.Event import Event


class EventCase:
    def __init__(self):
        self.even = Event()

    def test_01(self):
        body = {
            "eid": 34311,
            "name": "phone1291",
            "limit": 30,
            "status": 1,
            "address": "源码时代",
            "start_time": "2021-7-20"
        }

        result = self.even.event_add(body)
        print(result)
        status_code = result.get('status_code')
        assert status_code == 200

    def test_02(self):
        params = {
            "eid": "31411",
            "name": "phone1911"
        }
        result1 = self.even.event_get(params)
        print(result1)
        status_code = result1.get('status_code')
        assert status_code == 200


if __name__ == '__main__':
    EventCase().test_01()
    print('*' * 100)
    EventCase().test_02()
