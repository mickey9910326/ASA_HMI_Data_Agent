# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/hmi_load_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HmiLoadDialog(object):
    def setupUi(self, HmiLoadDialog):
        HmiLoadDialog.setObjectName("HmiLoadDialog")
        HmiLoadDialog.resize(644, 330)
        self.gridLayout = QtWidgets.QGridLayout(HmiLoadDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(HmiLoadDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_mat = QtWidgets.QWidget()
        self.tab_mat.setObjectName("tab_mat")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_mat)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_load = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_load.setObjectName("pushButton_load")
        self.gridLayout_3.addWidget(self.pushButton_load, 1, 1, 1, 1)
        self.tableWidget_mat = QtWidgets.QTableWidget(self.tab_mat)
        self.tableWidget_mat.setObjectName("tableWidget_mat")
        self.tableWidget_mat.setColumnCount(4)
        self.tableWidget_mat.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(3, item)
        self.gridLayout_3.addWidget(self.tableWidget_mat, 1, 0, 8, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 7, 1, 1, 1)
        self.pushButton_confirm = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.gridLayout_3.addWidget(self.pushButton_confirm, 8, 1, 1, 1)
        self.pushButton_up = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_up.setObjectName("pushButton_up")
        self.gridLayout_3.addWidget(self.pushButton_up, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 1, 1, 1)
        self.pushButton_down = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_down.setObjectName("pushButton_down")
        self.gridLayout_3.addWidget(self.pushButton_down, 5, 1, 1, 1)
        self.pushButton_delete = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.gridLayout_3.addWidget(self.pushButton_delete, 6, 1, 1, 1)
        self.tabWidget.addTab(self.tab_mat, "")
        self.tab_csv = QtWidgets.QWidget()
        self.tab_csv.setObjectName("tab_csv")
        self.tabWidget.addTab(self.tab_csv, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(HmiLoadDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HmiLoadDialog)

    def retranslateUi(self, HmiLoadDialog):
        _translate = QtCore.QCoreApplication.translate
        HmiLoadDialog.setWindowTitle(_translate("HmiLoadDialog", "Dialog"))
        self.pushButton_load.setText(_translate("HmiLoadDialog", "選擇檔案"))
        item = self.tableWidget_mat.horizontalHeaderItem(0)
        item.setText(_translate("HmiLoadDialog", "type"))
        item = self.tableWidget_mat.horizontalHeaderItem(1)
        item.setText(_translate("HmiLoadDialog", "nums"))
        item = self.tableWidget_mat.horizontalHeaderItem(2)
        item.setText(_translate("HmiLoadDialog", "bytes"))
        item = self.tableWidget_mat.horizontalHeaderItem(3)
        item.setText(_translate("HmiLoadDialog", "data"))
        self.pushButton_confirm.setText(_translate("HmiLoadDialog", "確認"))
        self.pushButton_up.setText(_translate("HmiLoadDialog", "上移"))
        self.pushButton_down.setText(_translate("HmiLoadDialog", "下移"))
        self.pushButton_delete.setText(_translate("HmiLoadDialog", "刪除"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mat), _translate("HmiLoadDialog", "mat file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_csv), _translate("HmiLoadDialog", "csv file"))

