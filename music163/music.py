import utils
import json
import re
import requests
from bs4 import BeautifulSoup
from numpy import array

_163_URL = 'http://music.163.com/'


class Music:
    def __init__(self, mid, url=None, name=None, sen=None, comment=None, lrc=None):
        self._mid = mid
        self._url = url
        self._name = name
        self._sen = sen
        self._comment = comment
        self._html = utils.get_html('http://music.163.com/api/song/lyric?' + 'id=' + str(mid) + '&lv=1&kv=1&tv=-1')
        self._lrc = lrc

    @property
    def url(self):
        return _163_URL + '/song?id=' + str(self._mid)

    @property
    def name(self):
        pass

    @property
    def sen(self):
        # print(self.get_lyric())
        return utils.sen(self.lrc)

    @property
    def comment(self):
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % str(self._mid)
        data = {
            'params': 'vRlMDmFsdQgApSPW3Fuh93jGTi/ZN2hZ2MhdqMB503TZaIWYWujKWM4hAJnKoPdV7vMXi5GZX6iOa1aljfQwxnKsNT+5/uJKuxosmdhdBQxvX/uwXSOVdT+0RFcnSPtv',
            'encSecKey': '46fddcef9ca665289ff5a8888aa2d3b0490e94ccffe48332eca2d2a775ee932624afea7e95f321d8565fd9101a8fbc5a9cadbe07daa61a27d18e4eb214ff83ad301255722b154f3c1dd1364570c60e3f003e15515de7c6ede0ca6ca255e8e39788c2f72877f64bc68d29fac51d33103c181cad6b0a297fe13cd55aa67333e3e5'
        }
        headers = {
            'Referer': 'http://music.163.com',
        }
        r = utils.get_html(url, headers=headers, data=data)
        comment = json.loads(r)
        return comment['total']

    @property
    def lrc(self):
        lyric = json.loads(self._html)['lrc']['lyric']
        pat = re.compile(r'\[.*\]')
        lrc = re.sub(pat, "", lyric)
        lrc = lrc.strip()
        return lrc


class Artist:
    def __init__(self, uid, url=None, ):
        self._uid = uid
        self._url = url

    def name(self):
        pass

    @property
    def url(self):
        return _163_URL + 'artist?id=' + str(self._uid)

    @property
    def songs(self):
        r = requests.get(self.url)
        print(r)
        bs_obj = BeautifulSoup(r.text, 'lxml')
        t = bs_obj.find('textarea', {'style': "display:none;"})
        print(t)
        musics = json.loads(t.text)
        # name = musics[0]['artists']['name']
        ids = {}
        for music in musics:
            # music = json.loads(music)
            ids[music['name']] = music['id']
            yield music['id']


class Album:
    pass


#
# yzw = Artist(6066)
# print(yzw.url, )
# s = []
# for enum in yzw.songs:
#     s.append(Music(enum).sen)
#     # print()
# print(s)

data = array([0.12644816102849255, 0.9213855139683516, 0.94514489322052, 0.8528345687027243, 0.39207811713033325,
              0.8765359120295384, 0.88195770847653, 0.5607141433065496, 0.9116944050871821, 0.6057450011091527,
              0.4822985378947211, 0.3135552376758629, 0.9204015646889525, 0.9457894940595829, 0.4125163288077879,
              0.4145283718974274, 0.8286081639796427, 0.4371946988438363, 0.09729649215819869, 0.6668402915574165,
              0.8658020685040592, 0.8415878319649518, 0.9373301760610907, 0.5353664954029269, 0.41667233512410773,
              0.05278532445302586, 0.83125427513022, 0.2945805970997747, 0.10698624382389621, 0.13767427754553574,
              0.8796406082362036, 0.7464466190083463, 0.32267611205090263, 0.7879122667783454, 0.759416136937956,
              0.563812452252972, 0.49288202797276703, 0.265481558617078, 0.9546237842266501, 0.09588016471763605,
              0.1024078013550499, 0.780972370024567, 0.12980253574922263, 0.9891249119391636, 0.9268214108249151,
              0.9765706861285026, 0.9652573104081659, 0.47819573124097026, 0.4914091847208979, 0.6658230754151282])
from matplotlib import pyplot


# 绘制直方图
def drawHist(heights):
    # 创建直方图
    # 第一个参数为待绘制的定量数据，不同于定性数据，这里并没有事先进行频数统计
    # 第二个参数为划分的区间个数
    pyplot.hist(heights, 50)
    pyplot.xlabel(u'sen')
    pyplot.ylabel(u'count')
    pyplot.title(u'TOP50 music sen')
    pyplot.show()


drawHist(data)

# music = Music(25788001)
# print(music.sen, music.lrc, music.comment)
