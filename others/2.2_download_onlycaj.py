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

# 读取Excel文件中的CNKI下载列
def read_urls_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df['CNKI'].tolist()



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
        caj_download_button = WebDriverWait(driver, 5).until(
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
    input_file_path = 'output/articles_qikan.xlsx'  # 替换为实际的输入文件路径

    urls = read_urls_from_excel(input_file_path)

    for url in urls:
        print(f"Visiting CNKI link: {url}")
        download_caj_from_cnki(url)

        # 增加随机延迟，避免被检测为爬虫
        # time.sleep(random.uniform(20, 35))

# 基本设置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0', 
    'Cookie': 'wengine_vpn_ticketvpn_cgl_org_cn=c3a1b09351bf455e'
}

# 控制主流程
if __name__ == "__main__":
    main()
