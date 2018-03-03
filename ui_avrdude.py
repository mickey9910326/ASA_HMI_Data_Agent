# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/avrdude.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidgetAvrdude(object):
    def setupUi(self, MainWidgetAvrdude):
        MainWidgetAvrdude.setObjectName("MainWidgetAvrdude")
        MainWidgetAvrdude.resize(526, 700)
        self.gridLayout_8 = QtWidgets.QGridLayout(MainWidgetAvrdude)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.groupBox_config = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_config.setFont(font)
        self.groupBox_config.setObjectName("groupBox_config")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_config)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_config = QtWidgets.QComboBox(self.groupBox_config)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.comboBox_config.setFont(font)
        self.comboBox_config.setEditable(True)
        self.comboBox_config.setObjectName("comboBox_config")
        self.comboBox_config.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_config)
        self.pushButton_configSave = QtWidgets.QPushButton(self.groupBox_config)
        self.pushButton_configSave.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_configSave.setFont(font)
        self.pushButton_configSave.setObjectName("pushButton_configSave")
        self.horizontalLayout.addWidget(self.pushButton_configSave)
        self.pushButton_configDelete = QtWidgets.QPushButton(self.groupBox_config)
        self.pushButton_configDelete.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_configDelete.setFont(font)
        self.pushButton_configDelete.setObjectName("pushButton_configDelete")
        self.horizontalLayout.addWidget(self.pushButton_configDelete)
        self.gridLayout_8.addWidget(self.groupBox_config, 0, 0, 1, 4)
        self.groupBox_serial = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_serial.setFont(font)
        self.groupBox_serial.setObjectName("groupBox_serial")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_serial)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_serialSetPort = QtWidgets.QLabel(self.groupBox_serial)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_serialSetPort.setFont(font)
        self.label_serialSetPort.setObjectName("label_serialSetPort")
        self.gridLayout_7.addWidget(self.label_serialSetPort, 0, 1, 1, 1)
        self.label_serialSetBaud = QtWidgets.QLabel(self.groupBox_serial)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_serialSetBaud.setFont(font)
        self.label_serialSetBaud.setObjectName("label_serialSetBaud")
        self.gridLayout_7.addWidget(self.label_serialSetBaud, 0, 2, 1, 1)
        self.lineEdit_serialSetBaud = QtWidgets.QLineEdit(self.groupBox_serial)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_serialSetBaud.setFont(font)
        self.lineEdit_serialSetBaud.setObjectName("lineEdit_serialSetBaud")
        self.gridLayout_7.addWidget(self.lineEdit_serialSetBaud, 1, 2, 1, 1)
        self.comboBox_serialSetPort = QtWidgets.QComboBox(self.groupBox_serial)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.comboBox_serialSetPort.setFont(font)
        self.comboBox_serialSetPort.setObjectName("comboBox_serialSetPort")
        self.gridLayout_7.addWidget(self.comboBox_serialSetPort, 1, 1, 1, 1)
        self.pushButton_updatePort = QtWidgets.QPushButton(self.groupBox_serial)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.pushButton_updatePort.setFont(font)
        self.pushButton_updatePort.setObjectName("pushButton_updatePort")
        self.gridLayout_7.addWidget(self.pushButton_updatePort, 0, 0, 2, 1)
        self.gridLayout_8.addWidget(self.groupBox_serial, 1, 0, 1, 3)
        self.groupBox_flash = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_flash.setFont(font)
        self.groupBox_flash.setObjectName("groupBox_flash")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_flash)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_flash = QtWidgets.QLineEdit(self.groupBox_flash)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_flash.setFont(font)
        self.lineEdit_flash.setObjectName("lineEdit_flash")
        self.gridLayout_2.addWidget(self.lineEdit_flash, 0, 0, 1, 4)
        self.toolButton_flash = QtWidgets.QToolButton(self.groupBox_flash)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.toolButton_flash.setFont(font)
        self.toolButton_flash.setObjectName("toolButton_flash")
        self.gridLayout_2.addWidget(self.toolButton_flash, 0, 4, 1, 1)
        self.radioButton_flashRead = QtWidgets.QRadioButton(self.groupBox_flash)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.radioButton_flashRead.setFont(font)
        self.radioButton_flashRead.setAutoExclusive(False)
        self.radioButton_flashRead.setObjectName("radioButton_flashRead")
        self.gridLayout_2.addWidget(self.radioButton_flashRead, 1, 1, 1, 1)
        self.radioButton_flashWrite = QtWidgets.QRadioButton(self.groupBox_flash)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.radioButton_flashWrite.setFont(font)
        self.radioButton_flashWrite.setAutoExclusive(False)
        self.radioButton_flashWrite.setObjectName("radioButton_flashWrite")
        self.gridLayout_2.addWidget(self.radioButton_flashWrite, 1, 0, 1, 1)
        self.radioButton_flashVerify = QtWidgets.QRadioButton(self.groupBox_flash)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.radioButton_flashVerify.setFont(font)
        self.radioButton_flashVerify.setAutoExclusive(False)
        self.radioButton_flashVerify.setObjectName("radioButton_flashVerify")
        self.gridLayout_2.addWidget(self.radioButton_flashVerify, 1, 2, 1, 1)
        self.pushButton_flashGo = QtWidgets.QPushButton(self.groupBox_flash)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_flashGo.setFont(font)
        self.pushButton_flashGo.setObjectName("pushButton_flashGo")
        self.gridLayout_2.addWidget(self.pushButton_flashGo, 1, 3, 1, 2)
        self.gridLayout_8.addWidget(self.groupBox_flash, 2, 0, 2, 3)
        self.groupBox_eeprom = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_eeprom.setFont(font)
        self.groupBox_eeprom.setObjectName("groupBox_eeprom")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_eeprom)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_eeprom = QtWidgets.QLineEdit(self.groupBox_eeprom)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_eeprom.setFont(font)
        self.lineEdit_eeprom.setObjectName("lineEdit_eeprom")
        self.gridLayout_3.addWidget(self.lineEdit_eeprom, 0, 0, 1, 4)
        self.toolButton_eeprom = QtWidgets.QToolButton(self.groupBox_eeprom)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.toolButton_eeprom.setFont(font)
        self.toolButton_eeprom.setObjectName("toolButton_eeprom")
        self.gridLayout_3.addWidget(self.toolButton_eeprom, 0, 4, 1, 1)
        self.radioButton_eepromRead = QtWidgets.QRadioButton(self.groupBox_eeprom)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.radioButton_eepromRead.setFont(font)
        self.radioButton_eepromRead.setAutoExclusive(False)
        self.radioButton_eepromRead.setObjectName("radioButton_eepromRead")
        self.gridLayout_3.addWidget(self.radioButton_eepromRead, 1, 1, 1, 1)
        self.radioButton_eepromWrite = QtWidgets.QRadioButton(self.groupBox_eeprom)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.radioButton_eepromWrite.setFont(font)
        self.radioButton_eepromWrite.setAutoExclusive(False)
        self.radioButton_eepromWrite.setObjectName("radioButton_eepromWrite")
        self.gridLayout_3.addWidget(self.radioButton_eepromWrite, 1, 0, 1, 1)
        self.radioButton_eepromVerify = QtWidgets.QRadioButton(self.groupBox_eeprom)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.radioButton_eepromVerify.setFont(font)
        self.radioButton_eepromVerify.setAutoExclusive(False)
        self.radioButton_eepromVerify.setObjectName("radioButton_eepromVerify")
        self.gridLayout_3.addWidget(self.radioButton_eepromVerify, 1, 2, 1, 1)
        self.pushButton_eepromGo = QtWidgets.QPushButton(self.groupBox_eeprom)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_eepromGo.setFont(font)
        self.pushButton_eepromGo.setObjectName("pushButton_eepromGo")
        self.gridLayout_3.addWidget(self.pushButton_eepromGo, 1, 3, 1, 2)
        self.gridLayout_8.addWidget(self.groupBox_eeprom, 4, 0, 1, 3)
        self.groupBox_else = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_else.setFont(font)
        self.groupBox_else.setObjectName("groupBox_else")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_else)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.checkBox_cancelVerify = QtWidgets.QCheckBox(self.groupBox_else)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.checkBox_cancelVerify.setFont(font)
        self.checkBox_cancelVerify.setObjectName("checkBox_cancelVerify")
        self.gridLayout_6.addWidget(self.checkBox_cancelVerify, 0, 0, 1, 1)
        self.checkBox_eraseChip = QtWidgets.QCheckBox(self.groupBox_else)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.checkBox_eraseChip.setFont(font)
        self.checkBox_eraseChip.setObjectName("checkBox_eraseChip")
        self.gridLayout_6.addWidget(self.checkBox_eraseChip, 0, 1, 1, 1)
        self.label_additionalParameter = QtWidgets.QLabel(self.groupBox_else)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.label_additionalParameter.setFont(font)
        self.label_additionalParameter.setObjectName("label_additionalParameter")
        self.gridLayout_6.addWidget(self.label_additionalParameter, 1, 0, 1, 1)
        self.lineEdit_additionalParameter = QtWidgets.QLineEdit(self.groupBox_else)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_additionalParameter.setFont(font)
        self.lineEdit_additionalParameter.setObjectName("lineEdit_additionalParameter")
        self.gridLayout_6.addWidget(self.lineEdit_additionalParameter, 1, 1, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_else, 5, 0, 2, 3)
        self.pushButton_startProgram = QtWidgets.QPushButton(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_startProgram.setFont(font)
        self.pushButton_startProgram.setObjectName("pushButton_startProgram")
        self.gridLayout_8.addWidget(self.pushButton_startProgram, 7, 0, 1, 1)
        self.pushButton_stopProgram = QtWidgets.QPushButton(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_stopProgram.setFont(font)
        self.pushButton_stopProgram.setObjectName("pushButton_stopProgram")
        self.gridLayout_8.addWidget(self.pushButton_stopProgram, 7, 1, 1, 1)
        self.pushButton_bitSelector = QtWidgets.QPushButton(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_bitSelector.setFont(font)
        self.pushButton_bitSelector.setObjectName("pushButton_bitSelector")
        self.gridLayout_8.addWidget(self.pushButton_bitSelector, 7, 3, 1, 1)
        self.textBrowser_cmd = QtWidgets.QTextBrowser(MainWidgetAvrdude)
        self.textBrowser_cmd.setMinimumSize(QtCore.QSize(0, 20))
        self.textBrowser_cmd.setMaximumSize(QtCore.QSize(16777215, 20))
        self.textBrowser_cmd.setSizeIncrement(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(8)
        self.textBrowser_cmd.setFont(font)
        self.textBrowser_cmd.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.textBrowser_cmd.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_cmd.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_cmd.setObjectName("textBrowser_cmd")
        self.gridLayout_8.addWidget(self.textBrowser_cmd, 8, 0, 1, 4)
        self.textBrowser_cmdterminal = QtWidgets.QTextBrowser(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(8)
        self.textBrowser_cmdterminal.setFont(font)
        self.textBrowser_cmdterminal.setObjectName("textBrowser_cmdterminal")
        self.gridLayout_8.addWidget(self.textBrowser_cmdterminal, 9, 0, 1, 4)
        self.groupBox_mcu = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_mcu.setFont(font)
        self.groupBox_mcu.setObjectName("groupBox_mcu")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_mcu)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_mcuSelect = QtWidgets.QComboBox(self.groupBox_mcu)
        self.comboBox_mcuSelect.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.comboBox_mcuSelect.setFont(font)
        self.comboBox_mcuSelect.setObjectName("comboBox_mcuSelect")
        self.comboBox_mcuSelect.addItem("")
        self.comboBox_mcuSelect.addItem("")
        self.gridLayout.addWidget(self.comboBox_mcuSelect, 0, 0, 1, 2)
        self.pushButton_mcuDetect = QtWidgets.QPushButton(self.groupBox_mcu)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_mcuDetect.setFont(font)
        self.pushButton_mcuDetect.setObjectName("pushButton_mcuDetect")
        self.gridLayout.addWidget(self.pushButton_mcuDetect, 1, 0, 1, 2)
        self.gridLayout_8.addWidget(self.groupBox_mcu, 1, 3, 1, 1)
        self.groupBox_lock = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_lock.setFont(font)
        self.groupBox_lock.setObjectName("groupBox_lock")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_lock)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_lockTitle = QtWidgets.QLabel(self.groupBox_lock)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_lockTitle.setFont(font)
        self.label_lockTitle.setObjectName("label_lockTitle")
        self.gridLayout_5.addWidget(self.label_lockTitle, 0, 0, 1, 1)
        self.lineEdit_lock = QtWidgets.QLineEdit(self.groupBox_lock)
        self.lineEdit_lock.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_lock.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_lock.setBaseSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_lock.setFont(font)
        self.lineEdit_lock.setObjectName("lineEdit_lock")
        self.gridLayout_5.addWidget(self.lineEdit_lock, 0, 1, 1, 1)
        self.pushButton_lockWrite = QtWidgets.QPushButton(self.groupBox_lock)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_lockWrite.setFont(font)
        self.pushButton_lockWrite.setObjectName("pushButton_lockWrite")
        self.gridLayout_5.addWidget(self.pushButton_lockWrite, 1, 2, 1, 1)
        self.pushButton_lockRead = QtWidgets.QPushButton(self.groupBox_lock)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_lockRead.setFont(font)
        self.pushButton_lockRead.setObjectName("pushButton_lockRead")
        self.gridLayout_5.addWidget(self.pushButton_lockRead, 0, 2, 1, 1)
        self.checkBox_lockSet = QtWidgets.QCheckBox(self.groupBox_lock)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.checkBox_lockSet.setFont(font)
        self.checkBox_lockSet.setObjectName("checkBox_lockSet")
        self.gridLayout_5.addWidget(self.checkBox_lockSet, 1, 0, 1, 2)
        self.gridLayout_8.addWidget(self.groupBox_lock, 5, 3, 2, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(MainWidgetAvrdude)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_fuseRead = QtWidgets.QPushButton(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_fuseRead.setFont(font)
        self.pushButton_fuseRead.setObjectName("pushButton_fuseRead")
        self.gridLayout_4.addWidget(self.pushButton_fuseRead, 0, 2, 1, 1)
        self.lineEdit_fuseHigh = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_fuseHigh.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_fuseHigh.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_fuseHigh.setBaseSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_fuseHigh.setFont(font)
        self.lineEdit_fuseHigh.setObjectName("lineEdit_fuseHigh")
        self.gridLayout_4.addWidget(self.lineEdit_fuseHigh, 1, 1, 1, 1)
        self.label_fuseHigh = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_fuseHigh.setFont(font)
        self.label_fuseHigh.setObjectName("label_fuseHigh")
        self.gridLayout_4.addWidget(self.label_fuseHigh, 1, 0, 1, 1)
        self.pushButton_fuseWrite = QtWidgets.QPushButton(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.pushButton_fuseWrite.setFont(font)
        self.pushButton_fuseWrite.setObjectName("pushButton_fuseWrite")
        self.gridLayout_4.addWidget(self.pushButton_fuseWrite, 1, 2, 1, 1)
        self.label_fuseExtra = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_fuseExtra.setFont(font)
        self.label_fuseExtra.setObjectName("label_fuseExtra")
        self.gridLayout_4.addWidget(self.label_fuseExtra, 2, 0, 1, 1)
        self.lineEdit_fuseExtra = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_fuseExtra.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_fuseExtra.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_fuseExtra.setBaseSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_fuseExtra.setFont(font)
        self.lineEdit_fuseExtra.setObjectName("lineEdit_fuseExtra")
        self.gridLayout_4.addWidget(self.lineEdit_fuseExtra, 2, 1, 1, 1)
        self.label_fuseLow = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_fuseLow.setFont(font)
        self.label_fuseLow.setObjectName("label_fuseLow")
        self.gridLayout_4.addWidget(self.label_fuseLow, 0, 0, 1, 1)
        self.lineEdit_fuseLow = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_fuseLow.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_fuseLow.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_fuseLow.setBaseSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.lineEdit_fuseLow.setFont(font)
        self.lineEdit_fuseLow.setObjectName("lineEdit_fuseLow")
        self.gridLayout_4.addWidget(self.lineEdit_fuseLow, 0, 1, 1, 1)
        self.checkBox_fuseSet = QtWidgets.QCheckBox(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.checkBox_fuseSet.setFont(font)
        self.checkBox_fuseSet.setObjectName("checkBox_fuseSet")
        self.gridLayout_4.addWidget(self.checkBox_fuseSet, 3, 0, 1, 2)
        self.gridLayout_8.addWidget(self.groupBox_5, 2, 3, 3, 1)

        self.retranslateUi(MainWidgetAvrdude)
        QtCore.QMetaObject.connectSlotsByName(MainWidgetAvrdude)
        MainWidgetAvrdude.setTabOrder(self.comboBox_config, self.pushButton_configSave)
        MainWidgetAvrdude.setTabOrder(self.pushButton_configSave, self.pushButton_configDelete)
        MainWidgetAvrdude.setTabOrder(self.pushButton_configDelete, self.pushButton_updatePort)
        MainWidgetAvrdude.setTabOrder(self.pushButton_updatePort, self.comboBox_serialSetPort)
        MainWidgetAvrdude.setTabOrder(self.comboBox_serialSetPort, self.lineEdit_serialSetBaud)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_serialSetBaud, self.comboBox_mcuSelect)
        MainWidgetAvrdude.setTabOrder(self.comboBox_mcuSelect, self.pushButton_mcuDetect)
        MainWidgetAvrdude.setTabOrder(self.pushButton_mcuDetect, self.lineEdit_flash)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_flash, self.toolButton_flash)
        MainWidgetAvrdude.setTabOrder(self.toolButton_flash, self.radioButton_flashWrite)
        MainWidgetAvrdude.setTabOrder(self.radioButton_flashWrite, self.radioButton_flashRead)
        MainWidgetAvrdude.setTabOrder(self.radioButton_flashRead, self.radioButton_flashVerify)
        MainWidgetAvrdude.setTabOrder(self.radioButton_flashVerify, self.pushButton_flashGo)
        MainWidgetAvrdude.setTabOrder(self.pushButton_flashGo, self.lineEdit_eeprom)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_eeprom, self.toolButton_eeprom)
        MainWidgetAvrdude.setTabOrder(self.toolButton_eeprom, self.radioButton_eepromWrite)
        MainWidgetAvrdude.setTabOrder(self.radioButton_eepromWrite, self.radioButton_eepromRead)
        MainWidgetAvrdude.setTabOrder(self.radioButton_eepromRead, self.radioButton_eepromVerify)
        MainWidgetAvrdude.setTabOrder(self.radioButton_eepromVerify, self.pushButton_eepromGo)
        MainWidgetAvrdude.setTabOrder(self.pushButton_eepromGo, self.lineEdit_fuseLow)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_fuseLow, self.pushButton_fuseRead)
        MainWidgetAvrdude.setTabOrder(self.pushButton_fuseRead, self.lineEdit_fuseHigh)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_fuseHigh, self.pushButton_fuseWrite)
        MainWidgetAvrdude.setTabOrder(self.pushButton_fuseWrite, self.lineEdit_fuseExtra)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_fuseExtra, self.checkBox_fuseSet)
        MainWidgetAvrdude.setTabOrder(self.checkBox_fuseSet, self.checkBox_cancelVerify)
        MainWidgetAvrdude.setTabOrder(self.checkBox_cancelVerify, self.checkBox_eraseChip)
        MainWidgetAvrdude.setTabOrder(self.checkBox_eraseChip, self.lineEdit_additionalParameter)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_additionalParameter, self.lineEdit_lock)
        MainWidgetAvrdude.setTabOrder(self.lineEdit_lock, self.pushButton_lockRead)
        MainWidgetAvrdude.setTabOrder(self.pushButton_lockRead, self.checkBox_lockSet)
        MainWidgetAvrdude.setTabOrder(self.checkBox_lockSet, self.pushButton_lockWrite)
        MainWidgetAvrdude.setTabOrder(self.pushButton_lockWrite, self.pushButton_startProgram)
        MainWidgetAvrdude.setTabOrder(self.pushButton_startProgram, self.pushButton_stopProgram)
        MainWidgetAvrdude.setTabOrder(self.pushButton_stopProgram, self.pushButton_bitSelector)
        MainWidgetAvrdude.setTabOrder(self.pushButton_bitSelector, self.textBrowser_cmd)
        MainWidgetAvrdude.setTabOrder(self.textBrowser_cmd, self.textBrowser_cmdterminal)

    def retranslateUi(self, MainWidgetAvrdude):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_config.setTitle(_translate("MainWidgetAvrdude", "設定檔"))
        self.comboBox_config.setItemText(0, _translate("MainWidgetAvrdude", "選擇設定檔..."))
        self.pushButton_configSave.setText(_translate("MainWidgetAvrdude", "儲存"))
        self.pushButton_configDelete.setText(_translate("MainWidgetAvrdude", "刪除"))
        self.groupBox_serial.setTitle(_translate("MainWidgetAvrdude", "燒錄器設定"))
        self.label_serialSetPort.setText(_translate("MainWidgetAvrdude", "Port  (-P)"))
        self.label_serialSetBaud.setText(_translate("MainWidgetAvrdude", "Baud rate (-b)"))
        self.pushButton_updatePort.setText(_translate("MainWidgetAvrdude", "更新串列埠"))
        self.groupBox_flash.setTitle(_translate("MainWidgetAvrdude", "Flash"))
        self.toolButton_flash.setText(_translate("MainWidgetAvrdude", "..."))
        self.radioButton_flashRead.setText(_translate("MainWidgetAvrdude", "Read"))
        self.radioButton_flashWrite.setText(_translate("MainWidgetAvrdude", "Write"))
        self.radioButton_flashVerify.setText(_translate("MainWidgetAvrdude", "Verify"))
        self.pushButton_flashGo.setText(_translate("MainWidgetAvrdude", "Go"))
        self.groupBox_eeprom.setTitle(_translate("MainWidgetAvrdude", "EEPROM"))
        self.toolButton_eeprom.setText(_translate("MainWidgetAvrdude", "..."))
        self.radioButton_eepromRead.setText(_translate("MainWidgetAvrdude", "Read"))
        self.radioButton_eepromWrite.setText(_translate("MainWidgetAvrdude", "Write"))
        self.radioButton_eepromVerify.setText(_translate("MainWidgetAvrdude", "Verify"))
        self.pushButton_eepromGo.setText(_translate("MainWidgetAvrdude", "Go"))
        self.groupBox_else.setTitle(_translate("MainWidgetAvrdude", "其餘選項"))
        self.checkBox_cancelVerify.setText(_translate("MainWidgetAvrdude", "取消驗證"))
        self.checkBox_eraseChip.setText(_translate("MainWidgetAvrdude", "清除晶片"))
        self.label_additionalParameter.setText(_translate("MainWidgetAvrdude", "增加參數"))
        self.pushButton_startProgram.setText(_translate("MainWidgetAvrdude", "開始燒錄！"))
        self.pushButton_stopProgram.setText(_translate("MainWidgetAvrdude", "強制終止"))
        self.pushButton_bitSelector.setText(_translate("MainWidgetAvrdude", "BitSelector"))
        self.groupBox_mcu.setTitle(_translate("MainWidgetAvrdude", "MCU"))
        self.comboBox_mcuSelect.setItemText(0, _translate("MainWidgetAvrdude", "請選擇MCU..."))
        self.comboBox_mcuSelect.setItemText(1, _translate("MainWidgetAvrdude", "ATmega88"))
        self.pushButton_mcuDetect.setText(_translate("MainWidgetAvrdude", "偵測"))
        self.groupBox_lock.setTitle(_translate("MainWidgetAvrdude", "Fuse bits"))
        self.label_lockTitle.setText(_translate("MainWidgetAvrdude", "Lock"))
        self.pushButton_lockWrite.setText(_translate("MainWidgetAvrdude", "Write"))
        self.pushButton_lockRead.setText(_translate("MainWidgetAvrdude", "Read"))
        self.checkBox_lockSet.setText(_translate("MainWidgetAvrdude", "Set Lock bits"))
        self.groupBox_5.setTitle(_translate("MainWidgetAvrdude", "Fuse bits"))
        self.pushButton_fuseRead.setText(_translate("MainWidgetAvrdude", "Read"))
        self.label_fuseHigh.setText(_translate("MainWidgetAvrdude", "High"))
        self.pushButton_fuseWrite.setText(_translate("MainWidgetAvrdude", "Write"))
        self.label_fuseExtra.setText(_translate("MainWidgetAvrdude", "Extra"))
        self.label_fuseLow.setText(_translate("MainWidgetAvrdude", "Low"))
        self.checkBox_fuseSet.setText(_translate("MainWidgetAvrdude", "Set Fuse"))

