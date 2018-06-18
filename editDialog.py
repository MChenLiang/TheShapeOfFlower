#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/6/16 21:48
# @email : spirit_az@foxmail.com

__author__ = 'miaochenliang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
from UI import editItemDialog

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pinyinMaster import spellChiness

from MUtils import openUI

from DATA import sqlEdit

from baseFunction import baseFunc

import initUI

import sip

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
reload(editItemDialog)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
sql = sqlEdit.sqlEdit()
bFc = baseFunc()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class editItem(QDialog, editItemDialog.Ui_Dialog):
    def __init__(self, conf='edit', parent=None, **kwargs):
        super(editItem, self).__init__(parent)
        self.conf = conf
        self.setWindowTitle(self.conf)
        self.kwg = kwargs
        self.setupUi(self)
        self.resize(900, 600)
        self.VLay = QVBoxLayout(self.frame_asset)

        self.imageP = ''
        self.typG = ''

        self.btDict = {'id': self.lineEdit_ID,
                       'chineseName': self.lineEdit_cName,
                       'spell': self.lineEdit_spell,
                       'otherName': self.lineEdit_sOther,
                       'SName': self.lineEdit_lName,
                       'genera': self.lineEdit_type,
                       'place': self.lineEdit_From,
                       'description': self.textEdit_intro,
                       'title': self.label_title
                       }
        self.otList = {self.typG: 'typeG', self.imageP: 'imagePath'}
        # keys = ['id', 'chineseName', 'spell', 'otherName', 'SName', 'genera', 'place', 'description', 'imagePath', 'title', 'typeG']

        self.init_ui()

    def init_ui(self):
        # keys = ['id', 'chineseName', 'spell', 'otherName', 'SName', 'genera', 'place', 'description', 'imagePath', 'title', 'typeG']
        # vals = [self.kwg[each] for each in keys]
        # self.picture_frame.setParent(self)
        if self.conf == 'edit':
            for (k, v) in self.kwg.items():
                self.btDict.has_key(k) and self.btDict[k].setText(v)

            self.imageP = self.kwg['imagePath']
            self.typG = self.kwg['typeG']

            for each in self.imageP.split(';'):
                self.addImage(each)

                # self.VLay.addWidget(self.picture_frame)

    def edit_item(self):
        pass

    def addImage(self, image):
        pushbutton = QPushButton(self)
        pushbutton.image = image

        # self.addAttr(pushbutton, image=image)
        pushbutton.setIcon(QIcon(image))
        pushbutton.setFlat(True)
        pushbutton.setIconSize(QSize(120, 120))
        pushbutton.setFixedSize(QSize(120, 120))
        pushbutton.setStyleSheet('QPushButton{border:none;}')
        pushbutton.setChecked(True)
        pushbutton.setObjectName(image)
        # label = QLabel(self)
        # label.setPixmap(QPixmap(image))
        # label.setFixedSize(80, 80)
        pushbutton.clicked.connect(self.showImage)
        self.VLay.addWidget(pushbutton)

    def showImage(self):
        print self.sender().image
        print 'show'

    def delImage(self, objLabel):
        objLabel.deleteLater()

    def accept(self):
        self.cName = list(str(self.lineEdit_cName.text()).decode('utf-8').strip())
        self.spell = str(self.lineEdit_spell.text()).rstrip().lstrip()
        while '  ' in self.spell:
            self.spell.replace('  ', ' ')
        self.spell = self.spell.split(' ')

        # print u'中文名称 ： ', self.cName
        # print u'中文拼音 ： ', self.spell

        if len(self.cName) != len(self.spell):
            openUI.show_warning(u'拼音的个数和中文名对不上！！！', 'e')
            return
        self.write_spell()
        self.write_sql()
        super(editItem, self).accept()
        print '提交数据库'

    def reject(self):
        super(editItem, self).reject()
        print 'pass'

    def write_spell(self):
        self.ct = spellChiness.connect()
        self.ct.write(**{k: [v] for (k, v) in zip(self.cName, self.spell)})

    def write_sql(self):
        idStr = 'ID="%s"' % str(self.lineEdit_ID.text())
        dictTemp = dict()
        for (k, v) in self.btDict.items():
            try:
                v = v if isinstance(v, str) else str(v.text())
            except:
                v = str(v.toPlainText())
            finally:
                dictTemp.setdefault('spell', ' '.join(self.spell))

            dictTemp.setdefault(k, v)

            # print dictTemp['typeG']
        if sql.queryItem(idStr):
            sql.updateItem(idStr, **dictTemp)
        else:
            sql.insertItem(**dictTemp)


class image_widget(QScrollArea):

    def __init__(self, **kwargs):
        super(image_widget, self).__init__(**kwargs)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)

        self.all_image = list()

        widget = QWidget(self)
        self.setWidget(widget)

        self.VLay = QVBoxLayout(widget)

    def add_label(self, image_path):
        # print image_path
        # if image_widget not in self.all_image:

        self.all_image.append(image_widget)
        label = QLabel(self)
        label.setFixedSize(60, 60)
        label.setScaledContents(True)
        label.setPixmap(QPixmap(image_path))
        self.VLay.addWidget(label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(image_widget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(image_widget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # 遍历输出拖动进来的所有文件路径
            allFilePath = (str(url.toLocalFile()).decode('UTF-8') for url in event.mimeData().urls())
            for each in allFilePath:
                if os.path.isfile(each):
                    self.add_label(each)
                else:
                    map(lambda x: self.add_label(x), self.getAllImage(each))

            event.acceptProposedAction()
        else:
            super(image_widget, self).dropEvent(event)

    def getAllImage(self, inPath):
        return bFc.getListDirK(inPath, 'file', '(.jpg)|(.png)|(.jpeg)')


class dialogItem(QDialog, editItemDialog.Ui_Dialog):
    def __init__(self, conf='edit', **kwargs):
        super(dialogItem, self).__init__(**kwargs)

        self.conf = conf

        self.setupUi(self)
        self.setWindowTitle(conf)

        self.image_widget = image_widget(parent=self)
        # VLay = QVBoxLayout(self.frame_asset)
        self.verticalLayout_3.addWidget(self.image_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.image_widget.setSizePolicy(sizePolicy)

        # self.frame_asset

        if conf == 'edit':
            self.edit_item()

        elif conf == 'add':
            self.add_item()

    def run(self):
        chiness = self.lineEdit_cName.text()
        spell = self.lineEdit_spell.text()
        other = self.lineEdit_sOther.text()
        lName = self.lineEdit_lName.text()
        typ = self.lineEdit_type.text()
        place = self.lineEdit_From.text()
        ID = self.lineEdit_ID.text()
        intro = self.textEdit_intro.toPlainText()

    def get_label(self):
        all_label = [each.text() for each in self.image_widget.children() if isinstance(each, QLabel)]

        all_image_path = ';'.join(os.path.split(each) for each in self.image_widget.all_image)

    def add_item(self):
        pass

    def edit_item(self, **kwargs):
        pass

    def submit_sql(self):

        pass


if __name__ == '__main__':
    app = QApplication([])
    Form = dialogItem(conf='add')
    # Form = image_widget()
    Form.show()
    app.exec_()
