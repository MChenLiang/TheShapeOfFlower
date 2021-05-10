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
import psutil
from collections import defaultdict
from functools import partial

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import find_ui
import baseEnv
import editConf
import editDialog
import existsUI as exUI
import initUI
import myThread
from DATA import typeEdit, sqlEdit
from MUtils import openUI as mUI
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from UI import UI_succulentPlants

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
reload(initUI)
reload(UI_succulentPlants)
reload(typeEdit)
reload(editDialog)
reload(exUI)
reload(sqlEdit)
reload(myThread)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import __init__

__start_path__ = __init__.__start_path__
_conf = editConf.conf()

__win_name__ = _conf.get(baseEnv.configuration, baseEnv.name)
__version__ = _conf.get(baseEnv.configuration, baseEnv.version)

sql = sqlEdit.sqlEdit()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
__init__._main()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def icon_path(in_name):
    return os.path.join(__start_path__, 'UI/icons', in_name).replace('\\', '/')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class openUI(QMainWindow):
    keyword = None

    def __init__(self, parent=None):
        super(openUI, self).__init__(parent)

        self.UI()
        self.allSel = defaultdict()
        self.t = myThread.add_item()
        self.t.setParent(self)

        self.t.signal.connect(self.add_items)

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
        self.add_tray()

    # connect +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def __init__ui__(self):
        self.setWindowIcon(QIcon(icon_path('window_icon.ico')))
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

    # alp +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def showLabel(self, obj, widget):
        geo_p = obj.parent().geometry()
        geo = obj.geometry()
        x, y, width, height = geo.x() + geo_p.x(), geo.y() + geo_p.y(), geo.width(), geo.height()
        widget.setGeometry(QRect(x + 300, y, width, height))
        widget.setHidden(False)

    def hideLabel(self, widget):
        widget.setHidden(True)

    # connect +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def bt_clicked(self):
        self.win.treeView_type.selectionModel().selectionChanged.connect(self.on_treeView_selectionChanged)
        self.pageW.comboBoxNum.activated.connect(self.on_page_comboBox_changed)
        all_pt = [self.pageW.minP, self.pageW.dnP, self.pageW.upP, self.pageW.maxP]
        for pt in all_pt:
            pt.clicked.connect(self.on_page_comboBox_changed)

    def on_page_comboBox_changed(self):
        page = int(self.pageW.comboBoxNum.currentText())
        num = int(self.pageW.spin.currentText())
        allImage = self.allSel[self.get_selection_treeView()]
        tool = len(allImage)
        minNum = (page - 1) * num
        maxNum = page * num if tool > page * num else tool
        self.add_items(allImage[minNum:maxNum])

    def on_treeView_selectionChanged(self):
        selStr = self.get_selection_treeView()
        if selStr not in self.allSel.keys():
            self.get_data(selStr)
        self.t.str_tree = selStr
        self.t.run()

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

    def add_items(self, messageList):
        widget = self.widget_other.objWidget
        widget.clearAll()
        map(lambda x: self.add_item(x), messageList)
        widget.layout()

    def add_item(self, i):
        if self.widget_other.objWidget.Image_widget_list.has_key(i[0]):
            wgt = self.widget_other.objWidget.Image_widget_list[i[0]]
            wgt.update(*i)
        else:
            wgt = initUI.image_widget(*i)
            wgt.clicked[int].connect(partial(self.set_image, wgt))
            wgt.doubleClicked.connect(partial(self.dlgImage, wgt))
            self.widget_other.objWidget.add_widget(wgt)
        wgt.show()

    # edit image plane and sql data +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def get_data(self, selStr):
        beG = u'typeG like "%{}%" '.format(selStr)
        self.allSel[selStr] = sql.queryItem(beG) or list()
        if self.keyword and self.keyword != 'search':
            self.allSel[selStr] = [each for each in self.allSel[selStr] if self.keyword in each[2]]

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
            mUI.show_warning(u'添加成功！！！', 's')

    def asset_edit(self):
        if not self.get_selection_item():
            mUI.show_warning('Please selected only one item!!!', 'w')
            return
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
        if self.edDialog.exec_():
            self.updateSelTree_sql()
            mUI.show_warning(u'编辑成功！！！', 's')

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
            mUI.show_warning(u'删除成功 ： \n\t %s' % sel.chineseName, 's')

    def updateSelTree_sql(self):
        num = self.pageW.comboBoxNum.currentIndex()
        selStr = self.get_selection_treeView()
        self.get_data(selStr)
        self.t.str_tree = selStr
        self.t.run()
        maxCount = self.pageW.comboBoxNum.maxCount()
        num = num if num <= maxCount else maxCount
        self.pageW.comboBoxNum.setCurrentIndex(num)
        self.on_page_comboBox_changed()

    def setAllItem(self, sender):
        self.inP = sender
        self.keyword = self.inP.objectName().split('_')[-1].toLower()
        selStr = self.get_selection_treeView()
        if not selStr:
            return
        self.get_data(selStr)
        self.t.str_tree = selStr
        self.t.run()

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

    # add tray ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def add_tray(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(icon_path('window_icon.png')))
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.trayClick)
        self.trayMenu()

    def trayClick(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

        elif reason == QSystemTrayIcon.MiddleClick:
            self.showMessage()
        else:
            pass

    def showMessage(self):
        icon = QSystemTrayIcon.Information
        in_text = 'soft :{}\r\n'.format(__win_name__)
        in_text += 'version : {}\r\n'.format(__version__)
        in_text += 'author : {}\r\n'.format(__author__)
        self.trayIcon.showMessage('introduce : ', in_text, icon)

    def trayMenu(self):

        img_main = QIcon(icon_path('window_icon.ico'))
        img_min = QIcon(icon_path('min_in.png'))
        img_exit = QIcon(icon_path('del_in.png'))

        self.trayIcon.setToolTip('{0}--{1}'.format(__win_name__, __version__))

        self.restoreAction = QAction(img_main, __win_name__, self)
        self.minAction = QAction(img_min, "Minimize", self)
        self.quitAction = QAction(img_exit, "Exit", self)

        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.minAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)

        self.restoreAction.triggered.connect(self.max_action)
        self.minAction.triggered.connect(self.min_action)
        self.quitAction.triggered.connect(self.exit_action)

    def min_action(self):
        self.showMinimized()

    def max_action(self):
        self.actions()
        self.showNormal()

    def exit_action(self):
        self.trayIcon.deleteLater()
        self.deleteLater()


# main ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
    current_proc = psutil.Process()
    # create_lnk.create_all_lnk(os.getcwd())
    if current_proc.name() == 'python.exe':
        pass

    else:
        if '192.168' in current_proc.exe():
            current_proc.kill()
        for proc in psutil.process_iter():
            if proc.name() != current_proc.name():
                continue
            if proc.pid != current_proc.pid:
                find_ui.delete_ui('QMainWindow', __win_name__)

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
