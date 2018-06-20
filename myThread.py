#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/19 0:18
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from DATA import sqlEdit


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class setItem(object):
    def __init__(self, mainC, beG, isUpdate=False):
        super(setItem, self).__init__()
        self.mainC = mainC
        self.beG = beG
        self.isUpdate = isUpdate

    def start(self):
        if self.isUpdate:
            sql = sqlEdit.sqlEdit()
            getItems = allItem = sql.queryItem(self.beG)
            self.mainC.imageDict.setdefault(self.beG, allItem)
        else:
            getItems = self.mainC.imageDict.get(self.beG)

        num = getItems.__len__()
        pageNum = int(self.mainC.pageW.spin.currentText())
        page = num / pageNum + 1
        self.mainC.pageW.comboBoxNum.clear()
        self.mainC.pageW.comboBoxNum.addItems([str(i) for i in range(1, page+1)])
        self.mainC.add_item(getItems[0:pageNum])

