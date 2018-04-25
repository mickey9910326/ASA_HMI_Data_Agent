import scipy.io
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from ui_hmi_save_dialog import Ui_HmiSaveDialog
import decodeASAformat as ds
import hmi.text_decoder as hmidecoder

import numpy as np
from numpy import array

# Reference : https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
# Reference : https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html

class Const:
    COL_NAME = 0
    COL_TYPE = 1
    COL_NUMS = 2
    COL_BYTE = 3
    COL_DATA = 4

# ---- class BitsSelector Start ------------------------------------------------
class HmiSaveDialog(QDialog, Ui_HmiSaveDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.pushButton_matClose.clicked.connect(self.accept)
        self.pushButton_matSave.clicked.connect(self.saveAsMat)

    def show(self):
        super(QDialog, self).show()

    def showAndLoadText(self, text):
        self.show()
        self.loadDataFromText(text)

    def loadDataFromText(self, text):
        resArrayNums, resTypeNumList, resDataListList, res = ds.decodeTextToStruct(text)
        print('-----------------------------------------')
        print(res)
        if(res is -1):
            pass
        else:
            self.tableWidget_mat.setRowCount(resArrayNums)
            for i in range(resArrayNums):
                typeNum = resTypeNumList[i]
                dataList = resDataListList[i]
                nums = len(dataList)
                bytes = nums * ds.getTypeSize(typeNum)
                dataListStr = ', '.join(str(x) for x in dataList)
                self.tableWidget_mat.setItem(i, Const.COL_NAME, QTableWidgetItem(''))
                self.tableWidget_mat.setItem(i, Const.COL_TYPE, QTableWidgetItem(hmidecoder.stdTypeStr(typeNum)))
                self.tableWidget_mat.setItem(i, Const.COL_NUMS, QTableWidgetItem(str(nums)))
                self.tableWidget_mat.setItem(i, Const.COL_BYTE, QTableWidgetItem(str(bytes)))
                self.tableWidget_mat.setItem(i, Const.COL_DATA, QTableWidgetItem(dataListStr))

    def appendArray(self):
        row = self.tableWidget_mat.rowCount() + 1
        self.tableWidget_mat.setRowCount(row)
        self.tableWidget_mat.setItem(row-1, Const.COL_NAME, QTableWidgetItem("ui8"))
        self.tableWidget_mat.setItem(row-1, Const.COL_TYPE, QTableWidgetItem("uint8"))
        self.tableWidget_mat.setItem(row-1, Const.COL_NUMS, QTableWidgetItem("5"))
        self.tableWidget_mat.setItem(row-1, Const.COL_BYTE, QTableWidgetItem("5"))
        self.tableWidget_mat.setItem(row-1, Const.COL_DATA, QTableWidgetItem("1,2,3,4,5"))
        # type = self.tableWidget_mat.itemAt(1, Const.COL_TYPE).text()
        # print('type' + type)

    def saveAsMat(self):
        type = self.tableWidget_mat.item(0, Const.COL_TYPE).text()
        dataStrList = self.tableWidget_mat.item(0, Const.COL_DATA).text().split(',')
        print('type' + type)
        if (
                type == 'int8'
                or type == 'int16'
                or type == 'int32'
                or type == 'int64'
                or type == 'uint8'
                or type == 'uint16'
                or type == 'uint32'
                or type == 'uint64'
            ):
                print('int')
                data = list(map(int, dataStrList))
                name, _ = QFileDialog.getSaveFileName(self, 'Save File','', 'All Files (*);;Mat Files (*.mat)' ,initialFilter='Mat Files (*.mat)')
                if name is not '':
                    scipy.io.savemat(name,{self.tableWidget_mat.item(1, Const.COL_NAME).text() : array(data, dtype=type)})
        elif (
                type == 'float32'
                or type == 'float64'
            ):
                print('float')
                data = list(map(float, dataStrList))
                print(data)
                name, _ = QFileDialog.getSaveFileName(self, 'Save File','', 'All Files (*);;Mat Files (*.mat)' ,initialFilter='Mat Files (*.mat)')
                if name is not '':
                    scipy.io.savemat(name,{self.tableWidget_mat.item(1, Const.COL_NAME).text() : array(data, dtype=type)})
        else :
            # TODO error msg
            pass
