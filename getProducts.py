from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import json
from time import sleep


def category_list(target):
    r = requests.get('http://www.lativ.com.tw/' + target)
    soup = BeautifulSoup(r.text, 'lxml')
    c = defaultdict(list)
    c = {}
    for i in soup.select('.category_sub'):
        category = i.h2.string.strip()  # 大類
        c[category] = {}
        links = i.select('a')
        for j in links:
            c[category][j['title']] = j['href']
    return c


def style_list(c, target):
    style = defaultdict(str)
    for cat in c.keys():
        for subcat in c[cat]:

            r = requests.get('http://www.lativ.com.tw' + c[cat][subcat])
            soup = BeautifulSoup(r.text, 'lxml')
            patterns = soup.select('.list_display')
            for j in patterns:
                pattern = j.previous_sibling.previous_sibling.a.string.strip()
                products = j.find_all('li')
                for i in products:
                    styleNo = i.a.img['data-prodpic'].split('/')[4]
                    if not style[styleNo]:
                        style[styleNo] = {'name': i.find(class_='productname').string.strip(),
                                          'price': int(i.select(".currency")[-1].string.strip()),
                                          'pattern': pattern,
                                          'subcat': subcat,
                                          'category': cat,
                                          'target': target,
                                          'store': 'lativ'
                                          }
    return style


def color_product(l, check_style, style, sec):
    pop_list = []
    for styleNo in check_style:
        # session=requests.Session()
        # re=session.get('http://www.lativ.com.tw/Detail/28139011')
        sleep(sec)
        r = requests.get(
            'http://www.lativ.com.tw/Product/ProductInfo/?styleNo=' + styleNo, allow_redirects=False)
        if r.status_code != 200:
            continue
        samestyle = json.loads(r.json()['info'])

        for j in samestyle:
            l.append({
                'link': '/Detail/' + j['ItemList'][0]['sn'],
                'id': j['ItemList'][0]['sn'][:-1],
                'color': j['color'],
                'thumb': j['ItemList'][0]['img280'],
                'size': [i['size'] for i in j['ItemList']],
                'styleNo': styleNo,
                'img': ''})
        model(samestyle[0]['ItemList'][0]['sn'], style)
        pop_list.append(styleNo)
    for i in pop_list:
        check_style.remove(i)


def model(pid, style):
    r = requests.get('http://www.lativ.com.tw/Detail/' +
                     pid, allow_redirects=False)
    # sleep(0.5)
    if r.status_code != 200:
        style[pid]['img'] = r.status_code
        return
    soup = BeautifulSoup(r.text, 'lxml')
    pics = soup.select(".oldPic")
    if pics:
        pics = pics[0].select("img")
    else:
        style[pid]['img'] = -1
        return
    if len(pics) > 2:
        pics = pics[:2]
    elif len(pics) == 0:
        style[pid]['img'] = []
        return
    style[pid[:-3]]['img'] = [j["data-original"] for j in pics]


if __name__ == '__main__':
    target = 'MEN'
    category_url_lists = category_list(target)
    style = style_list(category_url_lists, target.lower())

    products = []
    check_style = list(style.keys())

    # api不穩，要重複多次
    for _ in range(5):
        color_product(products, check_style, style, 1)

    with open('style.json', 'w')as f:
        json.dump(style, f, sort_keys=True, indent=4, ensure_ascii=False)

    with open('products.json', 'w')as g:
        json.dump(products, g, sort_keys=True, indent=4, ensure_ascii=False)
