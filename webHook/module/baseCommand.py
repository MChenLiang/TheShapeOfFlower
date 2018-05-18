#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/4 23:58
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def agent():
    ie = r"""safari 5.1 – Windows
Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50
IE 9.0
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;)
IE 8.0
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)
IE 7.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
IE 6.0
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
Firefox 4.0.1 – Windows
Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1
Opera 11.11 – Windows
Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11
傲游（Maxthon）
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)
腾讯TT
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)
世界之窗（The World） 2.x
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)
世界之窗（The World） 3.x
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)
搜狗浏览器 1.x
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)
360浏览器
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)
Avant
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)
Green Browser
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)
    """
    return ie.split('\n')[1::2]
