import requests

url = "https://vpn.cgl.org.cn/https/77726476706e69737468656265737421f6ef0f9f203c265f6c0fc7af96/s?sw=%E9%87%91%E7%9F%BF&size=15&isort=0&x=642_243&pages=1"  # 替换为你要访问的网站

# 发送一个简单的请求
response = requests.get(url)

# 打印请求头
print(response.request.headers)
