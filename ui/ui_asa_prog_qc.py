# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/asa_prog_qc.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidgetAsaProgQc(object):
    def setupUi(self, MainWidgetAsaProgQc):
        MainWidgetAsaProgQc.setObjectName("MainWidgetAsaProgQc")
        MainWidgetAsaProgQc.resize(500, 700)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        MainWidgetAsaProgQc.setFont(font)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(MainWidgetAsaProgQc)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_basicFuns = QtWidgets.QGroupBox(MainWidgetAsaProgQc)
        self.groupBox_basicFuns.setObjectName("groupBox_basicFuns")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_basicFuns)
        self.gridLayout.setObjectName("gridLayout")
        self.label_inputNum = QtWidgets.QLabel(self.groupBox_basicFuns)
        self.label_inputNum.setObjectName("label_inputNum")
        self.gridLayout.addWidget(self.label_inputNum, 1, 0, 1, 1)
        self.lineEdit_num = QtWidgets.QLineEdit(self.groupBox_basicFuns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_num.sizePolicy().hasHeightForWidth())
        self.lineEdit_num.setSizePolicy(sizePolicy)
        self.lineEdit_num.setObjectName("lineEdit_num")
        self.gridLayout.addWidget(self.lineEdit_num, 1, 1, 1, 1)
        self.lineEdit_selectFile = QtWidgets.QLineEdit(self.groupBox_basicFuns)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.lineEdit_selectFile.setFont(font)
        self.lineEdit_selectFile.setObjectName("lineEdit_selectFile")
        self.gridLayout.addWidget(self.lineEdit_selectFile, 2, 0, 1, 1)
        self.pushButton_selectFile = QtWidgets.QPushButton(self.groupBox_basicFuns)
        self.pushButton_selectFile.setObjectName("pushButton_selectFile")
        self.gridLayout.addWidget(self.pushButton_selectFile, 2, 1, 1, 1)
        self.label_steps = QtWidgets.QLabel(self.groupBox_basicFuns)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        self.label_steps.setFont(font)
        self.label_steps.setObjectName("label_steps")
        self.gridLayout.addWidget(self.label_steps, 4, 0, 1, 3)
        self.pushButton_startProg = QtWidgets.QPushButton(self.groupBox_basicFuns)
        self.pushButton_startProg.setObjectName("pushButton_startProg")
        self.gridLayout.addWidget(self.pushButton_startProg, 3, 0, 1, 1)
        self.pushButton_stopProg = QtWidgets.QPushButton(self.groupBox_basicFuns)
        self.pushButton_stopProg.setObjectName("pushButton_stopProg")
        self.gridLayout.addWidget(self.pushButton_stopProg, 3, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_basicFuns)
        self.groupBox_status = QtWidgets.QGroupBox(MainWidgetAsaProgQc)
        self.groupBox_status.setObjectName("groupBox_status")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_status)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_status)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_statusTitle = QtWidgets.QLabel(self.groupBox_status)
        self.label_statusTitle.setObjectName("label_statusTitle")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_statusTitle)
        self.label_programSizeTitle = QtWidgets.QLabel(self.groupBox_status)
        self.label_programSizeTitle.setObjectName("label_programSizeTitle")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_programSizeTitle)
        self.label_programSizeContent = QtWidgets.QLabel(self.groupBox_status)
        self.label_programSizeContent.setObjectName("label_programSizeContent")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_programSizeContent)
        self.label_etcTitle = QtWidgets.QLabel(self.groupBox_status)
        self.label_etcTitle.setObjectName("label_etcTitle")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_etcTitle)
        self.label_etcContent = QtWidgets.QLabel(self.groupBox_status)
        self.label_etcContent.setObjectName("label_etcContent")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_etcContent)
        self.label_statusContent = QtWidgets.QLabel(self.groupBox_status)
        self.label_statusContent.setObjectName("label_statusContent")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_statusContent)
        self.label_progedNum = QtWidgets.QLabel(self.groupBox_status)
        self.label_progedNum.setObjectName("label_progedNum")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_progedNum)
        self.label_progedNumContent = QtWidgets.QLabel(self.groupBox_status)
        self.label_progedNumContent.setObjectName("label_progedNumContent")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_progedNumContent)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setVerticalSpacing(6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_dut0Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut0Title.setObjectName("label_dut0Title")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_dut0Title)
        self.label_dut0Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut0Content.setObjectName("label_dut0Content")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_dut0Content)
        self.label_dut1Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut1Title.setObjectName("label_dut1Title")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_dut1Title)
        self.label_dut1Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut1Content.setObjectName("label_dut1Content")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_dut1Content)
        self.label_dut2Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut2Title.setObjectName("label_dut2Title")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_dut2Title)
        self.label_dut2Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut2Content.setObjectName("label_dut2Content")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_dut2Content)
        self.label_dut3Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut3Title.setObjectName("label_dut3Title")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_dut3Title)
        self.label_dut3Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut3Content.setObjectName("label_dut3Content")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_dut3Content)
        self.label_dut4Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut4Title.setObjectName("label_dut4Title")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_dut4Title)
        self.label_dut4Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut4Content.setObjectName("label_dut4Content")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_dut4Content)
        self.label_dut5Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut5Title.setObjectName("label_dut5Title")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_dut5Title)
        self.label_dut5Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut5Content.setObjectName("label_dut5Content")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.label_dut5Content)
        self.horizontalLayout.addLayout(self.formLayout_3)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setVerticalSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_dut6Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut6Title.setObjectName("label_dut6Title")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_dut6Title)
        self.label_dut6Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut6Content.setObjectName("label_dut6Content")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_dut6Content)
        self.label_dut7Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut7Title.setObjectName("label_dut7Title")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_dut7Title)
        self.label_dut7Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut7Content.setObjectName("label_dut7Content")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_dut7Content)
        self.label_dut8Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut8Title.setObjectName("label_dut8Title")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_dut8Title)
        self.label_dut8Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut8Content.setObjectName("label_dut8Content")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_dut8Content)
        self.label_dut9Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut9Title.setObjectName("label_dut9Title")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_dut9Title)
        self.label_dut9Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut9Content.setObjectName("label_dut9Content")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_dut9Content)
        self.label_dut10Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut10Title.setObjectName("label_dut10Title")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_dut10Title)
        self.label_dut10Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut10Content.setObjectName("label_dut10Content")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_dut10Content)
        self.label_dut11Title = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut11Title.setObjectName("label_dut11Title")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_dut11Title)
        self.label_dut11Content = QtWidgets.QLabel(self.groupBox_status)
        self.label_dut11Content.setObjectName("label_dut11Content")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.label_dut11Content)
        self.horizontalLayout.addLayout(self.formLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.groupBox_status)

        self.retranslateUi(MainWidgetAsaProgQc)
        QtCore.QMetaObject.connectSlotsByName(MainWidgetAsaProgQc)

    def retranslateUi(self, MainWidgetAsaProgQc):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_basicFuns.setTitle(_translate("MainWidgetAsaProgQc", "燒錄設定"))
        self.label_inputNum.setText(_translate("MainWidgetAsaProgQc", "輸入燒錄數量："))
        self.pushButton_selectFile.setText(_translate("MainWidgetAsaProgQc", "選擇檔案"))
        self.label_steps.setText(_translate("MainWidgetAsaProgQc", "<html><head/><body><p><br/></p><p><br/></p><p><br/></p><p><br/></p></body></html>"))
        self.pushButton_startProg.setText(_translate("MainWidgetAsaProgQc", "開始連續燒錄"))
        self.pushButton_stopProg.setText(_translate("MainWidgetAsaProgQc", "強制終止"))
        self.groupBox_status.setTitle(_translate("MainWidgetAsaProgQc", "燒錄狀態"))
        self.label_statusTitle.setText(_translate("MainWidgetAsaProgQc", "當前狀態："))
        self.label_programSizeTitle.setText(_translate("MainWidgetAsaProgQc", "程式大小："))
        self.label_programSizeContent.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_etcTitle.setText(_translate("MainWidgetAsaProgQc", "預估花費時間："))
        self.label_etcContent.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_statusContent.setText(_translate("MainWidgetAsaProgQc", "等待燒錄"))
        self.label_progedNum.setText(_translate("MainWidgetAsaProgQc", "已燒錄數量："))
        self.label_progedNumContent.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut0Title.setText(_translate("MainWidgetAsaProgQc", "裝置0  ："))
        self.label_dut0Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut1Title.setText(_translate("MainWidgetAsaProgQc", "裝置1  ："))
        self.label_dut1Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut2Title.setText(_translate("MainWidgetAsaProgQc", "裝置2  ："))
        self.label_dut2Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut3Title.setText(_translate("MainWidgetAsaProgQc", "裝置3  ："))
        self.label_dut3Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut4Title.setText(_translate("MainWidgetAsaProgQc", "裝置4  ："))
        self.label_dut4Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut5Title.setText(_translate("MainWidgetAsaProgQc", "裝置5  ："))
        self.label_dut5Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut6Title.setText(_translate("MainWidgetAsaProgQc", "裝置6  ："))
        self.label_dut6Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut7Title.setText(_translate("MainWidgetAsaProgQc", "裝置7  ："))
        self.label_dut7Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut8Title.setText(_translate("MainWidgetAsaProgQc", "裝置8  ："))
        self.label_dut8Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut9Title.setText(_translate("MainWidgetAsaProgQc", "裝置9  ："))
        self.label_dut9Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut10Title.setText(_translate("MainWidgetAsaProgQc", "裝置10 ："))
        self.label_dut10Content.setText(_translate("MainWidgetAsaProgQc", "-"))
        self.label_dut11Title.setText(_translate("MainWidgetAsaProgQc", "裝置11 ："))
        self.label_dut11Content.setText(_translate("MainWidgetAsaProgQc", "-"))

