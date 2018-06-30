#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/6/16 21:48
# @email : spirit_az@foxmail.com

__author__ = 'miaochenliang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import initUI
from DATA import sqlEdit
from MUtils import openUI
from UI import editItemDialog
from __init__ import __start_path__
from baseFunction import baseFunc
from pinyinMaster import spellChiness

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
reload(editItemDialog)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
sql = sqlEdit.sqlEdit()
bFc = baseFunc()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class image_frame(initUI.picture_prev):
    def __init__(self, *args):
        super(image_frame, self).__init__(*args)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(image_frame, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(image_frame, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # 遍历输出拖动进来的所有文件路径
            allFilePath = (str(url.toLocalFile()).decode('UTF-8') for url in event.mimeData().urls())
            for each in allFilePath:
                if os.path.isfile(each):
                    self.add_widget(each)
                else:
                    map(lambda x: self.add_widget(x), self.getAllImage(each))

            event.acceptProposedAction()
        else:
            super(image_frame, self).dropEvent(event)

    def add_widget(self, imagePath):
        if os.path.isfile(imagePath):
            widget = initUI.image_widget(parent=self.item_area)
            widget.set_in_path(imagePath)
            widget.ID = imagePath

            self.Image_widget_list.setdefault(str(widget.id), widget)
            self.createContextMenu(widget)
            self.set_item_size(self.slider.value())
            widget.show()

            widget.doubleClicked.connect(self.image_doubleClicked)

    def image_doubleClicked(self):
        wgt = self.sender()
        print wgt.__in_path__

    def getAllImage(self, inPath):
        return bFc.getListDirK(inPath, 'file', '(.jpg)|(.png)|(.jpeg)')

    def createContextMenu(self, widget):
        widget.setContextMenuPolicy(Qt.CustomContextMenu)
        widget.customContextMenuRequested.connect(self.showContextMenu)

        # create menu
        self.contextMenu = QMenu(self)

        self.editAction = QAction(u'| 删除', self)
        self.contextMenu.addAction(self.editAction)

        self.editAction.triggered.connect(self.remove_item)

    def remove_item(self):
        wgt = initUI.image_widget.prevSelected
        if not wgt:
            return
        self.clear_item(wgt)


class dialogItem(QDialog, editItemDialog.Ui_Dialog):

    def __init__(self, parent=None, conf='edit', **kwargs):
        super(dialogItem, self).__init__(parent)

        self.setupUi(self)

        self.conf, self.kwargs, self.typeG = conf, kwargs, None

        self.image_widget = image_frame(self)
        self.horizontalLayout.addWidget(self.image_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_widget.sizePolicy().hasHeightForWidth())
        self.image_widget.setSizePolicy(sizePolicy)
        self.image_widget.setMinimumWidth(460)

        if self.conf == 'edit':
            self.initUI_edit()
        elif self.conf == 'add':
            self.initUI_add()

    def initUI_add(self):
        self.typeG = self.kwargs.get('typeG')
        self.lineEdit_ID.setText(self.kwargs.get('ID'))

    def initUI_edit(self):
        temp_dict_bt = {'chineseName': self.lineEdit_cName,
                        'spell': self.lineEdit_spell,
                        'otherName': self.lineEdit_sOther,
                        'SName': self.lineEdit_lName,
                        'genera': self.lineEdit_type,
                        'place': self.lineEdit_From,
                        'ID': self.lineEdit_ID,
                        'description': self.textEdit_intro,
                        'title': self.lineEdit_title}

        [temp_dict_bt[each].setText(self.kwargs[each]) for each in temp_dict_bt.keys() if self.kwargs.has_key(each)]
        self.typeG = self.kwargs.get('typeG')
        for each in self.kwargs.get('imagePath').split(';'):
            self.image_widget.add_widget(
                u'%s' % os.path.join(__start_path__, 'DATA/Image', self.kwargs.get('title'), each).replace('\\', '/'))

    def get_label(self, title):
        base_path = [each.__in_path__ for each in self.image_widget.Image_widget_list.values()]
        all_image_path = ';'.join(u'{}'.format(os.path.split(each)[-1]) for each in base_path)

        dir_path = u'%s' % os.path.join(__start_path__, 'DATA/Image', title).replace('\\', '/')

        os.path.exists(dir_path) or os.makedirs(dir_path)

        had = [os.path.normcase(os.path.join(dir_path, each)) for each in bFc.getListDir(dir_path, 'file')]
        for ser in base_path:
            if os.path.normcase(ser) in had:
                continue
            bFc.moveFileto(ser, dir_path)

        return all_image_path

    def get_message(self):
        temp_dict = {'chineseName': str(self.lineEdit_cName.text()),
                     'spell': str(self.lineEdit_spell.text()),
                     'otherName': str(self.lineEdit_sOther.text()),
                     'SName': str(self.lineEdit_lName.text()),
                     'genera': str(self.lineEdit_type.text()),
                     'place': str(self.lineEdit_From.text()),
                     'ID': str(self.lineEdit_ID.text()),
                     'description': str(self.textEdit_intro.toPlainText()),
                     'title': str(self.lineEdit_title.text()),
                     'imagePath': self.get_label(str(self.lineEdit_title.text())),
                     'typeG': self.typeG}

        return temp_dict

    def write_spell(self):
        self.ct = spellChiness.connect()
        self.ct.write(**{k: [v] for (k, v) in zip(self.cName, self.spell)})

    def submit_sql(self, **kwargs):
        if self.conf == 'add':
            sql.insertItem(**kwargs)
        elif self.conf == 'edit':
            sql.updateItem('ID="{}"'.format(kwargs.get('ID')), **kwargs)

        for (k, v) in kwargs.items():
            print '\t\t', k, '-->>', v

    def accept(self):
        self.cName = list(str(self.lineEdit_cName.text()).decode('utf-8').strip())
        self.spell = str(self.lineEdit_spell.text()).rstrip().lstrip()
        while '  ' in self.spell:
            self.spell.replace('  ', ' ')
        self.spell = self.spell.split(' ')

        if len(self.cName) != len(self.spell):
            openUI.show_warning(u'拼音的个数和中文名对不上！！！', 'e')
            return
        self.write_spell()

        temp_dict = self.get_message()
        self.submit_sql(**temp_dict)
        super(dialogItem, self).accept()

    def show(self):
        super(dialogItem, self).show()


if __name__ == '__main__':
    app = QApplication([])
    Form = dialogItem(conf='add', typeG='tst', ID='1dfasfdg')
    # Form = image_widget()
    Form.show()
    app.exec_()
