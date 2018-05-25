#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
try:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
except ImportError:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

import os
import glob
import random

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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置 窗口名称
        self.setObjectName(obj_name)
        self.setWindowTitle(obj_name)
        self.label_icon = QLabel(self)

        self.label_message = QLabel(self)
        self.label_message.setText(title)

        self.button_box = QDialogButtonBox(self)

        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")

        font = QFont()
        font.setPointSize(20)

        self.label_message.setFont(font)
        self.button_box.setFont(font)

        self.__init__UI()
        self.bt_clicked()

        self.setFixedSize(self.all_x, self.all_y)

    def __init__UI(self):
        new_cc = self.conf.upper().strip()
        if new_cc == 'E':
            pixmap = QPixmap(icon_path('dlg/dialog_error.png'))
            pass

        elif new_cc == 'S':
            pixmap = QPixmap(icon_path('dlg/dialog_error.png'))
            pass

        elif new_cc == 'A':
            pixmap = QPixmap(icon_path('dlg/dialog_error.png'))
            pass

        else:
            # if new_cc == 'w':
            pixmap = QPixmap(icon_path('dlg/dialog_error.png'))

        of_x, of_y = pixmap.width(), pixmap.height()
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setGeometry((self.all_x - of_x) / 2, 10, of_x, of_y)

    def bt_clicked(self):
        """
        所有的按钮信号槽链接
        :return:
        """
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

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

    def resizeEvent(self, event):
        self.setAttribute(Qt.WA_TranslucentBackground, 1)

    def showEvent(self, *args):
        self.button_box.setGeometry(self.all_x / 2, self.all_y - 35, self.all_x / 2, 35)
        self.label_message.setGeometry(0, self.all_y - 90, self.all_x, 35)

# if __name__ == '__main__':
#     app = QApplication([])
#     dlg = warning_ui('txt_')
#     aa = dlg.exec_()
#     print aa
#     app.exec_()
