import json
import os.path


class OperationJson:
    @staticmethod
    def operationjson(jsonpath):
        with open(jsonpath, mode='r', encoding='UTF-8') as f:
            json_data = json.load(f)
            return json_data


if __name__ == '__main__':
    jsonpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/data/login_json.json'
    print(OperationJson.operationjson(jsonpath))