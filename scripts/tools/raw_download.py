import sys
import os
import wget
import time
import requests

libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
rawdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'raw')


def download():
    try:
        down_data = []
        with open(os.path.join(libdir, 'data_record.txt'), 'r', encoding='UTF-8') as f:
            for line in f:
                temp = line.strip('\n')
                if(len(temp) > 0):
                    down_data.append(temp)
        down_lenth = len(down_data)
        rawdata = []
        with open(os.path.join(libdir, 'metadata.txt'), 'r', encoding='UTF-8') as f:
            for line in f:
                temp = line.strip('\n')
                if temp.startswith('!') or temp.startswith('[R]') \
                        or temp.startswith('[M]') or len(temp) == 0:
                    continue
                else:
                    rawdata.append(temp.strip('[+]').strip('[P]').strip('[M]'))
        raw_lenth = len(rawdata)
        for i in range(0, raw_lenth):
            if os.path.exists(os.path.join(rawdir, rawdata[i])):
                os.remove(os.path.join(rawdir, rawdata[i]))
            else:
                continue
        for i in range(0, down_lenth):
            down_txt = wget.download(down_data[i], rawdir)
        return 1

    except Exception as e:
        return 0


def isConnected():
    try:
        html = requests.get("https://www.baidu.com", timeout=5)
    except:
        return False
    return True

# remove raw data


def clean_raw_data():
    for items in os.listdir(rawdir):
        if (not 'mobile' in items) and (not 'raw' in items) and (not 'white' in items):
            os.remove(os.path.join(rawdir, items))
