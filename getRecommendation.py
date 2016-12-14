from collections import defaultdict
from bs4 import BeautifulSoup
import json
from time import sleep
import requests
from logger import LoggerHelper
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
mylog = LoggerHelper.init_logger('main', log_fullname='recfail')


def spider(rec, num):
    l = {}
    try:
        for i in range(num):
            mylog.info(i)
            flag = True
            menu = browser.find_element_by_xpath(
                "//a[contains(@index, '" + str(i + 1) + "')]")
            ActionChains(browser).click(menu).perform()
            sleep(1.5)

            page = browser.page_source
            soup = BeautifulSoup(page, 'lxml')
            tags = soup.select(".tag_price")
            for i in tags:
                mylog.info(i.string)
                if i.string.strip() == '無庫存':
                    flag = False
                    break
            if len(tags) < 2:
                flag = False
            if flag:
                tags = soup.select(".tag_name")
                l['items'] = [i['item'][:-1] for i in tags]
                l['image'] = soup.find(class_="cboxPhoto")['src']
                l['category'] = category
                mylog.info(l)
                p.append(l.copy())

            closeBut = browser.find_element_by_id('cboxClose')
            ActionChains(browser).click(closeBut).perform()
            sleep(1)
    except Exception as e:
        mylog.error(i + 1)
        mylog.error(e)

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('http://www.lativ.com.tw/STYLE/')
    category = ['men', 'women', 'sports']
    rec = []
    for cat in category:
        mylog.info(cat)
        menu = browser.find_element_by_class_name(cat)
        ActionChains(browser).click(menu).perform()
        sleep(1)
        pageSource = browser.page_source
        soup = BeautifulSoup(pageSource, 'lxml')
        num = len(soup.select('.cboxElement'))

        spider(rec, num)

    browser.close()
    with open('rec.json', 'w')as f:
        json.dump(p, f, sort_keys=True, indent=4, ensure_ascii=False)
