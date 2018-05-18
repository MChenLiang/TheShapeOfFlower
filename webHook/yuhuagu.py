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
import sys
import json
import urllib2
import requests
import multiprocessing
from random import randint
from bs4 import BeautifulSoup
from module import baseCommand as bcmds

import baseEnv

import DATA.sqlEdit as sqlEdit
import pinyinMaster.pinyin as py

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
reload(sys)
sys.setdefaultencoding("utf-8")

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
    sql = sqlEdit.sqlEdit()
    for each in getAllUrlStr():
        getMessage(each, sql)

    # sql = sqlEdit.sqlEdit
    # pool = multiprocessing.Pool()
    # for each in getAllUrlStr():
    #     pool.apply_async(getMessage, args=(each, sql,))
    # pool.close()
    # pool.join()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class getMessage(object):
    def __init__(self, http, sql=None):
        request = urllib2.Request(http)
        self.html = urllib2.urlopen(request)
        self.message = dict()
        self.sql = sql
        self.run()

    def run(self):
        for each in self.get_all_html():
            mDict = dict()
            request = urllib2.Request(each)
            html = urllib2.urlopen(request)

            bsObj = BeautifulSoup(html, "html.parser", from_encoding='GB2312')
            title = list(bsObj.find('h1').childGenerator())[0].title()

            for k in bsObj.body.find('ul', {'class': 'li'}).find_all('li'):
                contents = k.contents
                if not contents:
                    continue
                k, v = contents
                val = v.__dict__['contents']
                val = val[0] if val.__len__() else ''
                mDict.setdefault(k.decode('utf-8'), val.replace('"', "'"))

            mDict.setdefault(u'intro：', str(bsObj.find('p')).replace('"', "'"))

            for k in bsObj.body.find('div', {'class': 'wenz'}).find_all('p'):
                httpImagePath = k.contents[0].contents[0].attrs['src']
                _, fileName = os.path.split(httpImagePath)
                fileName = fileName.split(' ')[0]
                localFPath = os.path.join(dirP, title.split(' ')[0], fileName).replace('\\', '/')
                mDict.setdefault(u'image：', list()).append(localFPath)
                r = requests.get(httpImagePath, stream=True)

                # dir_p = os.path.dirname(localFPath)
                # os.path.exists(dir_p) or os.makedirs(dir_p)
                #
                # with open(localFPath, 'wb') as f:
                #     for chunk in r.iter_content(chunk_size=32):
                #         f.write(chunk)

            mDict.setdefault(u'image：', json.dumps(mDict.get(u'image：')))

            self.message.setdefault(title, mDict)
        #

        for (k, vs) in self.message.items():
            # kwargs = {'title':
            #   'chineseName':
            #   'spell':
            #   'otherName':
            #   'SName':
            #   'genera':
            #   'place':
            #   'description':
            #   'imagePath':}
            kwargs = {'title': k}
            try:
                for (i, v) in vs.items():
                    kwargs.setdefault(baseEnv.titleMatch[i], v)
            except :
                break
            else:
                kwargs.setdefault('spell',
                                  py.PinYin().hanzi2pinyin_split(str=kwargs.get('chineseName'),
                                                                 split=" "))
                kwargs.setdefault('typeG', '多肉植物;多肉植物->番杏科(Aizoaceae)')
                self.sql.insertItem(**kwargs)

    def get_all_html(self):
        bsObj = BeautifulSoup(self.html, "html.parser", from_encoding='GB2312')
        div = bsObj.find_all('div', {'id': 'pnavv'})
        return (each.find('a').attrs['href'] for each in div)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
    main()
