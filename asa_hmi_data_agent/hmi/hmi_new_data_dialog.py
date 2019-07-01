import numpy as np
import scipy.io
import os.path
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from asa_hmi_data_agent.ui.ui_hmi_new_data_dialog import Ui_HmiNewDataDialog
from asa_hmi_data_agent.ui.ui_widget_hmi_new_sd import Ui_WidgeHmiNewStructData
from asa_hmi_data_agent.ui.ui_widget_hmi_new_sop import Ui_WidgeHmiNewStructOp
from .data_to_text import arToStr, stToStr, mtToStr
from ..hmipac.type import *


class SD(QtCore.QObject, Ui_WidgeHmiNewStructData):
    def __init__(self):
        QDialog.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)


class SOP(QtCore.QObject, Ui_WidgeHmiNewStructOp):
    def __init__(self):
        QDialog.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)


class HmiNewDataDialog(QDialog, Ui_HmiNewDataDialog):
    sigArrayAccept = pyqtSignal(np.ndarray)
    sigMatrixAccept = pyqtSignal(np.ndarray)
    sigStructAccept = pyqtSignal(np.ndarray)

    def __init__(self):
        QDialog.__init__(self)
        self.struct_init()
        self.setupUi(self)

        self.pushButton_mconfirm.clicked.connect(self.matrix_confirm)
        self.pushButton_aconfirm.clicked.connect(self.array_confirm)
        self.pushButton_sconfirm.clicked.connect(self.struct_confirm)
        self.pushButton_mconsel.clicked.connect(self.accept)
        self.pushButton_aconsel.clicked.connect(self.accept)
        self.pushButton_sconsel.clicked.connect(self.accept)
    
    def show(self):
        self.struct_update()
        super(QDialog, self).show()

    def matrix_confirm(self):
        try:
            fs = "{}_{}x{}".format(
                self.comboBox_mtype.currentText(),
                int(self.lineEdit_dim1.text()),
                int(self.lineEdit_dim2.text())
            )
            dt, shape = mtFs2Np(fs)
        except:
            pass
        else:
            self.sigMatrixAccept.emit(np.zeros(shape, dtype=dt))
            self.accept()
    
    def array_confirm(self):
        try:
            tn = typeStr2TypeNum(self.comboBox_atype.currentText())
            dt = typeNum2NpType(tn)
            shape = (int(self.lineEdit_anum.text()))
        except:
            pass
        else:
            self.sigArrayAccept.emit(np.zeros(shape, dtype=dt))
            self.accept()
    
    def struct_confirm(self):
        try:
            fs = ','.join(["{}_{}".format(
                sd.comboBox_type.currentText(),
                sd.lineEdit_num.text()
            )
                for sd in self.sd
            ])
            dt = fs2dt(fs)
        except:
            pass
        else:
            self.sigStructAccept.emit(np.zeros(dt.shape, dtype=dt))
            self.accept()

    def struct_init(self):
        self.sd = list()
        self.sop = list()
        self.sd.append(SD())
        self.sop.append(SOP())
        self.sd[0].row = 0
        self.sop[0].row = 0
        self.struct_sop_init(0)
    
    def struct_update(self):
        for i in range(self.gridLayout_struct.rowCount()-1)[::-1]:
            if self.gridLayout_struct.itemAtPosition(i+1, 0):
                self.gridLayout_struct.itemAtPosition(i+1, 0).widget().hide()
                self.gridLayout_struct.removeWidget(self.gridLayout_struct.itemAtPosition(i+1, 0).widget())
                self.gridLayout_struct.itemAtPosition(i+1, 1).widget().hide()
                self.gridLayout_struct.removeWidget(self.gridLayout_struct.itemAtPosition(i+1, 1).widget())
        for i in range(len(self.sd)):
            self.gridLayout_struct.addWidget(self.sd[i].widget, i+1, 1)
            self.gridLayout_struct.addWidget(self.sop[i].widget, i+1, 0)
            self.sd[i].widget.show()
            self.sop[i].widget.show()
            self.sd[i].row = i
            self.sop[i].row = i
    
    def struct_addRow(self, i):
        self.sd.insert(i+1, SD())
        self.sop.insert(i+1, SOP())
        self.sd[i+1].row = i+1
        self.sop[i+1].row = i+1
        self.struct_sop_init(i+1)
        self.struct_update()
    
    def struct_removeRow(self, i):
        if len(self.sd) == 1:
            return
        for k in range(len(self.sd)-i-1):
            self.sd[k+i].comboBox_type.setCurrentText(self.sd[k+i+1].comboBox_type.currentText())
            self.sd[k+i].lineEdit_num.setText(self.sd[k+i+1].lineEdit_num.text())
        self.sd = self.sd[:-1]
        self.sop = self.sop[:-1]
        self.struct_update()

    def struct_UpRow(self, i):
        if len(self.sd) == 1:
            return
        if i == 0:
            return
        a = self.sd[i].comboBox_type.currentText()
        b = self.sd[i].lineEdit_num.text()
        self.sd[i].comboBox_type.setCurrentText(self.sd[i-1].comboBox_type.currentText())
        self.sd[i].lineEdit_num.setText(self.sd[i-1].lineEdit_num.text())
        self.sd[i-1].comboBox_type.setCurrentText(a)
        self.sd[i-1].lineEdit_num.setText(b)

    def struct_DownRow(self, i):
        if len(self.sd) == 1:
            return
        if i == len(self.sd)-1:
            return
        a = self.sd[i].comboBox_type.currentText()
        b = self.sd[i].lineEdit_num.text()
        self.sd[i].comboBox_type.setCurrentText(self.sd[i+1].comboBox_type.currentText())
        self.sd[i].lineEdit_num.setText(self.sd[i+1].lineEdit_num.text())
        self.sd[i+1].comboBox_type.setCurrentText(a)
        self.sd[i+1].lineEdit_num.setText(b)

    def struct_sop_init(self, i):
        self.sop[i].pushButton_plus.clicked.connect(lambda: self.struct_addRow(self.sop[i].row))
        self.sop[i].pushButton_minus.clicked.connect(lambda: self.struct_removeRow(self.sop[i].row))
        self.sop[i].pushButton_up.clicked.connect(lambda: self.struct_UpRow(self.sop[i].row))
        self.sop[i].pushButton_down.clicked.connect(lambda: self.struct_DownRow(self.sop[i].row))

    def struct_clear(self):
        for i in range(self.gridLayout_struct.rowCount()-1):
            self.gridLayout_struct.itemAtPosition(i+1, 0).widget().hide()
            self.gridLayout_struct.removeWidget(self.gridLayout_struct.itemAtPosition(i+1, 0).widget())
            self.gridLayout_struct.itemAtPosition(i+1, 1).widget().hide()
            self.gridLayout_struct.removeWidget(self.gridLayout_struct.itemAtPosition(i+1, 1).widget())




