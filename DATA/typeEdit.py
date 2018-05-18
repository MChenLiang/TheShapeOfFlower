#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/6 23:31
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

from ImageTyp import xml_read, xml_write
reload(xml_write)
reload(xml_read)


class xml_edit(object):
    @classmethod
    def addType(cls, typeName):
        mxml = xml_write.xml_edit()
        mxml.addType(typeName=typeName)

    @classmethod
    def getType(cls):
        mxml = xml_read.xml_edit()
        return mxml.get_all()

