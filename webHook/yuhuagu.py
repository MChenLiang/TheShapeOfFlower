#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/5 13:51
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
"""
<meta http-equiv="Content-Type" content="text/html;charset=GB2312" />

Request URL:http://www.yuhuagu.com/fanxingke/
Request Method:GET
Status Code:200 OK (from disk cache)
Remote Address:121.40.39.177:80
Referrer Policy:no-referrer-when-downgrade

Content-Encoding:gzip
Content-Type:text/html
Server: nginx
Content-Length: 16233
Connection: close
Vary: Accept-Encoding
Accept-Ranges: bytes

Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
"""
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
import re
import sys
import json
import urllib2
import requests
import multiprocessing
from random import randint
from bs4 import BeautifulSoup
from module import baseCommand as bcmds

import baseEnv

# 数据库的链接封装 这里要改成自己的数据库
import DATA.sqlEdit as sqlEdit
import pinyinMaster.spellChiness as spellChiness

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
reload(sys)
sys.setdefaultencoding('UTF-8')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
all_agent = bcmds.agent()

dirP = os.path.join(os.path.os.path.dirname(os.path.dirname(__file__)), 'DATA/Image').replace('\\', '/')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def getAllUrlStr():
    mainHttp = 'http://www.yuhuagu.com/fanxingke'
    request = urllib2.Request(mainHttp)
    html = urllib2.urlopen(request, data=all_agent[randint(0, all_agent.__len__() - 1)])

    bsObj = BeautifulSoup(html, "html.parser", from_encoding='GB2312')
    pageItem = list(bsObj.find('span', {"class": "pageinfo"}).childGenerator())[1]
    page = int(pageItem.childGenerator().next())

    http = 'http://www.yuhuagu.com/fanxingke/list_63432_{}.html'
    for i in range(1, page + 1):
        yield http.format(i)


def main():
    """sqlite3 不支持多线程或多进程。"""
    sql = sqlEdit.sqlEdit()  # 数据库的实例
    # sql = None
    for each in getAllUrlStr():
        getMessage(each, sql)
        # break

    # 下面为多进程的网页爬取
    # sql = sqlEdit.sqlEdit
    # pool = multiprocessing.Pool()
    # for each in getAllUrlStr():
    #     pool.apply_async(getMessage, args=(each, sql,))
    # pool.close()
    # pool.join()


def download_image(httpImagePath, localFPath):
    r = requests.get(httpImagePath, stream=True)

    dir_p = os.path.dirname(localFPath)
    os.path.exists(dir_p) or os.makedirs(dir_p)

    with open(localFPath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class getMessage(object):
    def __init__(self, http, sql=None):
        request = urllib2.Request(http)
        self.html = urllib2.urlopen(request)
        self.message = dict()
        self.sql = sql
        self.run()

    def run(self):

        all_dict = dict()
        for each in self.get_all_html():
            temp_dict = dict()
            request = urllib2.Request(each)
            html = urllib2.urlopen(request)

            bsObj = BeautifulSoup(html, "html.parser", from_encoding='')
            body = bsObj.body.find('div', {'id': 'in_l'})

            title = bsObj.h1.children.next()
            all_dict.setdefault(title, temp_dict)
            v_list = list()
            for k in body.find('ul', {'class': 'li'}).find_all('li'):
                contents = k.contents
                if not contents:
                    continue
                k, v = contents
                val = v.__dict__['contents']
                val = val[0] if val.__len__() else ''

                v_list.append(val)

            temp_dict.setdefault('chineseName', v_list[0])
            temp_dict.setdefault('spell', spellChiness.connect().split(' ', *v_list[0]))
            temp_dict.setdefault('otherName', v_list[1])
            temp_dict.setdefault('SName', v_list[2])
            temp_dict.setdefault('genera', v_list[3])
            temp_dict.setdefault('place', v_list[4])
            temp_dict.setdefault('typeG', u'多肉植物;多肉植物->番杏科(Aizoaceae)')

            intro = body.find('p').children.next()
            temp_dict.setdefault('description', intro)

            all_http_image = ';'.join([k.find('a').contents[0].attrs['src'] for k in
                                       body.find('div', {'class': 'wenz'}).find_all('p')])

            temp_dict.setdefault('imagePath', all_http_image)

        for (k, v) in all_dict.items():
            http_image = v.get('imagePath').split(';')
            map(lambda x: download_image(x, os.path.join(dirP, k, os.path.split(x)[-1])), http_image)

            # image_f = ';'.join(os.path.split(each)[-1] for each in http_image)
            #
            # v.setdefault('title', k)
            # v.pop('imagePath')
            # v.setdefault('imagePath', image_f)
            # self.sql.insertItem(**v)

    def get_all_html(self):
        bsObj = BeautifulSoup(self.html, "html.parser", from_encoding='GB2312')
        div = bsObj.find_all('div', {'id': 'pnavv'})
        return (each.find('a').attrs['href'] for each in div)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
    main()
