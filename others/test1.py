import requests
from bs4 import BeautifulSoup


url = "https://vpn.cgl.org.cn/https/77726476706e69737468656265737421f6ef0f9f203c265f6c0fc7af96/s?strtype=&jxsearch=&sw=%E9%87%91%E7%9F%BF"
response = requests.get(url)
# 检查请求是否成功
if response.status_code == 200:
    print("请求成功")
else:
    print("请求失败")



soup = BeautifulSoup(response.text, 'html.parser')
# find_all查找包含论文信息的所有div元素，text属性用来获取元素中的文本。
papers = soup.find_all("div", class_="paper")
for paper in papers:
    title = paper.find("h2").text
    authors = paper.find("span", class_="authors").text
    abstract = paper.find("div", class_="abstract").text
    print(f"标题：{title}\n作者：{authors}\n摘要：{abstract}")


with open("papers.txt", "w") as file:
    for paper in papers:
        file.write(f"标题：{title}\n作者：{authors}\n摘要：{abstract}\n\n")

