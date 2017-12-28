from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from pyquery import PyQuery as pq
import pymongo
from config import *

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
browser=webdriver.Chrome()
wait = WebDriverWait(browser,10)

def search():
    try:
        browser.get('https://www.taobao.com')
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORDS)
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        print('正在翻页',page_number)
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        return next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        result={
            'img':item.find('.pic .img').attr('src'),
            'title':item.find('.title').text(),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(result)
        save_to_mongodb(result)

def save_to_mongodb(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存至MONGODB成功')
    except Exception:
        print('保存至MONGODB失败')

def main():
    try:
        total=search()
        total=int(re.compile('(\d+)',re.S).search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('出现错误')
    finally:
        browser.close()

if __name__=='__main__':
    main()






