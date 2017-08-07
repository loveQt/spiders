import requests
import json
# 找入口，从哪里抓取数据
import re


def download_by_music_id(music_id):
    # lrc_url = 'http://music.163.com/weapi/song/lyric?csrf_token='
    lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(music_id) + '&lv=1&kv=1&tv=-1'

    # url = 'http://music.163.com/#/song?id=468517654'
    r = requests.get(lrc_url)
    json_obj = r.text

    j = json.loads(json_obj)

    lrc = j['lrc']['lyric']
    pat = re.compile(r'\[.*\]')
    lrc = re.sub(pat, "", lrc)
    lrc = lrc.strip()
    return lrc


print(download_by_music_id(25788001))
