#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/6 23:31
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

try:
    from xml.etree import CElementTree as eTree
except ImportError:
    from xml.etree import ElementTree as eTree

import os
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


class xml_edit(object):
    xml_path = os.path.join(os.path.dirname(__file__), 'type.xml').replace('\\', '/')

    def __init__(self):
        parse = eTree.parse(self.xml_path)
        self.root = parse.getroot()

    def __get_all(self, doc, listT, p_name=''):
        for k in doc:
            name = k.attrib['name']
            listT.append(p_name + name)
            self.__get_all(k, listT, '%s>' % (p_name + name))

    def get_all(self):
        dictTyp = dict()
        tempList = list()
        self.__get_all(self.root, tempList)
        for each in tempList:
            self.__set_dict(dictTyp, each.split('>'))
        return dictTyp

    def __set_dict(self, dictTyp, listSpl):
        if listSpl.__len__() == 1:
            dictTyp.setdefault(listSpl[0], dict())
        else:
            k, vs = listSpl[0], listSpl[1:]
            dictTyp.setdefault(k, self.__set_dict(dictTyp[k], vs))


if __name__ == '__main__':
    mxml = xml_edit()
    print mxml.get_all()

