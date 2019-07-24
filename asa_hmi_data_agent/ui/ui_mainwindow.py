# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        self.centralWidget.setFont(font)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget_main = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget_main.setObjectName("tabWidget_main")
        self.tabHmi = QtWidgets.QWidget()
        self.tabHmi.setObjectName("tabHmi")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabHmi)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabHmi_2 = QtWidgets.QWidget(self.tabHmi)
        self.tabHmi_2.setObjectName("tabHmi_2")
        self.verticalLayout_2.addWidget(self.tabHmi_2)
        self.tabHmi_1 = QtWidgets.QWidget(self.tabHmi)
        self.tabHmi_1.setObjectName("tabHmi_1")
        self.verticalLayout_2.addWidget(self.tabHmi_1)
        self.tabWidget_main.addTab(self.tabHmi, "")
        self.tabAsaProg = QtWidgets.QWidget()
        self.tabAsaProg.setObjectName("tabAsaProg")
        self.tabWidget_main.addTab(self.tabAsaProg, "")
        self.tabAvrdude = QtWidgets.QWidget()
        self.tabAvrdude.setObjectName("tabAvrdude")
        self.tabWidget_main.addTab(self.tabAvrdude, "")
        self.tabAdtSettings = QtWidgets.QWidget()
        self.tabAdtSettings.setObjectName("tabAdtSettings")
        self.tabWidget_main.addTab(self.tabAdtSettings, "")
        self.verticalLayout.addWidget(self.tabWidget_main)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.tabWidget_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASA_HMI_Data_Agent"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabHmi), _translate("MainWindow", "HMI"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabAsaProg), _translate("MainWindow", "燒錄M128"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabAvrdude), _translate("MainWindow", "STK500燒錄"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabAdtSettings), _translate("MainWindow", "設定與更新"))

