import numpy as np
import scipy.io
import os.path
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from asa_hmi_data_agent.ui.ui_hmi_load_dialog import Ui_HmiLoadDialog
from .data_to_text import arToStr, stToStr, mtToStr
from ..hmipac.type import *

# Reference : https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
# Reference : https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html

class Const:
    COL_NEWSQE = 0
    COL_NAME = 1
    COL_TYPE = 2
    COL_NUMS = 3
    COL_SIZE = 4

# ---- class BitsSelector Start ------------------------------------------------
class HmiLoadDialog(QDialog, Ui_HmiLoadDialog):
    dataList = list()
    nameList = list()
    resText  = str()
    filename = str()

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.pushButton_txtLoad.clicked.connect(self.loadTxtFile)
        self.pushButton_matLoad.clicked.connect(self.loadMatFile)
        self.pushButton_confirm.clicked.connect(self.matConfirm)

        self.pushButton_up.clicked.connect(self.colMoveUp)
        self.pushButton_down.clicked.connect(self.colMoveDown)
        self.pushButton_delete.clicked.connect(self.colDelete)
        self.pushButton_newSeq.clicked.connect(self.applyNewSeq)

    def show(self):
        self.tableWidget_mat.setRowCount(0)
        self.dataList = list()
        self.resText  = ''
        super(QDialog, self).show()

    def matConfirm(self):
        self.updateTextFromDataList()
        self.accept()

    def loadTxtFile(self):
        # TODO load file
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File','', 'All Files (*);;txt Files (*.txt);;' ,initialFilter='txt Files (*.txt)')
        if filename != '':
            with open(filename, 'r') as f:
                self.filename = filename
                self.resText = '// load from txt file: ' + filename + '\n\n'
                self.resText += f.read()
            self.accept()

    def loadMatFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File','', 'All Files (*);;Mat Files (*.mat);;' ,initialFilter='Mat Files (*.mat)')
        if filename == '':
            return
        else:
            matDict = scipy.io.loadmat(filename)
            self.filename = filename
            self.dataList = list()
        for key, val in matDict.items():
            if (
                    key == '__header__' or
                    key == '__version__' or
                    key == '__globals__'
                ):
                    pass
            else:
                self.dataList.append(val)
                self.nameList.append(key)
        for i in range(len(self.dataList)):
            if len(self.dataList[i].shape) == 2:
                #matrix
                self.dataList[i] = self.dataList[i]
            elif self.dataList[i].dtype.names is None:
                # array
                self.dataList[i] = self.dataList[i][0]
            else:
                # struct
                self.dataList[i] = reStructureData(self.dataList[i])
        self.updateTableFromDataList()
        print(self.dataList)

    def updateTableFromDataList(self):
        self.tableWidget_mat.clearContents()
        self.tableWidget_mat.setRowCount(len(self.dataList))
        for row in range(len(self.dataList)):
            data = self.dataList[row]
            print(data)
            nameStr = self.nameList[row]
            # NOTE the structured data of loadmat's return is strange.
            if data.shape is ():
                # Struct
                typeStr = getFs(data.dtype)
                numsStr = '1'
                sizeStr = str(data.dtype.itemsize)
            elif len(data.shape) == 2:
                typeStr = np2MtFs(data.dtype, data.shape)
                numsStr = '1'
                sizeStr = str(data.size * data.dtype.itemsize)
            else:
                # Array
                typeStr = getTypeStr(getTypeNum(data.dtype.name))
                numsStr = str(data.size)
                sizeStr = str(data.size * data.dtype.itemsize)

            nameItem = QTableWidgetItem(nameStr)
            typeItem = QTableWidgetItem(typeStr)
            numsItem = QTableWidgetItem(numsStr)
            sizeItem = QTableWidgetItem(sizeStr)
            nameItem.setFlags(QtCore.Qt.ItemIsEnabled)
            typeItem.setFlags(QtCore.Qt.ItemIsEnabled)
            numsItem.setFlags(QtCore.Qt.ItemIsEnabled)
            sizeItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget_mat.setItem(row, Const.COL_NAME, nameItem)
            self.tableWidget_mat.setItem(row, Const.COL_TYPE, typeItem)
            self.tableWidget_mat.setItem(row, Const.COL_NUMS, numsItem)
            self.tableWidget_mat.setItem(row, Const.COL_SIZE, sizeItem)

    def updateTextFromDataList(self):
        if len(self.dataList) == 0:
            self.resText = ''
            return
        self.resText = '// load from mat file: ' + self.filename + '\n\n'
        for i, data in enumerate(self.dataList):
            if len(data.shape) == 2:
                self.resText += mtToStr(data)
            elif data.shape is ():
                self.resText += stToStr(data)
            else:
                self.resText += arToStr(data)
            if i != len(self.dataList)-1:
                self.resText += '\n'

    def colMoveUp(self):
        row = self.tableWidget_mat.currentRow()
        column = self.tableWidget_mat.currentColumn()
        if row > 0:
            tmp1 = self.dataList[row]
            tmp2 = self.nameList[row]
            self.dataList[row]   = self.dataList[row-1]
            self.nameList[row]   = self.nameList[row-1]
            self.dataList[row-1] = tmp1
            self.nameList[row-1] = tmp2
            self.updateTableFromDataList()
            self.tableWidget_mat.setCurrentCell(row-1,column)

    def colMoveDown(self):
        row = self.tableWidget_mat.currentRow()
        column = self.tableWidget_mat.currentColumn()
        if row < self.tableWidget_mat.rowCount()-1:
            tmp1 = self.dataList[row]
            tmp2 = self.nameList[row]
            self.dataList[row]   = self.dataList[row+1]
            self.nameList[row]   = self.nameList[row+1]
            self.dataList[row+1] = tmp1
            self.nameList[row+1] = tmp2
            self.updateTableFromDataList()
            self.tableWidget_mat.setCurrentCell(row+1,column)

    def colDelete(self):
        if len(self.dataList) == 0:
            return
        row = self.tableWidget_mat.currentRow()
        self.dataList.pop(row)
        self.nameList.pop(row)
        self.updateTableFromDataList()

    def applyNewSeq(self):
        cntRows = self.tableWidget_mat.rowCount()
        # check seq
        for row in range(cntRows):
            try:
                d = int(self.tableWidget_mat.item(row, Const.COL_NEWSQE).text())
            except ValueError:
                return
            if d < 1 or d > cntRows:
                return

        newDataList = list(self.dataList)
        newNameList = list(self.nameList)
        for row in range(cntRows):
            newIdx = int(self.tableWidget_mat.item(row, Const.COL_NEWSQE).text())-1
            newDataList[newIdx] = self.dataList[row]
            newNameList[newIdx] = self.nameList[row]
        self.dataList = newDataList
        self.nameList = newNameList
        self.updateTableFromDataList()

def reStructureData(data):
    f = data.dtype.names
    args = list() # args for new dtype
    dataList = list()
    for i in range(len(f)):
        d = data[f[i]][0][0][0]
        dataList.append(d)
        type = d.dtype.base
        num  = d.size
        args.append(('f'+str(i), type, (num,)))
    return np.array(tuple(dataList), args)
