import jsonpath


class GetKeyword:
    @staticmethod
    def git_keywords(source_data, keyword):
        kw = jsonpath.jsonpath(source_data, f'$..{keyword}')
        if kw is False:
            print(f"查找的{keyword}不存在")
        else:
            return kw

    @staticmethod
    def git_keyword(source_data, keyword):
        kw = jsonpath.jsonpath(source_data, f'$..{keyword}')
        if kw is False:
            print(f"查找的{keyword}不存在")
        else:
            return kw[0]


if __name__ == '__main__':
    source_data = {'status_code': 200,
                   'headers': {
                       'Vary': 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers',
                       'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block',
                       'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate', 'Pragma': 'no-cache',
                       'Expires': '0', 'X-Frame-Options': 'DENY', 'Content-Type': 'application/json',
                       'Transfer-Encoding': 'chunked', 'Date': 'Fri, 10 Jun 2022 03:31:58 GMT',
                       'Keep-Alive': 'timeout=60', 'Connection': 'keep-alive'},
                   'body': {'code': 200, 'message': '操作成功', 'data': {'tokenHead': 'Bearer ', 'code': 201,
                                                                     'token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImNyZWF0ZWQiOjE2NTQ4MzE5MTgxNzgsImV4cCI6MTY1NTQzNjcxOH0.J5a0VrwfYJuV3ec5biygHF06U9lH0RtPyFMs8VF-buEGWVVFvyRKM8nI39Sv8Pc9A9XHkoJ5TYVxSuagVLj3rQ'}},
                   'response_time': 138}

    print(GetKeyword.git_keyword(source_data, "token"))
