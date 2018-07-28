import scipy.io
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem
from asa_hmi_data_agent.ui.ui_hmi_save_dialog import Ui_HmiSaveDialog
# import asa_hmi_data_agent.hmi.decodeASAformat as ds
# import asa_hmi_data_agent.hmi.text_decoder as hmidecoder
# import ..hmipac

import numpy as np
from numpy import array
from .text_to_data import textToData
from ..hmipac.type import *

# Reference : https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
# Reference : https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html

class Const:
    COL_NAME = 0
    COL_TYPE = 1
    COL_NUMS = 2
    COL_SIZE = 3

# ---- class BitsSelector Start ------------------------------------------------
class HmiSaveDialog(QDialog, Ui_HmiSaveDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.pushButton_txtClose.clicked.connect(self.accept)
        self.pushButton_txtSave.clicked.connect(self.saveAsTxt)
        self.pushButton_matClose.clicked.connect(self.accept)
        self.pushButton_matSave.clicked.connect(self.saveAsMat)
        self.dataList = list()

    def show(self):
        super(QDialog, self).show()

    def showAndLoadText(self, text):
        self.show()
        self.loadDataFromText(text)

    def loadDataFromText(self, text):
        # tab_txt
        self.textEdit_txt.append(text)

        # tab_mat
        try:
            self.dataList = textToData(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            # TODO ERROR Dialog
            print(type(e))
            self.accept()
            pass
        else:
            self.tableWidget_mat.setRowCount(len(self.dataList))
            for i in range(len(self.dataList)):
                data = self.dataList[i]
                nameStr = 'data' + str(i)
                if data.shape is ():
                    # Struct
                    typeStr = getFs(data.dtype)
                    numsStr = '1'
                    sizeStr = str(data.dtype.itemsize)
                else:
                    # Array
                    typeStr = getTypeStr(getTypeNum(data.dtype.name))
                    numsStr = str(data.size)
                    sizeStr = str(data.size * data.dtype.itemsize)

                nameItem = QTableWidgetItem(nameStr)
                typeItem = QTableWidgetItem(typeStr)
                numsItem = QTableWidgetItem(numsStr)
                sizeItem = QTableWidgetItem(sizeStr)
                # nameItem.setFlags(QtCore.Qt.ItemIsEnabled)
                typeItem.setFlags(QtCore.Qt.ItemIsEnabled)
                numsItem.setFlags(QtCore.Qt.ItemIsEnabled)
                sizeItem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget_mat.setItem(i, Const.COL_NAME, nameItem)
                self.tableWidget_mat.setItem(i, Const.COL_TYPE, typeItem)
                self.tableWidget_mat.setItem(i, Const.COL_NUMS, numsItem)
                self.tableWidget_mat.setItem(i, Const.COL_SIZE, sizeItem)

    def saveAsMat(self):
        d = dict()
        for i in range(len(self.dataList)):
            name = self.tableWidget_mat.item(i, Const.COL_NAME).text()
            data = self.dataList[i]
            d[name] = data

        name, _ = QFileDialog.getSaveFileName(self, 'Save File','', 'All Files (*);;Mat Files (*.mat)' ,initialFilter='Mat Files (*.mat)')
        if name is not '':
            scipy.io.savemat(name, d)

    def saveAsTxt(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File','', 'All Files (*);;txt Files (*.txt)' ,initialFilter='txt Files (*.txt)')
        if name is not '':
            with open(name, 'w') as f:
                f.write(self.textEdit_txt.toPlainText())
