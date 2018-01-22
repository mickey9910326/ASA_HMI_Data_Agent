# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget_main = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget_main.setObjectName("tabWidget_main")
        self.tabHmi = QtWidgets.QWidget()
        self.tabHmi.setObjectName("tabHmi")
        self.tabWidget_main.addTab(self.tabHmi, "")
        self.tabAsaProg = QtWidgets.QWidget()
        self.tabAsaProg.setObjectName("tabAsaProg")
        self.tabWidget_main.addTab(self.tabAsaProg, "")
        self.tabAvrdude = QtWidgets.QWidget()
        self.tabAvrdude.setObjectName("tabAvrdude")
        self.tabWidget_main.addTab(self.tabAvrdude, "")
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
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabAvrdude), _translate("MainWindow", "M128_STK500"))

