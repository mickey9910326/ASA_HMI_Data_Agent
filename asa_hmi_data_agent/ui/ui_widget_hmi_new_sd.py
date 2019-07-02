# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/widget_hmi_new_sd.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgeHmiNewStructData(object):
    def setupUi(self, WidgeHmiNewStructData):
        WidgeHmiNewStructData.setObjectName("WidgeHmiNewStructData")
        WidgeHmiNewStructData.resize(120, 22)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        WidgeHmiNewStructData.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WidgeHmiNewStructData)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_type = QtWidgets.QComboBox(WidgeHmiNewStructData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_type.sizePolicy().hasHeightForWidth())
        self.comboBox_type.setSizePolicy(sizePolicy)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_type)
        self.lineEdit_num = QtWidgets.QLineEdit(WidgeHmiNewStructData)
        self.lineEdit_num.setObjectName("lineEdit_num")
        self.horizontalLayout.addWidget(self.lineEdit_num)

        self.retranslateUi(WidgeHmiNewStructData)
        QtCore.QMetaObject.connectSlotsByName(WidgeHmiNewStructData)

    def retranslateUi(self, WidgeHmiNewStructData):
        _translate = QtCore.QCoreApplication.translate
        self.comboBox_type.setItemText(0, _translate("WidgeHmiNewStructData", "i8"))
        self.comboBox_type.setItemText(1, _translate("WidgeHmiNewStructData", "i16"))
        self.comboBox_type.setItemText(2, _translate("WidgeHmiNewStructData", "i32"))
        self.comboBox_type.setItemText(3, _translate("WidgeHmiNewStructData", "i64"))
        self.comboBox_type.setItemText(4, _translate("WidgeHmiNewStructData", "ui8"))
        self.comboBox_type.setItemText(5, _translate("WidgeHmiNewStructData", "ui16"))
        self.comboBox_type.setItemText(6, _translate("WidgeHmiNewStructData", "ui32"))
        self.comboBox_type.setItemText(7, _translate("WidgeHmiNewStructData", "ui64"))
        self.comboBox_type.setItemText(8, _translate("WidgeHmiNewStructData", "f32"))
        self.comboBox_type.setItemText(9, _translate("WidgeHmiNewStructData", "f64"))

