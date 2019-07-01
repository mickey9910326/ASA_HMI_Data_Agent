# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/widget_hmi_new_sop.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgeHmiNewStructOp(object):
    def setupUi(self, WidgeHmiNewStructOp):
        WidgeHmiNewStructOp.setObjectName("WidgeHmiNewStructOp")
        WidgeHmiNewStructOp.resize(104, 24)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        WidgeHmiNewStructOp.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WidgeHmiNewStructOp)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_up = QtWidgets.QPushButton(WidgeHmiNewStructOp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_up.sizePolicy().hasHeightForWidth())
        self.pushButton_up.setSizePolicy(sizePolicy)
        self.pushButton_up.setMinimumSize(QtCore.QSize(24, 0))
        self.pushButton_up.setMaximumSize(QtCore.QSize(24, 16777215))
        self.pushButton_up.setObjectName("pushButton_up")
        self.horizontalLayout.addWidget(self.pushButton_up)
        self.pushButton_down = QtWidgets.QPushButton(WidgeHmiNewStructOp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_down.sizePolicy().hasHeightForWidth())
        self.pushButton_down.setSizePolicy(sizePolicy)
        self.pushButton_down.setMinimumSize(QtCore.QSize(24, 0))
        self.pushButton_down.setMaximumSize(QtCore.QSize(24, 16777215))
        self.pushButton_down.setObjectName("pushButton_down")
        self.horizontalLayout.addWidget(self.pushButton_down)
        self.pushButton_plus = QtWidgets.QPushButton(WidgeHmiNewStructOp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_plus.sizePolicy().hasHeightForWidth())
        self.pushButton_plus.setSizePolicy(sizePolicy)
        self.pushButton_plus.setMinimumSize(QtCore.QSize(24, 0))
        self.pushButton_plus.setMaximumSize(QtCore.QSize(24, 16777215))
        self.pushButton_plus.setObjectName("pushButton_plus")
        self.horizontalLayout.addWidget(self.pushButton_plus)
        self.pushButton_minus = QtWidgets.QPushButton(WidgeHmiNewStructOp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_minus.sizePolicy().hasHeightForWidth())
        self.pushButton_minus.setSizePolicy(sizePolicy)
        self.pushButton_minus.setMinimumSize(QtCore.QSize(24, 0))
        self.pushButton_minus.setMaximumSize(QtCore.QSize(24, 16777215))
        self.pushButton_minus.setObjectName("pushButton_minus")
        self.horizontalLayout.addWidget(self.pushButton_minus)

        self.retranslateUi(WidgeHmiNewStructOp)
        QtCore.QMetaObject.connectSlotsByName(WidgeHmiNewStructOp)

    def retranslateUi(self, WidgeHmiNewStructOp):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_up.setText(_translate("WidgeHmiNewStructOp", "↑"))
        self.pushButton_down.setText(_translate("WidgeHmiNewStructOp", "↓"))
        self.pushButton_plus.setText(_translate("WidgeHmiNewStructOp", "＋"))
        self.pushButton_minus.setText(_translate("WidgeHmiNewStructOp", "－"))

