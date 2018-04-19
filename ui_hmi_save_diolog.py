# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/hmi_save_diolog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HmiSaveDiolog(object):
    def setupUi(self, HmiSaveDiolog):
        HmiSaveDiolog.setObjectName("HmiSaveDiolog")
        HmiSaveDiolog.resize(625, 349)
        self.gridLayout_2 = QtWidgets.QGridLayout(HmiSaveDiolog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(HmiSaveDiolog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_mat = QtWidgets.QWidget()
        self.tab_mat.setObjectName("tab_mat")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_mat)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_matSave = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_matSave.setObjectName("pushButton_matSave")
        self.gridLayout_3.addWidget(self.pushButton_matSave, 1, 1, 1, 1)
        self.tableWidget_mat = QtWidgets.QTableWidget(self.tab_mat)
        self.tableWidget_mat.setObjectName("tableWidget_mat")
        self.tableWidget_mat.setColumnCount(5)
        self.tableWidget_mat.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(4, item)
        self.gridLayout_3.addWidget(self.tableWidget_mat, 1, 0, 4, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 1, 1, 1)
        self.pushButton_matClose = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_matClose.setObjectName("pushButton_matClose")
        self.gridLayout_3.addWidget(self.pushButton_matClose, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab_mat, "")
        self.tab_csv = QtWidgets.QWidget()
        self.tab_csv.setObjectName("tab_csv")
        self.tabWidget.addTab(self.tab_csv, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(HmiSaveDiolog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HmiSaveDiolog)

    def retranslateUi(self, HmiSaveDiolog):
        _translate = QtCore.QCoreApplication.translate
        HmiSaveDiolog.setWindowTitle(_translate("HmiSaveDiolog", "Dialog"))
        self.pushButton_matSave.setText(_translate("HmiSaveDiolog", "Save"))
        item = self.tableWidget_mat.horizontalHeaderItem(0)
        item.setText(_translate("HmiSaveDiolog", "name"))
        item = self.tableWidget_mat.horizontalHeaderItem(1)
        item.setText(_translate("HmiSaveDiolog", "type"))
        item = self.tableWidget_mat.horizontalHeaderItem(2)
        item.setText(_translate("HmiSaveDiolog", "nums"))
        item = self.tableWidget_mat.horizontalHeaderItem(3)
        item.setText(_translate("HmiSaveDiolog", "bytes"))
        item = self.tableWidget_mat.horizontalHeaderItem(4)
        item.setText(_translate("HmiSaveDiolog", "data"))
        self.pushButton_matClose.setText(_translate("HmiSaveDiolog", "Close"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mat), _translate("HmiSaveDiolog", "mat file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_csv), _translate("HmiSaveDiolog", "csv file"))

