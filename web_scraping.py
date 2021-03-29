# shopee.py
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
import pandas as pd

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=2')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)
timeout = 10
katakunci = input('Masukkan kata kunci : ')

def search(katakunci):
    links = []
    print('mencari semua product dengan kata kunci ' + katakunci)
    url = 'https://shopee.co.id/search?keyword=' + katakunci
    try:
        driver.get(url)
        time.sleep(5)
        driver.execute_script('window.scrollTo(0, 1500);')
        time.sleep(5)
        driver.execute_script('window.scrollTo(0, 2500);')
        time.sleep(5)
        soup_a = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup_a.find('div', class_='row shopee-search-item-result__items')
        for link in products.find_all('a'):
            links.append(link.get('href'))
            print(link.get('href'))
    except TimeoutException:
        print('failed to get links with query ')
    return links

def get_product(produt_url):
    try:
        url = 'https://shopee.co.id' + produt_url
        driver.get(url)
        time.sleep(3)
        driver.execute_script('window.scrollTo(0, 1500);')
        time.sleep(3)
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'attM6y')))
        soup_b = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup_b.find('div', class_='attM6y').text
        price = soup_b.find('div', class_='_3e_UQT').text
        ongkir = soup_b.find('div', class_='flex items-center deQMhv').text
        # print(price)
        # exit()
        # try:
        #     image = soup_b.find('div', class_='_2JMB9h _3XaILN')['style']
        #     imgurl = re.findall('url\((.*?)\)', image)
        # except:
        #     imgurl = 'none'
        # desc = soup_b.find('div', class_='_2u0jt9').text
        print('Scraping ' + title)
        return title, price, ongkir


        # kita simpan hasil scraping ke file sresult.csv
        # with open('sresult.csv','a', encoding='utf-8',newline='') as f:
        #     fieldnames = ['Judul', 'Harga']
        #     writer=csv.writer(f)
        #     # writer.writerow([title,price,url,desc,imgurl])
        #     # writer.writerow([title,price,url])
        #     writer.writerow([title, price])
        #     # for row in csv.reader(f):
            #     writer.writerow(row+[price])

    except TimeoutException:
        print('cant open the link')

product_urls = search(katakunci)
judul = []
harga = []
ongkos = []
temp_judul=[]
temp_harga=[]
df1 = pd.DataFrame()
df2 = pd.DataFrame()
for product_url in product_urls:
    temp_judul, temp_harga, temp_ongkir = get_product(product_url)
    judul.append(temp_judul)
    harga.append(temp_harga)
    ongkos.append(temp_ongkir)


dict = {'Judul': judul, 'Harga': harga, 'Ongkir': ongkos}
df = pd.DataFrame(dict)
# df1 = df1.append(pd.DataFrame(judul, columns = ['Judul']))
# df2 = df2.append(pd.DataFrame(harga, columns = ['Harga']))
#
# df1.insert(1, 'Harga', df2.values)

print(df.head())
# header = ["Judul", "Harga"]
df.to_csv("hasil_scraping.csv", header=False, index=False)


# with open('results.csv', 'a', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     # writer.writerow([title,price,url,desc,imgurl])
#     # writer.writerow([title,price,url])
#     writer.writerow([judul, harga])