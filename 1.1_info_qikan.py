import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import pandas as pd
from openpyxl import load_workbook
import os

# 需要修改的地方 1.(x, num_pages + 1)  2.'Cookie': 'wengine_vpn_ticketvpn_cgl_org_cn=x'

# 基本设置
base_url = "https://vpn.cgl.org.cn/https/77726476706e69737468656265737421f6ef0f9f203c265f6c0fc7af96/s?sw=%E9%87%91%E7%9F%BF&strchannel=1%2C2&size=15&isort=0&x=642_243"  # 替换为实际的文献网站URL
# base_url = "https://vpn.cgl.org.cn/https/77726476706e69737468656265737421f6ef0f9f203c265f6c0fc7af96/s?sw=%E9%87%91%E7%9F%BF&strchannel=1%2C2&size=50&isort=0&x=642_243"
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0', 
    
    # 'Accept-Encoding': 'gzip, deflate', 
    # 'Accept': '*/*', 
    # 'Connection': 'keep-alive', 
    'Cookie': 'wengine_vpn_ticketvpn_cgl_org_cn=0b2dab0582788538'
}

# 爬取每一页的文章列表
def fetch_articles(page):
    url = f"{base_url}&pages={page}"
    print(url) 
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

    # 初始化字典
    article_details = {
        "title": None,
        "authors": [],
        "affiliations": [],
        "journal": None,
        "year": None,
        "volume": None,
        "issue": None,
        "pages": None,
        "issn": None,
        "keywords": [],
        "classification": None,
        "subject_code": None,
        "abstract": None,
        "funding": None,
        "important_inclusions": None,
        "document_type": None,
        "url": None,
        "CNKI": None,
        "Weipu": None,
        "Weipu_Mirror": None,
        "Wenxian_Chuandi": None

    }
    
    # 提取作者，作者单位，期刊名，年份等信息
    # 以下代码需要根据具体页面的HTML结构进行调整
    # 查找包含所有信息的 div
    savelist_con = soup.find("div", class_="savelist_con")
    # 如果找不到 savelist_con 或 infolist，函数会直接返回一个空字典
    if not savelist_con:
        return article_details
    
    infolist = savelist_con.find("ul", class_="infolist")
    print("已获取到元素")
    if not infolist:
        return article_details


    # 提取每个 <li> 元素的内容
    for li in infolist.find_all("li"):
        em = li.find("em")
        if em:
            label = em.get_text(strip=True)
            content = li.get_text(strip=True).replace(label, "").strip()
            # print(f"{label}: {content}")
            if "作者】" in label:
                authors = []
                article_details["authors"] = content
            
            elif "作者单位" in label:
                affiliations = []
                article_details["affiliations"] = content

            elif "期刊名" in label:
                article_details["journal"] = content

            elif "年份" in label:
                article_details["year"] = content

            elif "卷号" in label:
                article_details["volume"] = content

            elif "期号" in label:
                article_details["issue"] = content

            elif "页码" in label:
                article_details["pages"] = content

            elif "I S S N" in label:
                article_details["issn"] = content

            elif "关键词" in label:
                keywords = []
                article_details["keywords"] = content

            elif "分类号" in label:
                article_details["classification"] = content

            elif "学科编号" in label:
                article_details["subject_code"] = content

            elif "摘要" in label:
                article_details["abstract"] = content

            elif "基金" in label:
                article_details["funding"] = content

            elif "重要收录" in label:
                article_details["important_inclusions"] = content

            elif "文献类型" in label:
                article_details["document_type"] = content
    
    try:
        article_details["title"] = soup.find("h4", class_="falv_tit").text.strip()
    except AttributeError:
        article_details["title"] = None
    article_details["url"] = article_url

## 查找四种下载方式的链接
    cnki_link = soup.find('a', string='CNKI(包库)')
    if cnki_link:
        article_details['CNKI'] = f"https://vpn.cgl.org.cn{cnki_link['href']}"
        # print(download_links['CNKI'])
    
    weipu_link = soup.find('a', string='维普')
    if weipu_link:
        article_details['Weipu'] = f"https://vpn.cgl.org.cn{weipu_link['href']}"

    weipu_mirror_link = soup.find('a', string='维普(镜像)')
    if weipu_mirror_link:
        article_details['Weipu_Mirror'] = f"https://vpn.cgl.org.cn{weipu_mirror_link['href']}"

    wenxian_chuandi_link = soup.find('a', string='文献传递')
    if wenxian_chuandi_link:
        article_details['Wenxian_Chuandi'] = f"https://vpn.cgl.org.cn{wenxian_chuandi_link['href']}"

    # 返回构造的字典
    return article_details

        
def merge_excel(file1, file2):

    # 读取第一个文件
    df1 = pd.read_excel(file1)
    # 读取第二个文件
    df2 = pd.read_excel(file2)
    # 按行合并两个文件 df1放最后
    result = pd.concat([df2, df1])
    # 将结果保存到新的Excel文件
    result.to_excel(file2, index=False)



# 主函数
def main():
    num_pages = 1000  # 假设你想爬取5页的内容，可以调整
    all_articles = []
    tag = 1
    # https://vpn.cgl.org.cn/https/77726476706e69737468656265737421f6ef0f9f203c265f6c0fc7af96/s?sw=%E9%87%91%E7%9F%BF&strchannel=1%2C2&size=15&isort=0&x=642_243&pages=313
    for page in range(1, num_pages + 1):# 下次该604  717
        print(f"Fetching page {page}...")
        html = fetch_articles(page)
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        
        # # 找到每篇文章的链接（需要根据实际HTML结构调整）
        # article_links = [a['href'] for a in soup.select("li.biaoti a[target='_blank']")]
        # 获取页面带有 target='_blank' 的链接，一页15篇，并去除前导的斜杠
        article_links = [a['href'].lstrip('/') for a in soup.select("li.biaoti a[target='_blank']")]

        # 第一页就访问失败, 还未手动验证
        if len(article_links) == 0:
            print(article_links) # 一页的link
            print("本次访问的第一页[预览页]就访问失败, 还未手动验证, 请先通过验证.")
            print(f"请访问以下链接进行手动验证：{base_url}&pages={page}")
            break
        
        for link in article_links:
            full_link = f"https://vpn.cgl.org.cn/{link}"  # 替换为实际的URL拼接方法

            # print(f"Fetching details for {full_link}...")
            details = fetch_article_details(full_link)
            
            if details['title'] is None:
                tag = 0
                print(f"请访问以下链接进行手动验证：{full_link}")
                break
            else:
                all_articles.append(details) 
        
        if tag == 0:
            print("############# 请先手动验证. #############")
            break
 
        # 增加随机延迟，避免被检测为爬虫
        time.sleep(random.uniform(5, 10))

        # time.sleep(1) # 暂停 1 秒

# 合并两个表格文件 将file1 文件中的内容合并到file2 文件
    # 创建一个DataFrame对象
    df = pd.DataFrame(all_articles)
    df.to_excel('output/qikan_part_1.xlsx', index=False) 
    # 合并文件
    file1 = 'output/qikan_part_1.xlsx'
    file2 = 'output/qikan_part_2.xlsx'
    merge_excel(file1, file2)
    print("信息已经保存到目录: output/qikan_part_2.xlsx")

# 控制主流程，遍历每一页，获取每篇文章的链接，并进一步爬取详细信息。
if __name__ == "__main__":
    main()