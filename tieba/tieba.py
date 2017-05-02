from bs4 import BeautifulSoup
import requests
import selenium.webdriver.support.ui as ui
from selenium import webdriver
import urllib.parse
import time
import json

tba = input('请输入贴吧名:')
m1 = str(input('请输入起始页数:'))
m2 = str(input('请输入页数,如果要抓取全部请输入max:'))

if m2 == 'max':
    text = requests.get('http://tieba.baidu.com/f/like/furank?kw=' + tba + '&ie=utf-8&pn=1').text
    s = BeautifulSoup(text, 'html.parser')
    js = json.loads(s.find('ul', {'class': 'p_rank_pager'}).attrs['data-field'])
    m2 = str(js['total_page'])
    print('\n' + '\n' + '=====排行榜共有' + m2 + '页，开始抓取=====' + '\n' + '\n')
else:
    print('\n' + '\n' + '=====抓取排行榜前' + m2 + '页，开始抓取=====' + '\n' + '\n')


def tieba(tb, minpage, maxpage):
    # url = 'http://tieba.baidu.com/f/like/furank?kw='+urllib.parse.quote(tb)+'&pn=2'
    # url = 'http://tieba.baidu.com/f/like/furank?kw=%C1%D6%D6%DD%D2%BB%D6%D0&pn=2'
    # url = 'http://tieba.baidu.com/f/like/furank?kw=%E6%9E%97%E5%B7%9E%E4%B8%80%E4%B8%AD&pn=2'
    tf = open(tb + m1 + '至' + m2 + '.txt', 'w', encoding='utf-8')
    for i in range(int(minpage), int(maxpage) + 1):
        url = 'http://tieba.baidu.com/f/like/furank?kw=' + tb + '&ie=utf-8&pn=' + str(i)
        try:
            result = requests.get(url)
            # print(r.text)
            sobj = BeautifulSoup(result.text, 'html.parser')
            tr = sobj.find_all('tr', {'class': 'drl_list_item'})
            for each in tr:
                nickname = each.find('a').text
                level = each.find('td', {'class': 'drl_item_title'}).find('div').attrs['class'][0][5:]
                exp = each.find('td', {'class': 'drl_item_exp'}).find('span').text
                print(nickname + '\t' + level + '\t' + exp)
                tf.write(nickname + '\t' + level + '\t' + exp + '\n')
        except:
            print(str(i) + '页' + '遭遇反爬')
            tf.write(str(i) + '页' + '遭遇反爬')
    tf.close()


tieba(tba, m1, m2)
print('\n' + '\n' + '=====排行榜抓取完毕，开始抓取用户个人信息，可能用时较长=====' + '\n' + '\n')
f = open(tba + m1 + '至' + m2 + '.txt', 'r', encoding='utf-8')
r = f.readlines()

driver = webdriver.PhantomJS(r'E:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
wait = ui.WebDriverWait(driver, 1)
for line in r:
    file = open(tba + m1 + '至' + m2 + 'user.txt', 'a', encoding='utf-8')
    nick = line.split('\t')[0]
    try:
        # t = user(nick)
        url = 'https://www.baidu.com/p/' + urllib.parse.quote(nick) + '?from=tieba'
        print(url)
        # url = 'https://www.baidu.com/p/YH%E5%9C%A81996?from=tieba'
        driver.get(url)
        time.sleep(1)
        ghtml = driver.page_source
        # print(ghtml)
        soup = BeautifulSoup(ghtml, 'html.parser')
        li = soup.find('ul', {'class': 'honor-list'}).find_all('li')
        for enum in li:
            title = enum.find('a').attrs['title']
            rank = enum.find('span').text
            print(title, rank)
            file.write(nick + '\t' + title + '\t' + rank + '\n')
    except AttributeError:
        try:
            # t = user(nick)
            url = 'https://www.baidu.com/p/' + urllib.parse.quote(nick) + '?from=tieba'
            print(url)
            # url = 'https://www.baidu.com/p/YH%E5%9C%A81996?from=tieba'
            driver.get(url)
            time.sleep(2)
            ghtml = driver.page_source
            # print(ghtml)
            soup = BeautifulSoup(ghtml, 'html.parser')
            li = soup.find('ul', {'class': 'honor-list'}).find_all('li')
            for enum in li:
                title = enum.find('a').attrs['title']
                rank = enum.find('span').text
                print(title, rank)
                file.write(nick + '\t' + title + '\t' + rank + '\n')

        except AttributeError:
            print('该用户隐藏了个人信息')
            file.write(nick + '\t' + '该用户隐藏了个人信息' + '\n')
    file.close()
f.close()
driver.quit()
