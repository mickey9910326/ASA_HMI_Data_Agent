from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog, QDialog
import scipy.io
import os.path
from ui_hmi_load_dialog import Ui_HmiLoadDialog

import numpy as np
from numpy import array

# Reference : https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
# Reference : https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html

class Const:
    COL_TYPE = 0
    COL_NUMS = 1
    COL_BYTE = 2
    COL_DATA = 3

# ---- class BitsSelector Start ------------------------------------------------
class HmiLoadDialog(QDialog, Ui_HmiLoadDialog):
    dataList = list()

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.pushButton_load.clicked.connect(self.loadFile)
        # self.pushButton_up.clicked.connect(self.accept)
        # self.pushButton_down.clicked.connect(self.accept)
        # self.pushButton_delete.clicked.connect(self.accept)
        # self.pushButton_confirm.clicked.connect(self.accept)
        self.show()

    def loadFile(self):
        # TODO load file
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File','', 'Mat Files (*.mat);;csv Files (*.csv)' ,initialFilter='Mat Files (*.mat)')
        name, extension = os.path.splitext(filename)
        self.loadMatFile(filename)

    def loadMatFile(self, filename):
        matDict = scipy.io.loadmat(filename)
        for key, val in matDict.items():
            print(val)
            print(type(val))
            if (
                    key == '__header__' or
                    key == '__version__' or
                    key == '__globals__'
                ):
                    pass
            else:
                y, nums = val.shape
                if(y is not 1):
                    # TODO ERROR msg
                    pass
                else:
                    dataString = str()
                    for i, data in enumerate(val[0,:]):
                        dataString += str(val[0,i])
                        if i is not nums-1:
                            dataString += ', '
                    self.appendRow(str(val.dtype), str(nums), str(val.nbytes), dataString)
                    self.dataList.append(val)



    def appendRow(self, typeStr, numStr, byteStr, dataStr):
        row = self.tableWidget_mat.rowCount() + 1
        self.tableWidget_mat.setRowCount(row)
        self.tableWidget_mat.setItem(row-1, Const.COL_TYPE, QTableWidgetItem(typeStr))
        self.tableWidget_mat.setItem(row-1, Const.COL_NUMS, QTableWidgetItem(numStr))
        self.tableWidget_mat.setItem(row-1, Const.COL_BYTE, QTableWidgetItem(byteStr))
        self.tableWidget_mat.setItem(row-1, Const.COL_DATA, QTableWidgetItem(dataStr))


    def loadDataFromText(self, str):
        # TODO
        pass

    def show(self):
        super(QDialog, self).show()
