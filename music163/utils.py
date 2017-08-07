import os
import glob
import re
import json
import requests
import time
from bs4 import BeautifulSoup


def merge_text(dir_path, outputFileName):
    # 如果dir不是目录返回错误
    if not os.path.isdir(dir_path):
        print("传入的参数有错%s不是一个目录" % dir_path)
        return False
    # list all txt files in dir
    outputFile = open(outputFileName, "wb+")
    for txtFile in glob.glob(os.path.join(dir_path, "*.txt")):
        print(txtFile)
        inputFile = open(txtFile, "rb")
        for line in inputFile:
            outputFile.write(line)
    return True


def get_html(url, headers=None, data=None):
    return requests.post(url, headers=headers, data=data).text


def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()


def timestamp_to_datetime(d):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d))


def sen(text):
    SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
    headers = {'X-Token': 'wEHUNeJc.4429.hI8qB_gVitpx'}
    data = json.dumps(text)
    resp = requests.post(SENTIMENT_URL, headers=headers, data=data)
    resp = json.loads(resp.text)
    # print(resp)
    return resp[0][0]
