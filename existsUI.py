#!/user/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'miaoChenLiang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import __init__

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
__start_path__ = __init__.__start_path__


def icon_path(in_name):
    return os.path.join(__start_path__, 'UI/icons', in_name).replace('\\', '/')


# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class mSplashScreen(QSplashScreen):
    def __init__(self, animation, flag, widget):
        super(mSplashScreen, self).__init__(QPixmap(), flag)
        self.movie = QMovie(animation)
        self.movie.frameChanged.connect(self.onNextFrame)
        self.count = self.movie.frameCount()
        self.step = 0
        self.widget = widget

    def onNextFrame(self):
        if self.step < self.count:
            pixmap = self.movie.currentPixmap()
            self.setPixmap(pixmap)
            self.setMask(pixmap.mask())
            self.step += 1

        else:
            self.finish(self.widget)

    def showEvent(self, *args):
        self.movie.start()

    def finish(self, widget):
        widget.show()
        self.deleteLater()
        self.movie.deleteLater()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class Ui_Dialog(QDialog):
    # m_pressed = False

    def __init__(self, in_text, keyword):
        super(Ui_Dialog, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        if keyword.upper() == 'S':
            qs = QPushButton('SUCCESS')
            qs.clicked.connect(self.accept)
            pt = [qs]
            in_image = os.path.join(os.getcwd(), 'UI/icons/dlg/dialog_success.png').replace('\\', '/')

        if keyword.upper() == 'A':
            qo, qc = QPushButton('YES'), QPushButton('NO')
            qo.clicked.connect(self.accept)
            qc.clicked.connect(self.reject)
            pt = [qo, qc]
            in_image = os.path.join(os.getcwd(), 'UI/icons/dlg/dialog_ask.png').replace('\\', '/')

        if keyword.upper() == 'E':
            qe = QPushButton('ERROR')
            qe.clicked.connect(self.reject)
            pt = [qe]
            in_image = os.path.join(os.getcwd(), 'UI/icons/dlg/dialog_error.png').replace('\\', '/')

        if keyword.upper() == 'W':
            qe = QPushButton('WARNING')
            qe.clicked.connect(self.reject)
            pt = [qe]
            in_image = os.path.join(os.getcwd(), 'UI/icons/dlg/dialog_warning.png').replace('\\', '/')

        for each in pt:
            each.setStyleSheet("QPushButton{font: 20pt;}")
            each.setMinimumHeight(30)
            each.setMinimumSize(120, 30)

        self.resize(450, 170)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.verticalLayout = QVBoxLayout(self)

        # label image
        self.l_widget = QWidget(self)
        self.l_lay = QHBoxLayout(self.l_widget)
        spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label_warn = QLabel(self)
        self.label_warn.setScaledContents(1)
        self.label_warn.setAlignment(Qt.AlignCenter)
        self.label_warn.setPixmap(QPixmap(in_image))
        self.label_warn.setFixedSize(60, 60)
        self.l_lay.addItem(spacer1)
        self.l_lay.addWidget(self.label_warn)
        self.l_lay.addItem(spacer2)

        self.verticalLayout.addWidget(self.l_widget)

        # label text
        self.label_message = QLabel(self)
        self.label_message.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.label_message.setText(in_text)
        self.label_message.setStyleSheet("QLabel{color: rgb(0, 17, 20);}")
        font = QFont()
        font.setPointSize(20)
        self.label_message.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_message.sizePolicy().hasHeightForWidth())
        self.label_message.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.label_message, Qt.AlignHCenter)

        # push button
        self.wdg = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wdg.sizePolicy().hasHeightForWidth())
        self.wdg.setSizePolicy(sizePolicy)
        self.pt_layout = QHBoxLayout(self.wdg)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pt_layout.addItem(spacerItem)
        map(lambda x: self.pt_layout.addWidget(x), pt)
        self.verticalLayout.addWidget(self.wdg)
        self.pt_layout.addItem(spacerItem1)

    def accept(self):
        super(Ui_Dialog, self).accept()
        self.conf = 1

    def reject(self):
        super(Ui_Dialog, self).reject()
        self.conf = 0

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.c_pos = event.globalPos() - self.pos()
            self.m_pressed = True

        elif event.buttons() == Qt.MiddleButton:
            self.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.m_pressed:
                self.move(event.globalPos() - self.c_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.m_pressed = False

    def resizeEvent(self, event):
        self.setAttribute(Qt.WA_TranslucentBackground, 1)


class mSplashScreen_new(QSplashScreen):
    """
    start movie once
    """

    def __init__(self, animation, flag, widget):
        super(mSplashScreen_new, self).__init__(QPixmap(), flag)
        self.movie = QMovie(animation)
        self.movie.frameChanged.connect(self.onNextFrame)
        self.count = self.movie.frameCount()
        self.step = 0
        self.widget = widget

    def onNextFrame(self):
        if self.step < self.count:
            pixmap = self.movie.currentPixmap()
            self.setPixmap(pixmap)
            self.setMask(pixmap.mask())
            self.step += 1

        else:
            self.finish(self.widget)

    def showEvent(self, *args):
        self.movie.start()

    def finish(self, widget):
        widget.show()
        self.deleteLater()
        self.movie.deleteLater()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class imageDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(imageDialog, self).__init__(**kwargs)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.pixmap = QPixmap()
        if not args:
            self.reject()
        self.imageList = [u'%s' % each for each in args if os.path.exists(each) and os.path.isfile(each)]
        self.defNum = 0

        if not len(self.imageList):
            sys.stdout.write(u'\r\n这个没有图片~~！\n')
            self.imageList = [icon_path('file_error.png')]
        else:

            self.l_P = mLabel(-1)
            self.l_P.setParent(self)
            self.r_P = mLabel(1)
            self.r_P.setParent(self)

            self.changeImage(0)

    def changeImage(self, k):
        if self.defNum == self.imageList.__len__() - 1:
            self.defNum = 0
        elif self.defNum == 0 and k == -1:
            self.defNum = self.imageList.__len__() - 1
        else:
            self.defNum += k

        self.image = QImage(self.imageList[self.defNum])
        self.x, y = self.image.size().width(), self.image.size().height()
        self.resize(self.x, y)

        self.l_P.setGeometry(0, 0, 120, y)
        self.r_P.setGeometry(self.x - 120, 0, 120, y)
        self.resizeEvent(self)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.c_pos = event.globalPos() - self.pos()
            self.m_pressed = True

        if event.buttons() == Qt.MiddleButton:
            self.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.m_pressed:
                self.move(event.globalPos() - self.c_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.m_pressed = False

    def resizeEvent(self, event):
        self.pixmap.load(self.imageList[self.defNum])
        pal = QPalette()
        pal.setBrush(QPalette.Window,
                     QBrush(self.pixmap.scaled(event.size(),
                                               Qt.KeepAspectRatioByExpanding,
                                               Qt.SmoothTransformation)))

        self.setPalette(pal)


class mLabel(QWidget):
    def __init__(self, ID, *args):
        super(mLabel, self).__init__(*args)
        self.ID = ID

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent().changeImage(self.ID)
        else:
            self.parent().accept()


if __name__ == '__main__':
    app = QApplication([])
    From = imageDialog(
        *('D:/MCL/succulentPlants/UI/icons/a.jpg', 'D:/MCL/succulentPlants/UI/icons/b.jpg'))
    From.show()
    app.exec_()
