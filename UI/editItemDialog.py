# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/MCL/python/succulentPlants/UI\editItemDialog.ui'
#
# Created: Mon Jun 25 22:54:56 2018
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(863, 624)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_message = QtGui.QFrame(Dialog)
        self.frame_message.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_message.sizePolicy().hasHeightForWidth())
        self.frame_message.setSizePolicy(sizePolicy)
        self.frame_message.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_message.setFrameShape(QtGui.QFrame.Box)
        self.frame_message.setObjectName(_fromUtf8("frame_message"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_message)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEdit_title = QtGui.QLineEdit(self.frame_message)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_title.setFont(font)
        self.lineEdit_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_title.setObjectName(_fromUtf8("lineEdit_title"))
        self.verticalLayout_2.addWidget(self.lineEdit_title)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_From = QtGui.QLabel(self.frame_message)
        self.label_From.setObjectName(_fromUtf8("label_From"))
        self.gridLayout.addWidget(self.label_From, 5, 0, 1, 1)
        self.lineEdit_cName = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_cName.setEnabled(True)
        self.lineEdit_cName.setAutoFillBackground(False)
        self.lineEdit_cName.setFrame(False)
        self.lineEdit_cName.setReadOnly(False)
        self.lineEdit_cName.setObjectName(_fromUtf8("lineEdit_cName"))
        self.gridLayout.addWidget(self.lineEdit_cName, 0, 1, 1, 1)
        self.label_spell = QtGui.QLabel(self.frame_message)
        self.label_spell.setObjectName(_fromUtf8("label_spell"))
        self.gridLayout.addWidget(self.label_spell, 1, 0, 1, 1)
        self.lineEdit_From = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_From.setFrame(False)
        self.lineEdit_From.setObjectName(_fromUtf8("lineEdit_From"))
        self.gridLayout.addWidget(self.lineEdit_From, 5, 1, 1, 1)
        self.label_sOther = QtGui.QLabel(self.frame_message)
        self.label_sOther.setObjectName(_fromUtf8("label_sOther"))
        self.gridLayout.addWidget(self.label_sOther, 2, 0, 1, 1)
        self.lineEdit_spell = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_spell.setEnabled(True)
        self.lineEdit_spell.setFrame(False)
        self.lineEdit_spell.setEchoMode(QtGui.QLineEdit.Normal)
        self.lineEdit_spell.setReadOnly(False)
        self.lineEdit_spell.setObjectName(_fromUtf8("lineEdit_spell"))
        self.gridLayout.addWidget(self.lineEdit_spell, 1, 1, 1, 1)
        self.lineEdit_type = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_type.setFrame(False)
        self.lineEdit_type.setObjectName(_fromUtf8("lineEdit_type"))
        self.gridLayout.addWidget(self.lineEdit_type, 4, 1, 1, 1)
        self.label_cName = QtGui.QLabel(self.frame_message)
        self.label_cName.setObjectName(_fromUtf8("label_cName"))
        self.gridLayout.addWidget(self.label_cName, 0, 0, 1, 1)
        self.label_type = QtGui.QLabel(self.frame_message)
        self.label_type.setObjectName(_fromUtf8("label_type"))
        self.gridLayout.addWidget(self.label_type, 4, 0, 1, 1)
        self.lineEdit_sOther = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_sOther.setEnabled(True)
        self.lineEdit_sOther.setFrame(False)
        self.lineEdit_sOther.setEchoMode(QtGui.QLineEdit.Normal)
        self.lineEdit_sOther.setReadOnly(False)
        self.lineEdit_sOther.setObjectName(_fromUtf8("lineEdit_sOther"))
        self.gridLayout.addWidget(self.lineEdit_sOther, 2, 1, 1, 1)
        self.label_lName = QtGui.QLabel(self.frame_message)
        self.label_lName.setObjectName(_fromUtf8("label_lName"))
        self.gridLayout.addWidget(self.label_lName, 3, 0, 1, 1)
        self.label_ID = QtGui.QLabel(self.frame_message)
        self.label_ID.setObjectName(_fromUtf8("label_ID"))
        self.gridLayout.addWidget(self.label_ID, 6, 0, 1, 1)
        self.lineEdit_ID = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_ID.setEnabled(False)
        self.lineEdit_ID.setFrame(False)
        self.lineEdit_ID.setObjectName(_fromUtf8("lineEdit_ID"))
        self.gridLayout.addWidget(self.lineEdit_ID, 6, 1, 1, 1)
        self.lineEdit_lName = QtGui.QLineEdit(self.frame_message)
        self.lineEdit_lName.setFrame(False)
        self.lineEdit_lName.setObjectName(_fromUtf8("lineEdit_lName"))
        self.gridLayout.addWidget(self.lineEdit_lName, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.textEdit_intro = QtGui.QTextEdit(self.frame_message)
        self.textEdit_intro.setObjectName(_fromUtf8("textEdit_intro"))
        self.verticalLayout_2.addWidget(self.textEdit_intro)
        self.horizontalLayout.addWidget(self.frame_message)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.lineEdit_title.setText(_translate("Dialog", "标题", None))
        self.label_From.setText(_translate("Dialog", "产地分布 ：", None))
        self.label_spell.setText(_translate("Dialog", "拼音     ：", None))
        self.label_sOther.setText(_translate("Dialog", "别称     ：", None))
        self.label_cName.setText(_translate("Dialog", "中文名   ：", None))
        self.label_type.setText(_translate("Dialog", "科属     ：", None))
        self.label_lName.setText(_translate("Dialog", "拉丁学名 ：", None))
        self.label_ID.setText(_translate("Dialog", "ID       ：", None))

