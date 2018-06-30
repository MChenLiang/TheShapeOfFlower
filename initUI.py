#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Time     :  23:46
# Email    : spirit_az@foxmail.com
# File     : initUI.py
__author__ = 'ChenLiang.Miao'
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import math
import os
import sys
from functools import partial

from PyQt4.QtCore import *
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from PyQt4.QtGui import *

import __init__
import baseEnv
import editConf

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
pushbutton_qss = editConf.conf().get(baseEnv.qss, baseEnv.button)
H_slider = editConf.conf().get(baseEnv.qss, baseEnv.H_slider)
comboBox = editConf.conf().get(baseEnv.qss, baseEnv.comboBox)
__start_path__ = __init__.__start_path__
_conf = editConf.conf()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def icon_path(in_name):
    return u'%s' % os.path.join(__start_path__, 'UI/icons', in_name).replace('\\', '/')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class list_ui(QWidget):
    _root_win = None
    grp_dict, pt_dict = dict(), dict()

    def __init__(self, parent):
        super(list_ui, self).__init__(parent)
        self.p = parent
        self.args = eval(_conf.get(baseEnv.configuration, baseEnv.alphabet))

    def initUI(self):
        HLay = QHBoxLayout(self)
        HLay.setContentsMargins(0, 0, 0, 0)

        self.widget_alp = QWidget(self.p)
        HLay.addWidget(self.widget_alp)
        self.widget_alp.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        VLay_alp = QVBoxLayout(self.widget_alp)
        VLay_alp.setContentsMargins(0, 0, 0, 0)
        VLay_alp.setSpacing(3)
        spacerItem_up = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        VLay_alp.addItem(spacerItem_up)

        self.search_b = search_button(self.p)
        self.pt_dict.setdefault('search', self.search_b)
        VLay_alp.addWidget(self.search_b)
        for each in self.args:
            pt = self.pushButton(each)
            self.pt_dict.setdefault(each, pt)
            VLay_alp.addWidget(pt)

        spacerItem_dn = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        VLay_alp.addItem(spacerItem_dn)

        self.objWidget = picture_prev(self)
        HLay.addWidget(self.objWidget)

        self.bt_clicked()

    def bt_clicked(self):
        [each.clicked.connect(self.bt_alp_clicked) for each in self.pt_dict.values()]

    def bt_alp_clicked(self):
        for each in self.pt_dict.values():
            each.setChecked(False)
        self.sender().setChecked(True)
        self.p.setAllItem(self.sender())

    def edit_item(self):
        self.p.asset_edit()

    def del_item(self):
        self.p.asset_del()

    def pushButton(self, name):
        button = asset_button(self.setLabelShow, self.setLabelHide)
        button.setText(name)
        button.widget.text = name
        button.setObjectName('pushButton_{}'.format(name))
        button.setParent(self.p)
        button.widget.setParent(self.p)
        return button

    def groupBox(self, name):
        grpbox = QGroupBox(self.p)
        grpbox.setTitle(name)
        grpbox.setFlat(True)
        grpbox.setObjectName('groupBox_{}'.format(name))
        VLay = QVBoxLayout(grpbox)
        VLay.setContentsMargins(0, 0, 0, 0)
        VLay.setSpacing(0)
        return grpbox

    def setLabelShow(self, obj, widget):
        self.p.showLabel(obj, widget)

    def setLabelHide(self, widget):
        self.p.hideLabel(widget)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.ShiftModifier:
            print event.key()


class search_button(QPushButton):
    def __init__(self, *args):
        super(search_button, self).__init__(*args)
        self.i = QIcon(icon_path('query_def.png'))
        self.setIcon(self.i)
        self.setFixedSize(15, 15)
        self.setCheckable(True)

        qss = """
    QPushButton{
        border-style: outset;    
        background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
        stop:0.45 rgb(0, 170, 200, 50), 
        stop:0.49 rgb(100, 100, 100)
        stop:0.5 rgba(255, 255, 255, 0));
        background: transparent;
        }
    QPushButton:hover{
    background-color :qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
        stop:0.45 #09bb07, 
        stop:0.49 rgb(100, 100, 100)
        stop:0.5 rgba(255, 255, 255, 0));
    }

        """

        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self.i = QIcon(icon_path('query.png'))
        self.setIcon(self.i)

    def leaveEvent(self, event):
        self.i = QIcon(icon_path('query_def.png'))
        self.setIcon(self.i)


