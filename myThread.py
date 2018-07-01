#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/19 0:18
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from PyQt4.QtCore import *

from DATA import sqlEdit

sql = sqlEdit.sqlEdit()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class add_item(QThread):
    signal = pyqtSignal(list)

    def __init__(self):
        super(add_item, self).__init__()
        self.selStr = str()

    @property
    def str_tree(self):
        return self.selStr

    @str_tree.setter
    def str_tree(self, selStr):
        self.selStr = selStr

    @str_tree.getter
    def str_tree(self):
        return self.selStr

    def run(self):
        self.parent().pageW.comboBoxNum.clear()
        message = self.parent().allSel[self.selStr] if self.parent().allSel.has_key(self.selStr) else list()
        num = message.__len__()

        pageNum = int(self.parent().pageW.spin.currentText())
        page = num / pageNum + 1
        self.parent().pageW.comboBoxNum.clear()
        self.parent().pageW.comboBoxNum.addItems([str(i) for i in range(1, page + 1)])

        self.signal.emit(message[0:pageNum])
