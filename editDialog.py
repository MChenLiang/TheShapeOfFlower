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

from __init__ import __start_path__

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
            widget.id = imagePath

            self.Image_widget_list.setdefault(str(widget.id), widget)
            self.createContextMenu(widget)
            self.set_item_size(self.slider.value())
            widget.show()

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
        self.verticalLayout_3.addWidget(self.image_widget)

        if self.conf == 'edit':
            self.initUI_edit()
        elif self.conf == 'add':
            self.initUI_add()

        self.image_widget.layout()

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
                        'title': self.label_title}

        [temp_dict_bt[each].setText(self.kwargs[each]) for each in temp_dict_bt.keys() if self.kwargs.has_key(each)]
        self.typeG = self.kwargs.get('typeG')
        for each in self.kwargs.get('imagePath').split(';'):
            self.image_widget.add_widget(
                os.path.join(__start_path__, 'DATA/Image', self.kwargs.get('title'), each).replace('\\', '/'))

    def get_label(self, title):
        base_path = (each.__in_path__ for each in self.image_widget.Image_widget_list.values())
        all_image_path = ';'.join(u'{}'.format(os.path.split(each)[-1]) for each in base_path)

        dir_path = u'%s' % os.path.join(__start_path__, 'DATA/Image', title).replace('\\', '/')

        os.path.exists(dir_path) or os.makedirs(dir_path)

        for ser in base_path:
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
                     'title': str(self.label_title.text()),
                     'imagePath': self.get_label(str(self.label_title.text())),
                     'typeG': self.typeG}

        return temp_dict

    def submit_sql(self, **kwargs):
        if self.conf == 'add':
            sql.insertItem(**kwargs)
        elif self.conf == 'edit':
            sql.updateItem('ID="{}"'.format(kwargs.get('ID')), **kwargs)
            pass

        for (k, v) in kwargs.items():
            print '\t\t', k, '-->>', v

    def accept(self):
        temp_dict = self.get_message()
        self.submit_sql(**temp_dict)
        super(dialogItem, self).accept()


if __name__ == '__main__':
    app = QApplication([])
    Form = dialogItem(conf='add', typeG='tst', ID='1dfasfdg')
    # Form = image_widget()
    Form.show()
    app.exec_()