class asset_button(QPushButton):
    def __init__(self, show, hide, *__args):
        super(asset_button, self).__init__(*__args)
        self.setFixedSize(15, 15)
        self.setCheckable(True)
        self.setStyleSheet(pushbutton_qss)
        self.setToolTip(self.text())
        self.widget = asset_label(icon_path('alp.png'))
        self.widget.setHidden(True)

        self.s, self.h = show, hide

    def enterEvent(self, event):
        self.s(self, self.widget)

    def leaveEvent(self, event):
        self.h(self.widget)


class asset_label(QWidget):
    def __init__(self, iconPath, *args):
        super(asset_label, self).__init__(*args)
        if not os.path.exists(iconPath):
            sys.stdout.write(u'\r\n没有找到这个文件：\n%s\n' % iconPath)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(30, 30)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.labelBGround = QLabel(self)
        self.labelBGround.setScaledContents(True)
        self.labelBGround.setAutoFillBackground(True)

        self.pixmap = QPixmap(iconPath)
        self.labelBGround.setPixmap(self.pixmap)
        self.labelBGround.setAttribute(Qt.WA_TranslucentBackground, True)
        self.labelBGround.setGeometry(0, 0, 30, 30)

        self.labelTx = QLabel(self)
        font = QFont()
        font.setPointSize(15)
        self.labelTx.setFont(font)
        self.labelTx.setAlignment(Qt.AlignCenter)
        self.labelTx.setStyleSheet('color : white')
        self.labelTx.setGeometry(1, 2, 25, 25)

    @property
    def text(self):
        return self.labelTx.text()

    @text.setter
    def text(self, txt):
        self.labelTx.setText(txt)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class image_widget(QWidget):
    clicked = pyqtSignal(int)
    doubleClicked = pyqtSignal()
    prevSelected = None
    __in_path__ = ''
    __flag__ = ''
    jpg_list = ['.jpg', '.jpeg', '.bmp', '.png']
    mov_list = ['.mov', '.gif', '.avi']

    def __init__(self, *args, **kwargs):
        super(image_widget, self).__init__(**kwargs)
        self.thumb = None
        self.version = ''
        self.id = 0
        self.is_height = 0
        self.selected = False
        self.kwargs = kwargs

        self.image_label = QLabel(self)
        size_policy_image = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy_image.setHorizontalStretch(0)
        size_policy_image.setVerticalStretch(0)
        size_policy_image.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(size_policy_image)
        self.image_label.setScaledContents(1)

        self.text_label = QLabel(self)
        self.text_label.setAlignment(Qt.AlignCenter)
        size_policy_text = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy_image.setHorizontalStretch(0)
        size_policy_image.setVerticalStretch(0)
        size_policy_image.setHeightForWidth(self.text_label.sizePolicy().hasHeightForWidth())
        self.text_label.setSizePolicy(size_policy_text)

        if args:
            self.update(*args)

        lay = QVBoxLayout(self)
        lay.addWidget(self.image_label)
        lay.addWidget(self.text_label)

        lay.setSpacing(0)
        lay.setMargin(0)

        self.text_label.setStyleSheet("QLabel{background-color: rgb(113, 114, 116);color: rgb(0, 0, 0);}")

        self.setStyleSheet("QWidget{border:1px solid rgb(50, 50, 50);}")

    @property
    def ID(self):
        return self.id

    @ID.setter
    def ID(self, id):
        self.id = id

    def update(self, *args):
        if args:
            self.args = args
            self.id, self.chineseName, spell, otherName, SName, genera, place, description, imagePath, title, typeG = args
            self.set_font(self.chineseName)
            self.imagePath = [u'%s' % os.path.join(_conf.get(baseEnv.configuration, baseEnv.path),
                                                   'DATA/Image',
                                                   title,
                                                   _).replace('\\', '/')
                              for _ in imagePath.split(';')]
            self.set_in_path(self.imagePath[0])
        super(image_widget, self).update()

    def set_in_path(self, in_path):
        if not os.path.exists(in_path):
            sys.stdout.write('\r\n这个路径没了啊!!!\n%s' % in_path)
            return
        self.__in_path__ = in_path.replace('\\', '/')
        self.__flag__ = os.path.splitext(in_path)[-1]
        if self.__flag__ in self.jpg_list:
            self.load_image()
        elif self.__flag__ in self.mov_list:
            self.load_mov()

    def set_font(self, in_text):
        # font = QFont()
        # font.setPointSize(18)
        # self.text_label.setFont(font)
        self.text_label.setText(in_text)

    def load_image(self):
        self.thumb = QPixmap(self.__in_path__)
        self.image_label.setPixmap(self.thumb)

    def load_mov(self):
        self.thumb = QMovie(self.__in_path__)
        self.thumb.jumpToNextFrame()
        self.image_label.setMovie(self.thumb)

    def setSelected(self, conf):
        if image_widget.prevSelected is not None:
            image_widget.prevSelected.selected = False
            image_widget.prevSelected.repaint() if not image_widget().isHidden() else True
        self.selected = conf
        self.repaint()
        image_widget.prevSelected = self

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(True)
            self.setSelected(1)

        if event.button() == Qt.MiddleButton:
            self.clicked.emit(False)
            self.setSelected(0)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    def enterEvent(self, event):
        self.is_height = True
        self.repaint()

    def leaveEvent(self, event):
        self.is_height = False
        self.repaint()

    def paintEvent(self, event):
        if self.selected:
            if self.is_height:
                self.setStyleSheet("QWidget{border:3px solid rgb(200, 200, 0);}")
                self.text_label.setStyleSheet("QLabel{background-color: rgb(255, 255, 0);color: rgb(0, 0, 0);}")
            else:
                self.setStyleSheet("QWidget{border:3px solid rgb(150, 150, 0);}")
                self.text_label.setStyleSheet("QLabel{background-color: rgb(200, 200, 0);color: rgb(0, 0, 0);}")

        else:
            if self.is_height:
                self.setStyleSheet("QWidget{border:2px solid rgb(255, 255, 255);}")
                self.text_label.setStyleSheet("QLabel{background-color: rgb(230, 230, 230);color: rgb(0, 0, 0);}")

            else:
                self.setStyleSheet("QWidget{border:1px solid rgb(50, 50, 50);}")
                self.text_label.setStyleSheet("QLabel{background-color: rgb(113, 114, 116);color: rgb(0, 0, 0);}")


