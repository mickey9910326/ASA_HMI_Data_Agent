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
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        HmiLoadDialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(HmiLoadDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(HmiLoadDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_mat = QtWidgets.QWidget()
        self.tab_mat.setObjectName("tab_mat")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_mat)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 8, 1, 1, 1)
        self.pushButton_up = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_up.setObjectName("pushButton_up")
        self.gridLayout_3.addWidget(self.pushButton_up, 5, 1, 1, 1)
        self.pushButton_confirm = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.gridLayout_3.addWidget(self.pushButton_confirm, 9, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 1, 1, 1)
        self.tableWidget_mat = QtWidgets.QTableWidget(self.tab_mat)
        self.tableWidget_mat.setObjectName("tableWidget_mat")
        self.tableWidget_mat.setColumnCount(6)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_mat.setHorizontalHeaderItem(5, item)
        self.gridLayout_3.addWidget(self.tableWidget_mat, 1, 0, 9, 1)
        self.pushButton_down = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_down.setObjectName("pushButton_down")
        self.gridLayout_3.addWidget(self.pushButton_down, 6, 1, 1, 1)
        self.pushButton_delete = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.gridLayout_3.addWidget(self.pushButton_delete, 7, 1, 1, 1)
        self.pushButton_load = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_load.setObjectName("pushButton_load")
        self.gridLayout_3.addWidget(self.pushButton_load, 1, 1, 1, 1)
        self.pushButton_newSeq = QtWidgets.QPushButton(self.tab_mat)
        self.pushButton_newSeq.setObjectName("pushButton_newSeq")
        self.gridLayout_3.addWidget(self.pushButton_newSeq, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 4, 1, 1, 1)
        self.tabWidget.addTab(self.tab_mat, "")
        self.tab_csv = QtWidgets.QWidget()
        self.tab_csv.setObjectName("tab_csv")
        self.tabWidget.addTab(self.tab_csv, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(HmiLoadDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HmiLoadDialog)
        HmiLoadDialog.setTabOrder(self.tabWidget, self.tableWidget_mat)
        HmiLoadDialog.setTabOrder(self.tableWidget_mat, self.pushButton_load)
        HmiLoadDialog.setTabOrder(self.pushButton_load, self.pushButton_newSeq)
        HmiLoadDialog.setTabOrder(self.pushButton_newSeq, self.pushButton_up)
        HmiLoadDialog.setTabOrder(self.pushButton_up, self.pushButton_down)
        HmiLoadDialog.setTabOrder(self.pushButton_down, self.pushButton_delete)
        HmiLoadDialog.setTabOrder(self.pushButton_delete, self.pushButton_confirm)

    def retranslateUi(self, HmiLoadDialog):
        _translate = QtCore.QCoreApplication.translate
        HmiLoadDialog.setWindowTitle(_translate("HmiLoadDialog", "HmiLoadDialog"))
        self.pushButton_up.setText(_translate("HmiLoadDialog", "上移"))
        self.pushButton_confirm.setText(_translate("HmiLoadDialog", "確認"))
        item = self.tableWidget_mat.horizontalHeaderItem(0)
        item.setText(_translate("HmiLoadDialog", "新順序"))
        item = self.tableWidget_mat.horizontalHeaderItem(1)
        item.setText(_translate("HmiLoadDialog", "變數名稱"))
        item = self.tableWidget_mat.horizontalHeaderItem(2)
        item.setText(_translate("HmiLoadDialog", "型態"))
        item = self.tableWidget_mat.horizontalHeaderItem(3)
        item.setText(_translate("HmiLoadDialog", "個數"))
        item = self.tableWidget_mat.horizontalHeaderItem(4)
        item.setText(_translate("HmiLoadDialog", "總byte"))
        item = self.tableWidget_mat.horizontalHeaderItem(5)
        item.setText(_translate("HmiLoadDialog", "資料"))
        self.pushButton_down.setText(_translate("HmiLoadDialog", "下移"))
        self.pushButton_delete.setText(_translate("HmiLoadDialog", "刪除"))
        self.pushButton_load.setText(_translate("HmiLoadDialog", "選擇檔案"))
        self.pushButton_newSeq.setText(_translate("HmiLoadDialog", "應用新順序"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mat), _translate("HmiLoadDialog", "mat file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_csv), _translate("HmiLoadDialog", "csv file"))
