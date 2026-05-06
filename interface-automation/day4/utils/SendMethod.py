import requests


class SendMethod:
    @staticmethod
    def send_method(method, url, params=None, data=None):
        if method == 'post':
            response = requests.post(url=url, data=data)
        elif method == 'get':
            response = requests.get(url=url, params=params)
        else:
            response = None
            print("请求方式错误")

        result = {}
        if response is not None:
            result['status_code'] = response.status_code
            result['headers'] = response.headers
            result['body'] = response.json()

            return result
        else:
            return response


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/api/add_event/'
    body = {
        "eid": 924,
        "name": "phone121",
        "limit": 30,
        "status": 1,
        "address": "源码时代",
        "start_time": "2021-7-20"
    }
    method = 'post'
    print(SendMethod.send_method(method=method, url=url, data=body))
