from asa_hmi_data_agent.ui.ui_adt_settings import Ui_MainWidgetAdtSettings
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog
from asa_hmi_data_agent.listport import getAvailableSerialPorts
from time import sleep
import serial
import math

class AdtSettings(QObject):
    widget = Ui_MainWidgetAdtSettings()
    signalTermNumApply = pyqtSignal(int)

    def __init__(self):
        super(AdtSettings, self).__init__()

    def setupUi(self, widget):
        self.widget.setupUi(widget)

    def init(self):
        self.widget.pushButton_termNumApply.clicked.connect(self.termNumApply)

    def termNumApply(self):
        num = int(self.widget.comboBox_termNum.currentText())
        self.signalTermNumApply.emit(num)
