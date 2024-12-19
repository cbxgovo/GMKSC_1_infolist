import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver import Edge
from selenium.webdriver.chrome.options import Options
from pywinauto import Desktop,Application
import time

import pyautogui

# 读取Excel文件中的URL列
def read_urls_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df['url'].tolist()

# 解析页面，获取下载链接
def fetch_download_links(article_url):
    response = requests.get(article_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 初始化下载链接字典
    download_links = {
        "CNKI": None,
        "Weipu": None,
        "Weipu_Mirror": None,
        "Wenxian_Chuandi": None
    }

    # 查找四种下载方式的链接
    cnki_link = soup.find('a', string='CNKI(包库)')
    if cnki_link:
        download_links['CNKI'] = f"https://vpn.cgl.org.cn{cnki_link['href']}"
        print(download_links['CNKI'])
    
    weipu_link = soup.find('a', string='维普')
    if weipu_link:
        download_links['Weipu'] = f"https://vpn.cgl.org.cn{weipu_link['href']}"

    weipu_mirror_link = soup.find('a', string='维普(镜像)')
    if weipu_mirror_link:
        download_links['Weipu_Mirror'] = f"https://vpn.cgl.org.cn{weipu_mirror_link['href']}"

    wenxian_chuandi_link = soup.find('a', string='文献传递')
    if wenxian_chuandi_link:
        download_links['Wenxian_Chuandi'] = f"https://vpn.cgl.org.cn{wenxian_chuandi_link['href']}"

    return download_links

# 访问CNKI(包库)链接并点击CAJ下载按钮
def download_caj_from_cnki(cnki_url):
    # 设置Edge浏览器驱动路径
    edge_driver_path = 'D:\b_installenv\edgedriver_win64\msedgedriver.exe'
    # 创建Edge浏览器对象，并连接到已有的调试端口
    options = webdriver.EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Edge(options=options)

    # 打开给定的网址链接
    url = cnki_url  # 替换为你要打开的网址
    driver.get(url)

    try:
       
        # 等待"CAJ下载"按钮可点击并点击
        caj_download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'CAJ下载'))
        )
        caj_download_button.click()
        # time.sleep(random.uniform(15, 20))

        # 可以进行下载操作或其他操作...

    finally:
        # 关闭浏览器
        driver.quit()

# 主函数
def main():
    input_file_path = 'output/articles2_qikan.xlsx'  # 替换为实际的输入文件路径
    output_file_path = 'output/articles2_qikan_download_links.xlsx'  # 替换为实际的输出文件路径

    urls = read_urls_from_excel(input_file_path)
    all_links = []

    for url in urls:
        print(f"Fetching download links for {url}...")
        links = fetch_download_links(url)
        links['url'] = url  # 将原始URL也加入结果中
        all_links.append(links)

        # 按优先级访问下载链接
        if links['CNKI']:
            print(f"Visiting CNKI link: {links['CNKI']}")
            download_caj_from_cnki(links['CNKI'])
            # time.sleep(random.uniform(10, 30))
        elif links['Weipu']:
            print(f"Visiting Weipu link: {links['Weipu']}")
            # 可扩展处理Weipu的下载逻辑
        elif links['Weipu_Mirror']:
            print(f"Visiting Weipu Mirror link: {links['Weipu_Mirror']}")
            # 可扩展处理Weipu Mirror的下载逻辑
        elif links['Wenxian_Chuandi']:
            print(f"Visiting Wenxian Chuandi link: {links['Wenxian_Chuandi']}")
            # 可扩展处理Wenxian Chuandi的下载逻辑

        # 增加随机延迟，避免被检测为爬虫
        # time.sleep(random.uniform(20, 35))

    # 创建一个DataFrame对象
    df = pd.DataFrame(all_links)
    # 保存DataFrame到Excel文件 所有可以下载的链接
    df.to_excel(output_file_path, index=False)

# 基本设置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0', 
    'Cookie': 'wengine_vpn_ticketvpn_cgl_org_cn=21e05f96cbbf824e'
}

# 控制主流程
if __name__ == "__main__":
    main()
