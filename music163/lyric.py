import re
import requests
import json
from bs4 import BeautifulSoup
import os
from utils import merge_text
import sentiment
from src.SegWordFreq import *


def download_lyric_by_music_id(mid):
    url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(mid) + '&lv=1&kv=1&tv=-1'
    # print(mid)
    try:
        lyric = json.loads(requests.post(url).text)['lrc']['lyric']
    except KeyError:
        lyric = '无歌词'
    pat = re.compile(r'\[.*\]')
    lrc = re.sub(pat, "", lyric)
    lrc = lrc.strip()
    return lrc


# print(download_lyric_by_music_id(25788001))


def get_music_ids_by_id(uid):
    url = 'http://music.163.com/artist?id=' + str(uid)
    r = requests.get(url).text
    bs_obj = BeautifulSoup(r, 'lxml')
    t = bs_obj.find('textarea',{'style':"display:none;"})
    print(t.text)
    musics = json.loads(t.text )# .replace('(', '[').replace(')', ']').replace('\'', '"'))

    # name = musics[0]['artists']['name']
    ids = {}
    for music in musics:
        # music = json.loads(music)
        ids[music['name']] = music['id']
    return ids
    # return t.text


def get_music_comment_count(mid):
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % str(mid)
    data = {
        'params': 'vRlMDmFsdQgApSPW3Fuh93jGTi/ZN2hZ2MhdqMB503TZaIWYWujKWM4hAJnKoPdV7vMXi5GZX6iOa1aljfQwxnKsNT+5/uJKuxosmdhdBQxvX/uwXSOVdT+0RFcnSPtv',
        'encSecKey': '46fddcef9ca665289ff5a8888aa2d3b0490e94ccffe48332eca2d2a775ee932624afea7e95f321d8565fd9101a8fbc5a9cadbe07daa61a27d18e4eb214ff83ad301255722b154f3c1dd1364570c60e3f003e15515de7c6ede0ca6ca255e8e39788c2f72877f64bc68d29fac51d33103c181cad6b0a297fe13cd55aa67333e3e5'
    }
    headers = {
        'Referer': 'http://music.163.com',
    }

    r = requests.post(url, headers=headers, data=data)
    comment = json.loads(r.text)
    return comment['total']


def download_lyric(uid):
    try:
        os.mkdir(str(uid))
    except IOError:
        pass
    music_ids = get_music_ids_by_id(uid)
    for key in music_ids:
        # key = key.replace('/', '／').replace('\\', '＼')
        text = download_lyric_by_music_id(music_ids[key])
        file = open(str(uid) + '\\' + key.replace('/', '／').replace('\\', '＼') + '.txt', 'a', encoding='utf-8')
        file.write(key + '\n')
        file.write(text)
        file.close()


# print(get_music_ids_by_id(6066))
# print(get_music_comment_count(25788001))
# music = get_music_ids_by_id(6066)
# for key in music:
#     print(key, '\\', get_music_comment_count(music[key]))
def one_click(aid):
    download_lyric(aid)
    merge_text(os.getcwd() + '\\' + str(aid), 'data/' + str(aid) + 'merge.txt')
    print(sentiment.sen_from_text('data/' + str(aid) + 'merge.txt'))
    file = 'data/' + str(aid) + 'merge'
    print("分词开始")
    file_seg(in_filename,
             out_filename,
             str_splitTag)
    print("分词完成")

    print("计算词频开始")
    word_freq(corpus_path,
              stop_words_path,
              freq_path)
    print("计算词频完成")


# one_click(1024308)

print(get_music_ids_by_id(1195028))
