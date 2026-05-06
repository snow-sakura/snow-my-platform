# 接口测试-day01-作业



1，请简述接口的概念？

答案：

```text
系统之间的数据交互的通道,包括外部系统和内部系统和内部系统和内部系统
```

2，请简述接口测试的概念

答案：

```text
校正接口数据结果和预期数据结果是否一致
```

3，为什么要进行接口测试？（价值）

答案：

```text
可以测试页面测试不到的问题,测试成本低效率高,可以早期介入测试流程 降低风险
```

4，我们可以使用哪些方式来实现接口测试？

答案：

```text
工具和代码  工具有postman  代码有pytest
```

5，请写出HTTP协议的5个特点

答案：

```text
客户端/服务器模式,无状态,无连接,简单快速,灵活
```

6，写出URL的格式，由哪 5 部分组成？

答案：

```text
协议,域名,端口号(可选) 资源路径, 查询参数
```

7，请写出 URL http://www.itsource.cn/subject/pythonzly/index.shtml?a=1&b=2 中，每个部分的内容

答案：

```text
http协议 www.itsuorce.cn域名 subject/pythonzly/index.shtml资源路径 a=1&b=2查询参数
```

8，以下关于HTTP请求的描述，错误的是？

A： HTTP请求包括了请求行，请求头，请求体

B： HTTP请求行包括协议/版本，URL，请求方法

C： HTTP请求头用于描述客户端信息

D： HTTP请求头中Content-Type用于描述客户端浏览器类型

E： HTTP请求中，只有Post请求才有请求体。

F： HTTP请求中，按照标准规范，请求的数据类型是由Content-Type来进行标志的。

答案

```text
CDE
```

9，在HTTP请求中，有哪些常用的请求方法？

答案：

```text
post get delete put
```

10，HTTP响应主要包括哪几个部分？

答案：

```text
响应行, 响应头, 响应体
```

11，简述接口测试流程。

答案：

```text
需求分析 API接口文档解析 设计测试用例 准备接口测试脚本 执行用例跟踪BUG 
```

12，有如下 http请求，请分别写出 请求方法、URL、协议和域名、资源路径、请求行、请求头、请求体。

```http
POST http://demo.zentao.net/user-login.html HTTP/1.1
Host: demo.zentao.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://demo.zentao.net/user-login.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 54
Connection: keep-alive
Upgrade-Insecure-Requests: 1

account=demo&password=efc4a3b32e48054865e5a8321cfda3e4
```

答案：

```yacas
请求方法:post URL:http://demo.zentao.net/user-login.html  协议:http 域名:demo.zentao.net/
资源路径:user-login.html 
请求行:POST http://demo.zentao.net/user-login.html HTTP/1.1
请求头:
Host: demo.zentao.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://demo.zentao.net/user-login.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 54
Connection: keep-alive
Upgrade-Insecure-Requests: 1
请求体:account=demo&password=efc4a3b32e48054865e5a8321cfda3e4
```

13，有如下 http 响应包，请分别写出 响应状态码、状态码描述、状态行、响应头、响应体的内容。

```http
HTTP/1.1 200 OK
Date: Fri, 22 May 2009 06:07:21 GMT
Content-Type: text/html; charset=UTF-8

<html>
	<head></head>
	<body>...</body>
</html>
```

答案：

```yacas
响应状态码:200 
状态行:HTTP/1.1 200 OK
响应头:Date: Fri, 22 May 2009 06:07:21 GMT
Content-Type: text/html; charset=UTF-8
响应体:
<html>
	<head></head>
	<body>...</body>
</html>
```

14，查看 《发布会项目接口文档》，解析添加嘉宾和查询嘉宾接口。

答案：

```yacas

```

