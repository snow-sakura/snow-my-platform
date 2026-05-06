import requests


class SendMethod:
    @staticmethod
    def send_method(method, url, params=None, data=None, json=None, headers=None):
        if method in ["get", "post"]:
            resp = requests.request(method=method, url=url, params=params, data=data, json=json, headers=headers)
        else:
            resp = None

        result = {}
        if resp is not None:
            result['status_codes'] = resp.status_code
            # result['headers'] = resp.headers
            result['body'] = resp.json()
            result['status_time'] = int(resp.elapsed.microseconds / 1000)
            return result
        else:
            return resp


if __name__ == '__main__':
    url = "http://47.108.206.100:8080/admin/login"
    method = "post"
    body = {
        "username": "admin",
        "password": "macro123"
    }
    print(SendMethod.send_method(method=method, url=url, json=body))
