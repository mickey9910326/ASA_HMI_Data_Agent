import scipy.io
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from asa_hmi_data_agent.ui.ui_hmi_save_dialog import Ui_HmiSaveDialog
import asa_hmi_data_agent.hmi.decodeASAformat as ds
import asa_hmi_data_agent.hmi.text_decoder as hmidecoder

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

    def saveAsMat(self):
        data = dict()
        for row in range(self.tableWidget_mat.rowCount()):
            type = self.tableWidget_mat.item(row, Const.COL_TYPE).text()
            dataStr = self.tableWidget_mat.item(row, Const.COL_DATA).text()
            name = self.tableWidget_mat.item(row, Const.COL_NAME).text()
            data[name] = np.fromstring(dataStr, dtype=type, sep=',')

        name, _ = QFileDialog.getSaveFileName(self, 'Save File','', 'All Files (*);;Mat Files (*.mat)' ,initialFilter='Mat Files (*.mat)')
        if name is not '':
            scipy.io.savemat(name, data)
