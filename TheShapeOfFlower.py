#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Time     :  17:45
# Email    : spirit_az@foxmail.com
# File     : TheShapeOfFlower.py

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
__author__ = 'miaochenliang'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import os
import sys
import uuid
from functools import partial

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import baseEnv
import editConf
import initUI
import myThread
from DATA import typeEdit, sqlEdit
import existsUI as exUI
from MUtils import openUI as mUI
import editDialog
from collections import defaultdict

import chardet

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from UI import UI_succulentPlants

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
reload(initUI)
reload(UI_succulentPlants)
reload(typeEdit)
reload(editDialog)
reload(exUI)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import __init__

__start_path__ = __init__.__start_path__
_conf = editConf.conf()

__win_name__ = _conf.get(baseEnv.configuration, baseEnv.name)
__version__ = _conf.get(baseEnv.configuration, baseEnv.version)

sql = sqlEdit.sqlEdit()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def icon_path(in_name):
    return os.path.join(__start_path__, 'UI/icons', in_name).replace('\\', '/')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class openUI(QMainWindow):
    def __init__(self, parent=None):
        super(openUI, self).__init__(parent)
        self.UI()
        self.selTree = None
        self.allSel = defaultdict()
        self.imageDict = defaultdict()

    # UI log in +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def UI(self):
        self.pt = QWidget(self)
        self.win = UI_succulentPlants.Ui_Form()
        self.win.setupUi(self.pt)
        self.setCentralWidget(self.pt)

        self.setWindowTitle('{0}--{1}'.format(__win_name__, __version__))
        self.setObjectName(__win_name__)

        self.win.label_ID.hide()
        self.win.lineEdit_ID.hide()

        self.__init__ui__()
        self.bt_clicked()

    # connect +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def __init__ui__(self):
        self.setWindowIcon(QIcon(icon_path('window_icon.png')))
        self.init_asset_menu()
        widget_asset = self.win.widget_asset
        HBox = QHBoxLayout(widget_asset)
        HBox.setContentsMargins(0, 0, 0, 0)

        self.widget_other = initUI.list_ui(self)
        self.widget_other.initUI()
        HBox.addWidget(self.widget_other)

        self.objWidget = self.widget_other.objWidget
        self.pageW = self.objWidget.pageW

        # tree_asset
        tree_type = self.win.treeView_type
        self.type_model = QStandardItemModel(tree_type)
        tree_type.setModel(self.type_model)

        tree_type.header().setStretchLastSection(1)
        tree_type.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.default_type_model()

    def default_type_model(self):
        self.type_model.clear()
        self.type_model.setHorizontalHeaderLabels([u'分类'])
        dict_tree = typeEdit.xml_edit.getType()
        self.initType(dict_tree, self.type_model)

    def initType(self, dictTyp, pItem):
        if not dictTyp:
            return
        for (k, v) in dictTyp.items():
            item = QStandardItem(k)
            pItem.appendRow([item])
            self.initType(v, item)

    # connect +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def showLabel(self, obj, widget):
        geo_p = obj.parent().geometry()
        geo = obj.geometry()
        x, y, width, height = geo.x() + geo_p.x(), geo.y() + geo_p.y(), geo.width(), geo.height()
        widget.setGeometry(QRect(x + 300, y + 2, width, height))
        widget.setHidden(False)

    def hideLabel(self, widget):
        widget.setHidden(True)

    def bt_clicked(self):
        self.win.treeView_type.selectionModel().selectionChanged.connect(self.on_treeView_selectionChanged)
        self.pageW.comboBoxNum.activated.connect(self.on_page_comboBox_changed)
        all_pt = [self.pageW.minP, self.pageW.dnP, self.pageW.upP, self.pageW.maxP]
        for pt in all_pt:
            pt.clicked.connect(self.on_page_comboBox_changed)

    def on_page_comboBox_changed(self):
        page = int(self.pageW.comboBoxNum.currentText())
        num = int(self.pageW.spin.currentText())
        allImage = self.imageDict[self.selTree]
        tool = len(allImage)
        minNum = (page - 1) * num
        maxNum = page * num if tool > page * num else tool
        self.add_item(allImage[minNum:maxNum])

    def on_treeView_selectionChanged(self):
        selStr = self.get_selection_treeView()
        sys.stdout.write(selStr)
        if selStr not in self.allSel.keys():
            self.get_data(selStr)

        self.initPage(selStr)

    def get_data(self, selStr, isUpdata=True):
        if isUpdata:
            beG = """typeG like "%{0}%" """.format(selStr)
            data = sql.queryItem(beG) or list()
            self.allSel.setdefault(selStr, data)

    def initPage(self, selStr=''):
        if selStr and (not self.allSel.has_key(selStr)):
            self.pageW.comboBoxNum.clear()
            self.add_item(list())
        else:
            num = self.allSel[selStr].__len__()
            pageNum = int(self.pageW.spin.currentText())
            page = num / pageNum + 1
            self.pageW.comboBoxNum.clear()
            self.pageW.comboBoxNum.addItems([str(i) for i in range(1, page + 1)])
            self.add_item(self.allSel[selStr][0:pageNum])

    def get_selection_treeView(self):
        indexs = self.win.treeView_type.selectedIndexes()
        if not indexs:
            return False
        index = indexs[0]
        str_sel = index.data(0).toString()
        str_p = index.parent().data(0).toString()

        return u'{0}->{1}'.format(str_p, str_sel) if str_p else u"%s" % str_sel

    def get_selection_item(self):
        sel = [k for k in self.objWidget.Image_widget_list.values() if k.selected]
        if sel:
            return sel[0]
        else:
            return False

    def init_asset_menu(self):
        self.win.widget_asset.setContextMenuPolicy(Qt.CustomContextMenu)
        self.win.widget_asset.customContextMenuRequested.connect(self.show_asset_menu)

        self.asset_menu = QMenu(self)
        self.asset_menu.setStyleSheet(_conf.get(baseEnv.configuration, baseEnv.menu))
        add_item = QAction(u'| 添加', self, triggered=self.asset_add)
        # edit_item = QAction(u'| 编辑', self, triggered=self.asset_edit)
        del_item = QAction(u'| 删除', self, triggered=self.asset_del)

        self.asset_menu.addActions([add_item, del_item])

    def show_asset_menu(self, pos):
        self.asset_menu.exec_(QCursor().pos())

    def asset_add(self):
        selTreeView = self.get_selection_treeView()
        if not selTreeView:
            mUI.show_warning('Must Select one type!!!', 'W')
            return
        typeG = selTreeView
        splList = selTreeView.split('->')
        if splList.__len__() == 2:
            typeG = u';{}'.format(splList[0]) + typeG
        kwg = {'typeG': typeG,
               'ID': str(uuid.uuid1())}

        self.edDialog = editDialog.dialogItem(parent=self, conf='add', **kwg)
        if self.edDialog.exec_():
            self.updateSelTree_sql()

    def asset_edit(self):
        if not self.get_selection_item():
            mUI.show_warning('Please selected only one item!!!', 'w')
            return

    def asset_del(self):
        sel = self.get_selection_item()
        if not sel:
            mUI.show_warning('Please selected only one item!!!', 'w')
            return

        if not mUI.show_warning(u'Are you sure you want to delete {} ???'.format(sel.chineseName), 'a'):
            return
        else:
            sql.deleteItem('ID="%s"' % sel.id)
            self.updateSelTree_sql()
            print 'delect --- >> %s' % sel.chineseName

    def updateSelTree_sql(self):
        num = self.pageW.comboBoxNum.currentIndex()
        selStr = self.get_selection_treeView()
        self.get_data(selStr)
        self.initPage(selStr)
        maxCount = self.pageW.comboBoxNum.maxCount()
        num = num if num <= maxCount else maxCount
        self.pageW.comboBoxNum.setCurrentIndex(num)
        self.on_page_comboBox_changed()

    def setAllItem(self, sender):
        self.inP = sender
        self.all_item = list()
        sep = int(self.pageW.spin.currentText())
        allNum = self.all_item.__len__()
        page = allNum / sep + 1
        self.pageW.comboBoxNum.clear()
        self.pageW.comboBoxNum.addItems([str(i) for i in range(1, page + 1)])

    def setWidget(self):
        sep = int(self.pageW.spin.currentText())
        page = int(self.pageW.comboBoxNum.currentText())
        max_num = self.all_item.__len__()
        showItem = self.all_item[(page - 1) * sep: max_num if page * sep > max_num else page * sep]
        # self.add_item(showItem="")

    def add_item(self, messageList):
        widget = self.widget_other.objWidget
        widget.clearAll()

        for i in messageList:
            if widget.Image_widget_list.has_key(i[0]):
                wgt = widget.Image_widget_list[i[0]]
                wgt.update(*i)
            else:
                wgt = initUI.image_widget(*i)
                wgt.clicked[int].connect(partial(self.set_image, wgt))
                wgt.doubleClicked.connect(partial(self.dlgImage, wgt))
                widget.add_widget(wgt)
            wgt.show()

        widget.layout()

    def edit_item(self):
        wgt = initUI.image_widget.prevSelected
        if not wgt:
            return
        keys = ['ID', 'chineseName', 'spell', 'otherName', 'SName', 'genera', 'place',
                'description', 'imagePath', 'title', 'typeG']
        vals = wgt.args
        kwg = dict()
        for (k, v) in zip(keys, vals):
            kwg.setdefault(k, v)
        self.edDialog = editDialog.dialogItem(parent=self, conf='edit', **kwg)
        self.edDialog.exec_()

    def dlgImage(self, wgt):
        self.dlg = exUI.imageDialog(*wgt.imagePath)
        self.dlg.exec_()

    def set_image(self, wgt, conf):
        (ID, chineseName, spell, otherName, SName, genera, place,
         description, imagePath, title, typeG) = wgt.args
        if conf:
            self.win.label_title.setText(title)
            self.win.lineEdit_cName.setText(chineseName)
            self.win.lineEdit_spell.setText(spell)
            self.win.lineEdit_sOther.setText(otherName)
            self.win.lineEdit_lName.setText(SName)
            self.win.lineEdit_type.setText(genera)
            self.win.lineEdit_From.setText(place)
            self.win.lineEdit_ID.setText(ID)
            self.win.textEdit_intro.setText(description)
        else:
            self.win.label_title.setText(u'标题')
            lList = [self.win.lineEdit_cName, self.win.lineEdit_sOther, self.win.lineEdit_lName,
                     self.win.lineEdit_type, self.win.lineEdit_From, self.win.lineEdit_ID,
                     self.win.textEdit_intro]

            for each in lList:
                each.clear()


# main ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    anim_path = icon_path('waiting.gif')
    # 加载主程序
    Form = openUI()
    splash = exUI.mSplashScreen_new(anim_path, Qt.WindowStaysOnTopHint, Form)
    splash.show()
    # # 添加提示信息
    splash.showMessage('author : %s' % __author__, Qt.AlignLeft | Qt.AlignBottom, Qt.yellow)
    # Form.show()
    sys.exit(app.exec_())
