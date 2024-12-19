import requests
from bs4 import BeautifulSoup
import pandas as pd

import time
"""
废弃 按照关键词匹配 语法总出问题
按照新的抓取网页的固定元素进行提取
见
testgpt_qikan
和
testgpt_lunwen 
"""

# 基本设置
base_url = "https://vpn.cgl.org.cn/https/77726476706e69737468656265737421f6ef0f9f203c265f6c0fc7af96/s?sw=%E9%87%91%E7%9F%BF&strchannel=1%2C2&size=15&isort=0&x=642_243"  # 替换为实际的文献网站URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 
    # 'Accept-Encoding': 'gzip, deflate', 
    # 'Accept': '*/*', 
    # 'Connection': 'keep-alive', 
    'Cookie': 'wengine_vpn_ticketvpn_cgl_org_cn=f8d69f05720fcec0'
}

# 爬取每一页的文章列表
def fetch_articles(page):
    url = f"{base_url}&pages={page}"
    # print(url) 
    # headers 是一个预先定义的字典，通常包含用户代理信息等，用于模拟浏览器请求，以避免被目标服务器拒绝或识别为爬虫
    response = requests.get(url, headers=headers)
    # 确保如果请求失败（例如404未找到或500服务器错误），代码会抛出异常并停止执行。
    response.raise_for_status()
    # 将HTML代码作为函数的返回值，以便调用这个函数的代码可以进一步处理和解析HTML内容
    return response.text

# 爬取每篇文章的详细信息
def fetch_article_details(article_url):
    response = requests.get(article_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    
    # 提取作者，作者单位，期刊名，年份等信息
    # 以下代码需要根据具体页面的HTML结构进行调整
    try:
        title = soup.find("h4", class_="falv_tit").text.strip()
    except AttributeError:
        title = None
    # authors = [author.text.strip() for author in soup.find_all("span", class_="author-name")]
    # authors = [author.get_text(strip=True) for author in soup.find_all("a", href=True) if "author" in author['href']]
    # 获取作者
    try:
        authors = [author.get_text(strip=True) for author in soup.find_all("a", href=True) if "author" in author['href']]
    except AttributeError:
        authors = None
    # 获取作者单位
    try:
        author_affiliations = [aff.get_text(strip=True) for aff in soup.find_all("a", href=True) if "authorcompy" in aff['href']]
    except AttributeError:
        author_affiliations = None
    # 获取期刊名
    try:
        journal_name = soup.find("li", id="factorSpanId").find("a").get_text(strip=True)
    except AttributeError:
        journal_name = None
    # 获取年份 none
    try:
        year = soup.find("li", string=lambda x: x and "【年份】" in x).get_text(strip=True).replace("【年份】", "")
    except AttributeError:
        year = None
    # 获取卷号 none
    try:
        volume = soup.find("li", string=lambda x: x and "【卷号】" in x).get_text(strip=True).replace("【卷号】", "")
    except AttributeError:
        volume = None
    # 获取期号 none
    try:
        issue = soup.find("li", string=lambda x: x and "【期号】" in x).get_text(strip=True).replace("【期号】", "")
    except AttributeError:
        issue = None
    # 获取页码 none
    try:
        pages = soup.find("li", string=lambda x: x and "【页码】" in x).get_text(strip=True).replace("【页码】", "")
    except AttributeError:
        pages = None
    # 获取ISSN none
    try:
        issn = soup.find("li", string=lambda x: x and "【I S S N】" in x).get_text(strip=True).replace("【I S S N】", "")
    except AttributeError:
        issn = None
    # 获取关键词
    try:
        keywords = [kw.get_text(strip=True) for kw in soup.find_all("a", href=True) if "keyword" in kw['href']]
    except AttributeError:
        keywords = None
    # 获取摘要
    try:
        abstract = soup.find("li", id="detailSubAbstractId").get_text(strip=True).replace("【摘要】", "")
    except AttributeError:
        abstract = None
    # 获取基金
    try:
        fund = soup.find("li", string=lambda x: x and "【基金】" in x).get_text(strip=True).replace("【基金】", "")
    except AttributeError:
        fund = None
    # 获取重要收录
    try:
        important_inclusion = soup.find("li", string=lambda x: x and "【重要收录】" in x).get_text(strip=True).replace("【重要收录】", "")
    except AttributeError:
        important_inclusion = None
    # 获取文献类型
    try:
        document_type = soup.find("li", string=lambda x: x and "【文献类型】" in x).get_text(strip=True).replace("【文献类型】", "")
    except AttributeError:
        document_type = None
    url = article_url
    
    return {
        "title": title,
        "authors": authors,
        "author_affiliations": author_affiliations,
        "journal_name": journal_name,
        "year": year,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "issn": issn,
        "keywords": keywords,
        "abstract": abstract,
        "fund": fund,
        "important_inclusion": important_inclusion,
        "document_type": document_type,
        "url": url,
    }

# 主函数
def main():
    num_pages = 1  # 假设你想爬取5页的内容，可以调整
    all_articles = []
    
    for page in range(1, num_pages + 1):# 下次该52页了
        print(f"Fetching page {page}...")
        html = fetch_articles(page)
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        

        # # 找到每篇文章的链接（需要根据实际HTML结构调整）
        # article_links = [a['href'] for a in soup.select("li.biaoti a[target='_blank']")]
        # 获取带有 target='_blank' 的链接，并去除前导的斜杠
        article_links = [a['href'].lstrip('/') for a in soup.select("li.biaoti a[target='_blank']")]
        print(article_links)
        
        for link in article_links:
            full_link = f"https://vpn.cgl.org.cn/{link}"  # 替换为实际的URL拼接方法
            print(link)
            print(f"Fetching details for {full_link}...")
            details = fetch_article_details(full_link)
            all_articles.append(details)
        
        # time.sleep(1) # 暂停 1 秒

    # 打印结果或保存到文件 字典类型
    # for article in all_articles:
    #     print(article)

    # 创建一个DataFrame对象
    df = pd.DataFrame(all_articles)
    # 保存DataFrame到Excel文件
    df.to_excel('output/articles.xlsx', index=False)

# 控制主流程，遍历每一页，获取每篇文章的链接，并进一步爬取详细信息。
if __name__ == "__main__":
    main()
