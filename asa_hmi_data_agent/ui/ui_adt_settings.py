# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/adt_settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidgetAdtSettings(object):
    def setupUi(self, MainWidgetAdtSettings):
        MainWidgetAdtSettings.setObjectName("MainWidgetAdtSettings")
        MainWidgetAdtSettings.resize(500, 700)
        self.gridLayout = QtWidgets.QGridLayout(MainWidgetAdtSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.label_termNum = QtWidgets.QLabel(MainWidgetAdtSettings)
        self.label_termNum.setObjectName("label_termNum")
        self.gridLayout.addWidget(self.label_termNum, 0, 0, 1, 1)
        self.pushButton_termNumApply = QtWidgets.QPushButton(MainWidgetAdtSettings)
        self.pushButton_termNumApply.setObjectName("pushButton_termNumApply")
        self.gridLayout.addWidget(self.pushButton_termNumApply, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.comboBox_termNum = QtWidgets.QComboBox(MainWidgetAdtSettings)
        self.comboBox_termNum.setObjectName("comboBox_termNum")
        self.comboBox_termNum.addItem("")
        self.comboBox_termNum.addItem("")
        self.gridLayout.addWidget(self.comboBox_termNum, 0, 1, 1, 1)

        self.retranslateUi(MainWidgetAdtSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWidgetAdtSettings)

    def retranslateUi(self, MainWidgetAdtSettings):
        _translate = QtCore.QCoreApplication.translate
        self.label_termNum.setText(_translate("MainWidgetAdtSettings", "Terminal 數量："))
        self.pushButton_termNumApply.setText(_translate("MainWidgetAdtSettings", "應用"))
        self.comboBox_termNum.setItemText(0, _translate("MainWidgetAdtSettings", "1"))
        self.comboBox_termNum.setItemText(1, _translate("MainWidgetAdtSettings", "2"))

