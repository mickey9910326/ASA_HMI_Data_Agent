from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog, QDialog
import scipy.io
import os.path
from ui_hmi_load_dialog import Ui_HmiLoadDialog
from decodeASAformat import *

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
    arrayList = list()

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.pushButton_load.clicked.connect(self.loadFile)
        self.pushButton_up.clicked.connect(self.colMoveUp)
        self.pushButton_down.clicked.connect(self.colMoveDown)
        self.pushButton_delete.clicked.connect(self.colDelete)
        self.pushButton_confirm.clicked.connect(self.confirm)
        self.show()

    def loadFile(self):
        # TODO load file
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File','', 'Mat Files (*.mat);;csv Files (*.csv)' ,initialFilter='Mat Files (*.mat)')
        if filename != '':
            name, extension = os.path.splitext(filename)
            self.loadMatFile(filename)

    def loadMatFile(self, filename):
        matDict = scipy.io.loadmat(filename)
        for key, val in matDict.items():
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
                    self.arrayList.append(val[0,:])
                    self.updateTableFromArrayList()

    def updateTableFromArrayList(self):
        self.tableWidget_mat.clearContents()
        self.tableWidget_mat.setRowCount(0)
        for array in self.arrayList:
            dataString = str()
            for i, data in enumerate(array):
                dataString += str(array[i])
                if i is not array.size-1:
                    dataString += ', '
            self.appendRow(str(array.dtype), str(array.size), str(array.nbytes), dataString)

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

    def confirm(self):
        # TODO check the data is OK
        self.accept()

    def colMoveUp(self):
        row = self.tableWidget_mat.currentRow()
        column = self.tableWidget_mat.currentColumn()
        if row > 0:
            tmp = self.arrayList[row]
            self.arrayList[row]   = self.arrayList[row-1]
            self.arrayList[row-1] = tmp
            self.updateTableFromArrayList()
            self.tableWidget_mat.setCurrentCell(row-1,column)

    def colMoveDown(self):
        row = self.tableWidget_mat.currentRow()
        column = self.tableWidget_mat.currentColumn()
        if row < self.tableWidget_mat.rowCount()-1:
            tmp = self.arrayList[row]
            self.arrayList[row]   = self.arrayList[row+1]
            self.arrayList[row+1] = tmp
            self.updateTableFromArrayList()
            self.tableWidget_mat.setCurrentCell(row+1,column)

    def colDelete(self):
        row = self.tableWidget_mat.currentRow()
        self.tableWidget_mat.removeRow(row)

    def getArrayListStr(self):
        return arrayListToStr(self.arrayList)

def arrayListToStr(arrayList):
    typeNums = len(arrayList)
    ret = str()
    for array in arrayList:
        ret += stdTypeToAsaType(str(array.dtype)) + ' : \n'
        dataNums = array.size
        dataString = str()
        for i, data in enumerate(array):
            dataString += str(array[i])
            if i is not dataNums-1:
                dataString += ', '
            if len(dataString) >= 100:
                ret += dataString + '\n'
                dataString = str()
        ret += dataString + '\n'
    return ret

def stdTypeToAsaType(typeStr):
    if typeStr == 'int8':
        return 'i8'
    elif typeStr == 'int16':
        return 'i16'
    elif typeStr == 'int32':
        return 'i32'
    elif typeStr == 'int64':
        return 'i64'
    elif typeStr == 'uint8':
        return 'ui8'
    elif typeStr == 'uint16':
        return 'ui16'
    elif typeStr == 'uint32':
        return 'ui32'
    elif typeStr == 'uint64':
        return 'ui64'
    elif typeStr == 'float32':
        return 'f32'
    elif typeStr == 'float64':
        return 'f64'
    else:
        return None
