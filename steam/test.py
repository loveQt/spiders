import requests
from bs4 import BeautifulSoup
import json


def sen_from_text(text):
    SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
    h = {'X-Token': 'wEHUNeJc.4429.hI8qB_gVitpx'}
    data = json.dumps(text)
    resp = requests.post(SENTIMENT_URL, headers=h, data=data.encode('utf-8'))
    resp = json.loads(resp.text)
    # print(resp)
    front = float(resp[0][0])
    return front


headers = {
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}
file = open('steam.txt', 'w+', encoding='utf-8')

for i in range(1, 6):
    url = 'http://steamcommunity.com/app/433850/homecontent/?userreviewsoffset=' + str(10 * (i - 1)) + '&p=' + str(
        i) + '&workshopitemspage=' + str(i) + '&readytouseitemspage=' + str(i) + '&mtxitemspage=' + str(
        i) + '&itemspage=' + str(i) + '&screenshotspage=' + str(i) + '&videospage=' + str(i) + '&artpage=' + str(
        i) + '&allguidepage=' + str(i) + '&webguidepage=' + str(i) + '&integratedguidepage=' + str(
        i) + '&discussionspage=' + str(
        i) + '&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=433850&appHubSubSection=10&l=schinese&filterLanguage=default&searchText=&forceanon=1'
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')  # 如果装了lxml，推荐把解析器改为lxml
    reviews = soup.find_all('div', {'class': 'apphub_Card'})
    for review in reviews:
        nick = review.find('div', {'class': 'apphub_CardContentAuthorName'})
        title = review.find('div', {'class': 'title'}).text
        hour = review.find('div', {'class': 'hours'}).text.split(' ')[0]
        link = nick.find('a').attrs['href']
        comment = review.find('div', {'class': 'apphub_CardTextContent'}).text.split('\n')[3].strip('\t')
        sen = sen_from_text(comment)
        # print(nick.text, title, hour, link, )

        file.write(
            nick.text + '\t' + title + '\t' + str(sen) + '\t' + hour + '\t' + link + '\t' + comment + '\n')
file.close()