class picture_prev(QFrame):
    THUMB_WIDTH = 128
    THUMB_HEIGHT = 128
    THUMB_MIN = 64
    THUMB_MAX = 256

    def __init__(self, *args):
        super(picture_prev, self).__init__(*args)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout = QVBoxLayout(self)

        self.scro = QScrollArea(self)
        self.item_area = QWidget(self.scro)
        self.scro.setWidget(self.item_area)
        self.scro.setStyleSheet("QScrollArea{background-color: rgb(191, 191, 191);}")
        self.item_area.setStyleSheet("QWidget{background-color: rgb(191, 191, 191);}")

        layout.addWidget(self.scro)

        hBox = QHBoxLayout()
        layout.addLayout(hBox)

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(self.THUMB_MIN)
        self.slider.setMaximum(self.THUMB_MAX)
        self.slider.setValue(107)
        self.slider.setFixedWidth(self.THUMB_WIDTH)
        self.slider.setFixedHeight(15)
        self.slider.setStyleSheet(H_slider)
        self.slider.valueChanged['int'].connect(self.set_item_size)
        hBox.addWidget(self.slider)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hBox.addItem(spacerItem)
        self.pageW = pageWidget()
        hBox.addWidget(self.pageW)

        self.asset_space = 20
        self.auto_space = 0

        self.setWindowOpacity(0.0)
        self.Image_widget_list = dict()

    def clearAll(self):
        widgets = self.item_area.children()
        if widgets:
            for widget in widgets:
                widget.setParent(None)
                widget.deleteLater()
        self.Image_widget_list.clear()

    def clear_item(self, widget):
        if widget.prevSelected is not None:
            widget.setParent(None)
            self.Image_widget_list.pop(str(widget.id))
            widget.prevSelected = None
            widget.deleteLater()
            self.layout()

    def add_widget(self, widget):
        widget.setParent(self.item_area)
        self.Image_widget_list.setdefault(str(widget.id), widget)
        self.createContextMenu(widget)
        self.set_item_size(self.slider.value())

    def add_widgets(self, widgets):
        for widget in widgets:
            self.add_widget(widget)

    def layout(self):
        w = self.width() - 60
        widgets = [_ for _ in self.item_area.children()]  # if not _.isHidden()]
        num_x = max(math.ceil(w / (self.THUMB_WIDTH + self.asset_space)), 1)  # Can do -1
        num_y = math.ceil(len(widgets) / num_x)
        self.item_area.resize(w, num_y * (self.THUMB_HEIGHT + self.asset_space) + 50)

        main_w = self.item_area.width()
        num_x = max(math.ceil(main_w / (self.THUMB_WIDTH + self.asset_space)), 1)  # Can do -1

        x = 0
        y = 0
        for i in range(len(widgets)):
            space_x = 0
            if self.auto_space:
                space_x = (main_w - 30 - self.asset_space * 2 - num_x * (
                        self.THUMB_WIDTH + self.asset_space)) / num_x
            widgets[i].move(self.asset_space * 1 + x * (self.THUMB_WIDTH + self.asset_space + space_x),
                            self.asset_space * 1 + y * (self.THUMB_HEIGHT + self.asset_space))
            x += 1
            if x >= num_x:
                x = 0
                y += 1

    def changeItemSize(self, mount):
        widgets = self.item_area.children()
        self.THUMB_WIDTH += mount
        if self.THUMB_WIDTH > self.max_height:
            self.THUMB_WIDTH = self.max_height
        elif self.THUMB_WIDTH < self.min_width:
            self.THUMB_WIDTH = self.min_width

        self.THUMB_HEIGHT += mount
        if self.THUMB_HEIGHT > self.max_height:
            self.THUMB_HEIGHT = self.max_height
        elif self.THUMB_HEIGHT < self.min_width:
            self.THUMB_HEIGHT = self.min_width

        for a in widgets:
            a.resize(self.THUMB_WIDTH, self.THUMB_HEIGHT)

        self.layout()

    def set_item_size(self, size):
        widgets = self.item_area.children()

        self.THUMB_WIDTH = size
        self.THUMB_HEIGHT = size

        for a in widgets:
            a.resize(size, size)

        self.layout()

    def setSelected(self, id):
        self.ImageWidgetList[str(id)].setSelected()

    def edit_item(self):
        wgt = image_widget.prevSelected
        if not wgt:
            return

    def createContextMenu(self, widget):
        widget.setContextMenuPolicy(Qt.CustomContextMenu)
        widget.customContextMenuRequested.connect(self.showContextMenu)

        # create menu
        self.contextMenu = QMenu(self)

        self.editAction = QAction(u'| 编辑', self)
        self.delAvtion = QAction(u'| 删除', self)
        self.contextMenu.addAction(self.editAction)
        self.contextMenu.addAction(self.delAvtion)

        self.editAction.triggered.connect(self.parent().edit_item)
        self.delAvtion.triggered.connect(self.parent().del_item)

    def showContextMenu(self):
        self.contextMenu.exec_(QCursor.pos())

    def resize(self, event):
        self.set_item_size(self.slider.value())


