# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(557, 729)
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
        self.mainTab_HMI = QtWidgets.QWidget()
        self.mainTab_HMI.setObjectName("mainTab_HMI")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.mainTab_HMI)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabMain_HMI = QtWidgets.QVBoxLayout()
        self.tabMain_HMI.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.tabMain_HMI.setContentsMargins(11, 0, 11, 0)
        self.tabMain_HMI.setSpacing(6)
        self.tabMain_HMI.setObjectName("tabMain_HMI")
        self.groupBox_Serial = QtWidgets.QGroupBox(self.mainTab_HMI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Serial.sizePolicy().hasHeightForWidth())
        self.groupBox_Serial.setSizePolicy(sizePolicy)
        self.groupBox_Serial.setMinimumSize(QtCore.QSize(0, 75))
        self.groupBox_Serial.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox_Serial.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_Serial.setObjectName("groupBox_Serial")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_Serial)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_Serial)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setBaseSize(QtCore.QSize(0, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.portComboBox = QtWidgets.QComboBox(self.groupBox_Serial)
        self.portComboBox.setObjectName("portComboBox")
        self.horizontalLayout_2.addWidget(self.portComboBox)
        self.buttonPortToggle = QtWidgets.QPushButton(self.groupBox_Serial)
        self.buttonPortToggle.setObjectName("buttonPortToggle")
        self.horizontalLayout_2.addWidget(self.buttonPortToggle)
        self.tabMain_HMI.addWidget(self.groupBox_Serial)
        self.groupBox_Terminal = QtWidgets.QGroupBox(self.mainTab_HMI)
        self.groupBox_Terminal.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox_Terminal.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_Terminal.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox_Terminal.setObjectName("groupBox_Terminal")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_Terminal)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textTerminal = QtWidgets.QTextBrowser(self.groupBox_Terminal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textTerminal.sizePolicy().hasHeightForWidth())
        self.textTerminal.setSizePolicy(sizePolicy)
        self.textTerminal.setMinimumSize(QtCore.QSize(0, 60))
        self.textTerminal.setObjectName("textTerminal")
        self.verticalLayout_2.addWidget(self.textTerminal)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditTerminalSend = QtWidgets.QLineEdit(self.groupBox_Terminal)
        self.lineEditTerminalSend.setEnabled(True)
        self.lineEditTerminalSend.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEditTerminalSend.setObjectName("lineEditTerminalSend")
        self.horizontalLayout.addWidget(self.lineEditTerminalSend)
        self.buttonTerminalSend = QtWidgets.QPushButton(self.groupBox_Terminal)
        self.buttonTerminalSend.setObjectName("buttonTerminalSend")
        self.horizontalLayout.addWidget(self.buttonTerminalSend)
        self.buttonTerminalClear = QtWidgets.QPushButton(self.groupBox_Terminal)
        self.buttonTerminalClear.setObjectName("buttonTerminalClear")
        self.horizontalLayout.addWidget(self.buttonTerminalClear)
        self.buttonTerminalSave = QtWidgets.QPushButton(self.groupBox_Terminal)
        self.buttonTerminalSave.setObjectName("buttonTerminalSave")
        self.horizontalLayout.addWidget(self.buttonTerminalSave)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tabMain_HMI.addWidget(self.groupBox_Terminal)
        self.groupBox_SendRead = QtWidgets.QGroupBox(self.mainTab_HMI)
        self.groupBox_SendRead.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_SendRead.setObjectName("groupBox_SendRead")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_SendRead)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_SendRead)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSend = QtWidgets.QWidget()
        self.tabSend.setObjectName("tabSend")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tabSend)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.textEditSend = QtWidgets.QTextEdit(self.tabSend)
        self.textEditSend.setObjectName("textEditSend")
        self.verticalLayout_7.addWidget(self.textEditSend)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.buttonSendUi8ToString = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendUi8ToString.setObjectName("buttonSendUi8ToString")
        self.horizontalLayout_5.addWidget(self.buttonSendUi8ToString)
        self.buttonSendStringToUi8 = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendStringToUi8.setObjectName("buttonSendStringToUi8")
        self.horizontalLayout_5.addWidget(self.buttonSendStringToUi8)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.buttonSendClear = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendClear.setObjectName("buttonSendClear")
        self.verticalLayout_5.addWidget(self.buttonSendClear)
        self.buttonSendStruct = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendStruct.setObjectName("buttonSendStruct")
        self.verticalLayout_5.addWidget(self.buttonSendStruct)
        self.buttonSendArray = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendArray.setObjectName("buttonSendArray")
        self.verticalLayout_5.addWidget(self.buttonSendArray)
        spacerItem1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem1)
        self.buttonSendSaveFile = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendSaveFile.setObjectName("buttonSendSaveFile")
        self.verticalLayout_5.addWidget(self.buttonSendSaveFile)
        self.buttonSendReadFile = QtWidgets.QPushButton(self.tabSend)
        self.buttonSendReadFile.setObjectName("buttonSendReadFile")
        self.verticalLayout_5.addWidget(self.buttonSendReadFile)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem2)
        self.labelSendVerify = QtWidgets.QLabel(self.tabSend)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSendVerify.sizePolicy().hasHeightForWidth())
        self.labelSendVerify.setSizePolicy(sizePolicy)
        self.labelSendVerify.setMinimumSize(QtCore.QSize(75, 23))
        self.labelSendVerify.setMaximumSize(QtCore.QSize(75, 23))
        self.labelSendVerify.setObjectName("labelSendVerify")
        self.verticalLayout_5.addWidget(self.labelSendVerify)
        self.textBrowserSendVerify = QtWidgets.QTextBrowser(self.tabSend)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserSendVerify.sizePolicy().hasHeightForWidth())
        self.textBrowserSendVerify.setSizePolicy(sizePolicy)
        self.textBrowserSendVerify.setMinimumSize(QtCore.QSize(75, 25))
        self.textBrowserSendVerify.setMaximumSize(QtCore.QSize(75, 25))
        self.textBrowserSendVerify.setObjectName("textBrowserSendVerify")
        self.verticalLayout_5.addWidget(self.textBrowserSendVerify)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tabSend, "")
        self.tabReceive = QtWidgets.QWidget()
        self.tabReceive.setObjectName("tabReceive")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabReceive)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.textEditGet = QtWidgets.QTextEdit(self.tabReceive)
        self.textEditGet.setObjectName("textEditGet")
        self.verticalLayout_8.addWidget(self.textEditGet)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.buttonGetUi8ToString = QtWidgets.QPushButton(self.tabReceive)
        self.buttonGetUi8ToString.setObjectName("buttonGetUi8ToString")
        self.horizontalLayout_7.addWidget(self.buttonGetUi8ToString)
        self.buttonGetStringToUi8 = QtWidgets.QPushButton(self.tabReceive)
        self.buttonGetStringToUi8.setObjectName("buttonGetStringToUi8")
        self.horizontalLayout_7.addWidget(self.buttonGetStringToUi8)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.buttonGetClear = QtWidgets.QPushButton(self.tabReceive)
        self.buttonGetClear.setObjectName("buttonGetClear")
        self.verticalLayout_6.addWidget(self.buttonGetClear)
        self.buttonGetSaveFile = QtWidgets.QPushButton(self.tabReceive)
        self.buttonGetSaveFile.setObjectName("buttonGetSaveFile")
        self.verticalLayout_6.addWidget(self.buttonGetSaveFile)
        self.buttomGetMovetoSend = QtWidgets.QPushButton(self.tabReceive)
        self.buttomGetMovetoSend.setObjectName("buttomGetMovetoSend")
        self.verticalLayout_6.addWidget(self.buttomGetMovetoSend)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.tabWidget.addTab(self.tabReceive, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.tabMain_HMI.addWidget(self.groupBox_SendRead)
        self.horizontalLayout_6.addLayout(self.tabMain_HMI)
        self.tabWidget_main.addTab(self.mainTab_HMI, "")
        self.tabMain_prog = QtWidgets.QWidget()
        self.tabMain_prog.setObjectName("tabMain_prog")
        self.tabWidget_main.addTab(self.tabMain_prog, "")
        self.tabMain_avrdude = QtWidgets.QWidget()
        self.tabMain_avrdude.setObjectName("tabMain_avrdude")
        self.tabWidget_main.addTab(self.tabMain_avrdude, "")
        self.verticalLayout.addWidget(self.tabWidget_main)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASA_HMI_Data_Agent"))
        self.groupBox_Serial.setTitle(_translate("MainWindow", "串列埠設定"))
        self.label.setText(_translate("MainWindow", "選擇串列埠："))
        self.buttonPortToggle.setText(_translate("MainWindow", "開啟串列埠"))
        self.groupBox_Terminal.setTitle(_translate("MainWindow", "文字對話區"))
        self.buttonTerminalSend.setText(_translate("MainWindow", "Send"))
        self.buttonTerminalClear.setText(_translate("MainWindow", "清除對話框"))
        self.buttonTerminalSave.setText(_translate("MainWindow", "儲存對話框"))
        self.groupBox_SendRead.setTitle(_translate("MainWindow", "資料送收區"))
        self.buttonSendUi8ToString.setText(_translate("MainWindow", "ui8 轉 String"))
        self.buttonSendStringToUi8.setText(_translate("MainWindow", "String 轉 ui8"))
        self.buttonSendClear.setText(_translate("MainWindow", "清除暫存區"))
        self.buttonSendStruct.setText(_translate("MainWindow", "傳送結構形式"))
        self.buttonSendArray.setText(_translate("MainWindow", "傳送矩陣形式"))
        self.buttonSendSaveFile.setText(_translate("MainWindow", "儲存文字檔"))
        self.buttonSendReadFile.setText(_translate("MainWindow", "讀取文字檔"))
        self.labelSendVerify.setText(_translate("MainWindow", "資料格式驗證"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSend), _translate("MainWindow", "發送"))
        self.buttonGetUi8ToString.setText(_translate("MainWindow", "ui8 轉 String"))
        self.buttonGetStringToUi8.setText(_translate("MainWindow", "String 轉 ui8"))
        self.buttonGetClear.setText(_translate("MainWindow", "清除暫存區"))
        self.buttonGetSaveFile.setText(_translate("MainWindow", "儲存文字檔"))
        self.buttomGetMovetoSend.setText(_translate("MainWindow", "移動到發送區"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReceive), _translate("MainWindow", "接收"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.mainTab_HMI), _translate("MainWindow", "HMI"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabMain_prog), _translate("MainWindow", "燒錄M128"))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabMain_avrdude), _translate("MainWindow", "M128_STK500"))

