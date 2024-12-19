import requests
from bs4 import BeautifulSoup

# 检索关键词
keywords = "金矿/金矿床"
# 文献搜索网站URL（假设该URL为搜索页面）
search_url = "https://scholar.google.com.hk/schhp?hl=zh-CN"

# 发送HTTP GET请求进行搜索
response = requests.get(search_url, params={"q": keywords})

# 检查请求是否成功
if response.status_code == 200:
    # 解析网页内容
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 假设每篇文献的信息都包含在一个class为"document"的div中
    documents = soup.find_all("div", class_="document")
    
    # 遍历每篇文献并提取信息
    for doc in documents:
        # 提取文献标题
        title = doc.find("h2", class_="title").text.strip()
        
        # 提取文献作者
        authors = doc.find("p", class_="authors").text.strip()
        
        # 提取文献出版日期
        publication_date = doc.find("p", class_="publication_date").text.strip()
        
        # 提取文献摘要
        abstract = doc.find("div", class_="abstract").text.strip()
        
        # 输出文献信息
        print("标题:", title)
        print("作者:", authors)
        print("出版日期:", publication_date)
        print("摘要:", abstract)
        print("="*80)

else:
    print("Error: Unable to fetch the search results.")

