from utils.SendMethod import SendMethod


class Event:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000'

    def event_add(self, data):
        method = 'post'
        url = self.url + '/api/add_event/'
        return SendMethod.send_method(method=method, url=url, data=data)

    def event_get(self, params):
        method = 'get'
        url = self.url + '/api/get_event_list/'
        return SendMethod.send_method(method=method, url=url, params=params)


if __name__ == '__main__':
    body = {
        "eid": 314111,
        "name": "phone19111",
        "limit": 30,
        "status": 1,
        "address": "源码时代",
        "start_time": "2021-7-20"
    }
    print(Event().event_add(body))
