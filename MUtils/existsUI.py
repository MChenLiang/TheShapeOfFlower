#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @email : spirit_az@foxmail.com
__author__ = 'miaoChenLiang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import re

import maya.OpenMayaUI as mui
import pymel.core as pm

maya_qt_ver = int(re.match('\d', pm.about(qt=True)).group())

if maya_qt_ver == 5:
    try:
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        from PyQt5 import uic
        import sip

        USE_PYQT_MODULE = True

    except:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        import shiboken2, pyside2uic

        USE_PYQT_MODULE = False

else:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        from PyQt4 import uic
        import sip, shiboken

        USE_PYQT_MODULE = True

    except:
        from PySide.QtCore import *
        from PySide.QtGui import *

        USE_PYQT_MODULE = False


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

def GetMayaLayout(layoutString):
    ptr = mui.MQtUtil.findLayout(layoutString)
    if ptr:
        return sip.wrapinstance(long(ptr), QObject)


def GetWindow(windowName):
    ptr = mui.MQtUtil.findWindow(windowName)
    if ptr:
        return sip.wrapinstance(long(ptr), QObject)


def GetFullName(qObj):
    pointer = sip.unwrapinstance(qObj)
    if type(pointer) == long:
        windowString = mui.MQtUtil.fullName(pointer)
        if windowString:
            return windowString
        else:
            return ""
    else:
        return GetQtWidget(qObj.objectName(), LongName=True)[-1]


# 实例maya窗口
def wrapInstance(widget):
    if isinstance(widget, basestring):
        widget = mui.MQtUtil.findWindow(widget)

    if USE_PYQT_MODULE:
        return sip.wrapinstance(long(widget), QObject)
    else:
        if maya_qt_ver == 5:
            return shiboken2.wrapInstance(long(widget), QWidget)
        else:
            return shiboken.wrapInstance(long(widget), QWidget)


def GetMayaMainWindow():
    maya_window = mui.MQtUtil.mainWindow()
    return wrapInstance(maya_window)


def GetQtWidget(QWidgetName, LongName=False):
    RootName = str(GetMayaMainWindow().objectName())
    Name = QWidgetName.split("|")[-1]
    for w in QApplication.topLevelWidgets():
        try:
            if w.objectName() == Name:
                if LongName:
                    return (w, "|" + "|".join([RootName, QWidgetName]))
                else:
                    return w
        except:
            pass
    try:
        for w in QApplication.topLevelWidgets():
            for c in w.children():
                if c.objectName() == Name:
                    if LongName:
                        return (c, "|" + "|".join([str(w.objectName()),
                                                   str(c.objectName())]))
                    else:
                        return c
    except:
        pass


# 查询
def UIExists(Name, AsBool=True):
    QObject = GetQtWidget(Name)
    if QObject:
        if AsBool:
            return bool(QObject)
        return QObject
    else:
        if AsBool:
            return False
        return None


def Raise(Name):
    qobject = GetQtWidget(Name)
    if qobject:
        qobject.deleteLater()
        # qobject.setHidden(False)
        # qobject.raise_()
        return True
    else:
        return False


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# 开机画面  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class mSplashScreen(QSplashScreen):
    def __init__(self, animation, flag):
        super(mSplashScreen, self).__init__(QPixmap(), flag)
        self.move = QMovie(animation)
        self.move.frameChanged.connect(self.onNextFrame)

    def onNextFrame(self):
        pixmap = self.move.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

    def showEvent(self, *args):
        self.move.start()

    def finish(self, widget):
        widget.show()
        self.deleteLater()
        self.move.deleteLater()


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