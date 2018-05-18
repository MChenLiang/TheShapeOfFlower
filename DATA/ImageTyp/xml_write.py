#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2018/5/6 23:31
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

try:
    from xml.etree import CElementTree as eTree
except ImportError:
    from xml.etree import ElementTree as eTree

import os
import sys
import time
import numpy as np
from xml.dom import minidom

import envSpecification as env

reload(sys)

sys.setdefaultencoding('utf-8')


class xml_edit(object):
    xml_path = os.path.join(os.path.dirname(__file__), 'type.xml').replace('\\', '/')

    def __init__(self):
        if not os.path.exists(self.xml_path):
            self.doc = minidom.Document()
            self.root = self.doc.createElement(env.XML_ROOT_TYPE)
            self.root.setAttribute('data', str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            self.root.setAttribute('author', __author__)
            self.doc.appendChild(self.root)
            self.dictTyp = {
                '观叶盆栽': {},
                '观花植物': {'月季花图片': {}, '天竺葵图片': {}},
                '水生花卉': {},
                '球根花卉': {},
                '多肉植物': {'番杏科(Aizoaceae)': {}, '景天科(Crassulaceae)': {}, '仙人掌类': {}},
                '菊科植物': {},
                '藤本植物': {},
                '盆景图片': {},
                '兰科植物': {},
                '宿根花卉': {},
                '常绿花木': {},
                '蕨类植物': {},
                '一二年生花卉': {},
                '看图识花': {}
            }
            self.getDoc(self.dictTyp, self.root)
        else:
            self.doc = minidom.parse(self.xml_path)
            self.root = self.doc._get_firstChild()

    def addType(self, typeName):
        splitType = typeName.split('>')

        if len(splitType) == 2:
            typ, genera = splitType
        else:
            typ = splitType[0]
            genera = None

        np_array = np.array(map(lambda x: (x, x.getAttribute('name')), self.get_all_cl(self.doc)))

        typName, typDocs = np_array[:, 0], np_array[:, 1]

        if typ not in typName:
            typDoc = self.doc.createElement(env.XML_IMAGE_TYPE)
            print type(typ)
            typDoc.setAttribute('name', typ)
            self.root.appendChild(typDoc)
        else:
            typDoc = typDocs[typName.index(typ)]

        if genera:
            generaName = [each.tagName for each in self.get_all_cl(typDoc)]
            if genera not in generaName:
                generaDoc = self.doc.createElement(env.XML_FAMILY_TYPE)
                generaDoc.setAttribute('name', generaName)

        self.write()

    def get_all_cl(self, doc):
        return doc.childNodes

    def getDoc(self, dictMess, parentDoc):
        xml_type = env.XML_IMAGE_TYPE if self.root == parentDoc else env.XML_FAMILY_TYPE
        for (k, vDicts) in dictMess.items():
            kDoc = self.doc.createElement(xml_type)
            kDoc.setAttribute('name', k)
            parentDoc.appendChild(kDoc)
            if isinstance(vDicts, dict):
                self.getDoc(vDicts, kDoc)

    def write(self):
        with open(self.xml_path, 'w') as f:
            self.doc.writexml(f, '\t', '\t', '\n', encoding='utf-8')


if __name__ == '__main__':
    mxml = xml_edit()
    mxml.write()
