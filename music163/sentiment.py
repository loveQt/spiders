import json
import requests
import os
import glob

SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
headers = {'X-Token': 'wEHUNeJc.4429.hI8qB_gVitpx'}


# resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
# resp = json.loads(resp.text)
# print(resp)

def sen_from_text(file_path):
    inputFile = open(file_path, "r+", encoding='utf-8').read()
    data = json.dumps(inputFile)
    resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    resp = json.loads(resp.text)
    front = float(resp[0][0])
    return front

# s = []
# dir_path = '.\\5781'
# for txtFile in glob.glob(os.path.join(dir_path, "*.txt")):
#     inputFile = open(txtFile, "r+", encoding='utf-8').read()
#     data = json.dumps(inputFile)
#     resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
#     resp = json.loads(resp.text)
#     front = float(resp[0][0])
#     if front <= 0.4:
#         flag = -1
#         sen = '负面'
#     elif front > 0.4 and front <= 0.6:
#         flag = 0
#         sen = '中性'
#     elif front > 0.6:
#         flag = 1
#         sen = '正面'
#     print(txtFile, sen, front)
# s.append(inputFile)

# s = ['他是个傻逼', '美好的世界']
# data = json.dumps(inputFile)
# resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
# resp = json.loads(resp.text)
# print(resp)

# print(resp.text)