class pageWidget(QWidget):
    def __init__(self, *args):
        super(pageWidget, self).__init__(*args)
        hBox = QHBoxLayout(self)
        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.setSpacing(9)
        hBox.setMargin(0)

        self.spin = QComboBox(self)
        self.spin.setFixedSize(50, 30)
        self.spin.setStyleSheet(comboBox)
        self.spin.addItems([str(i) for i in range(1, 101)])
        self.spin.setCurrentIndex(29)
        hBox.addWidget(self.spin)

        self.minP = QPushButton(QIcon(icon_path('minP.png')), '', self)
        self.dnP = QPushButton(QIcon(icon_path('dnP.png')), '', self)
        self.comboBoxNum = QComboBox(self)
        self.comboBoxNum.setStyleSheet(comboBox)
        self.upP = QPushButton(QIcon(icon_path('upP.png')), '', self)
        self.maxP = QPushButton(QIcon(icon_path('maxP.png')), '', self)

        all_pt = [self.minP, self.dnP, self.comboBoxNum, self.upP, self.maxP]

        for (i, t) in enumerate(all_pt):
            t.setIconSize(QSize(30, 30))
            if isinstance(t, QPushButton):
                t.setFixedSize(30, 30)
                t.setFlat(True)
                t.clicked.connect(partial(self.on_pushButton_clicked, i))
            else:
                t.setFixedSize(60, 30)
            hBox.addWidget(t)

    def on_pushButton_clicked(self, typ):
        maxNum = self.comboBoxNum.count() - 1
        if typ == 0:
            self.comboBoxNum.setCurrentIndex(0)
        elif typ == 1:
            changeIndex = self.comboBoxNum.currentIndex() - 1
            self.comboBoxNum.setCurrentIndex(changeIndex if changeIndex >= 0 else 0)
        elif typ == 3:
            changeIndex = self.comboBoxNum.currentIndex() + 1
            self.comboBoxNum.setCurrentIndex(changeIndex if changeIndex < maxNum else maxNum)
        else:
            self.comboBoxNum.setCurrentIndex(maxNum)
