#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

import os

from PyQt4.QtCore import *
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from PyQt4.QtGui import *

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
__abs_path__ = os.path.dirname(__file__).replace('\\', '/')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def icon_path(in_name):
    return os.path.join(__abs_path__, 'icons', in_name).replace('\\', '/')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class warning_ui(QDialog):
    all_x = 450
    all_y = 200

    def __init__(self, obj_name, title="Please enter something!", conf='w', parent=None):
        super(warning_ui, self).__init__(parent)
        self.conf = conf
        # 设置 窗口透明
        self.setMouseTracking(True)
        # self.setAttribute(Qt.WA_TranslucentBackground, 1)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置 窗口名称
        self.setObjectName(obj_name)
        self.setWindowTitle(obj_name)
        # 设置 尺寸
        self.setFixedWidth(self.all_x)
        # self.setFixedSize(self.all_x, self.all_y)

        # UI
        font = QFont()
        font.setPointSize(18)

        lay = QVBoxLayout(self)

        self.label_icon = QLabel(self)
        self.label_icon.setFixedSize(50, 50)
        self.label_icon.setScaledContents(True)
        self.label_icon.setAlignment(Qt.AlignCenter)

        lay.addWidget(self.label_icon, Qt.AlignHCenter, Qt.AlignHCenter)

        self.label_message = QLabel(self)
        self.label_message.setWordWrap(True)
        self.label_message.setAlignment(Qt.AlignCenter)

        self.label_message.setFont(font)
        self.label_message.setText(title)
        lay.addWidget(self.label_message)

        HLay = QHBoxLayout()
        lay.addLayout(HLay)

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        HLay.addItem(spacerItem)

        self.pushButton_OK = QPushButton('OK', self)
        self.pushButton_OK.setFixedWidth(120)
        self.pushButton_OK.setFont(font)
        HLay.addWidget(self.pushButton_OK)

        self.pushButton_cancel = QPushButton('cancel', self)
        self.pushButton_cancel.setFixedWidth(120)
        self.pushButton_cancel.setFont(font)
        HLay.addWidget(self.pushButton_cancel)

        self.__init__UI()
        self.bt_clicked()

        QMetaObject.connectSlotsByName(self)

    def __init__UI(self):
        new_cc = self.conf.upper().strip()
        if new_cc == 'E':
            pixmap = QPixmap(icon_path('dlg/dialog_error.png'))
            self.pushButton_OK.hide()
            pass

        elif new_cc == 'S':
            pixmap = QPixmap(icon_path('dlg/dialog_success.png'))
            self.pushButton_cancel.hide()
            pass

        elif new_cc == 'A':
            pixmap = QPixmap(icon_path('dlg/dialog_ask.png'))
            pass

        else:
            # if new_cc == 'w':
            pixmap = QPixmap(icon_path('dlg/dialog_warning.png'))
            self.pushButton_cancel.hide()

        of_x, of_y = pixmap.width(), pixmap.height()
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setGeometry((self.all_x - of_x) / 2, 10, of_x, of_y)

    def bt_clicked(self):
        """
        所有的按钮信号槽链接
        :return:
        """
        self.pushButton_OK.clicked.connect(self.accept)
        self.pushButton_cancel.clicked.connect(self.reject)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # super ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.c_pos = event.globalPos() - self.pos()
            self.m_pressed = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.m_pressed:
                self.move(event.globalPos() - self.c_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.m_pressed = False

    # def showEvent(self, *args):
    #     self.button_box.setGeometry(self.all_x / 2, self.all_y - 35, self.all_x / 2, 35)
    #     self.label_message.setGeometry(0, self.all_y - 90, self.all_x, 35)


if __name__ == '__main__':
    app = QApplication([])
    dlg = warning_ui('txt_', conf='a')
    aa = dlg.exec_()
    app.exec_()
