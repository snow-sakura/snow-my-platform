import requests

body = {
    "username": "admin",
    "password": "macro123"
}
URL = "http://47.108.206.100:8080/admin/login"

response = requests.post(URL, json=body)
print(response.status_code)
print(response.json())
print(response.json().get("message"))
print(response.json().get("data").get("token"))
