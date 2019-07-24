from asa_hmi_data_agent.ui.ui_adt_settings import Ui_MainWidgetAdtSettings
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog
from asa_hmi_data_agent.listport import getAvailableSerialPorts
from time import sleep
import serial
import math
import requests


class DownloadThread(QThread):
    sigStart = pyqtSignal(int) # max
    sigStepDone = pyqtSignal(int) #
    sigAllDone = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        r = requests.get(
            'https://github.com/mickey9910326/ASA_HMI_Data_Agent/releases/latest')
        tag = r.url.split('/')[-1]
        url = "https://github.com/mickey9910326/ASA_HMI_Data_Agent/releases/download/{}/ASA_HMI_Data_Agent_{}.zip".format(
            tag, tag
        )
        filename = "ASA_HMI_Data_Agent_{}.zip".format(tag)
        r = requests.get(url, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        block_size = 2048
        t = 0
        wrote = 0
        times = math.ceil(total_size//block_size)
        self.sigStart.emit(times)
                
        with open(filename, 'wb') as f:
            for data in r.iter_content(block_size):
                wrote = wrote + len(data)
                f.write(data)
                t = t + 1
                print("{}/{}".format(t, times))
                self.sigStepDone.emit(t)

        if total_size != 0 and wrote != total_size:
            print("ERROR, something went wrong")


class AdtSettings(QObject):
    widget = Ui_MainWidgetAdtSettings()
    signalTermNumApply = pyqtSignal(int)

    def __init__(self):
        super(AdtSettings, self).__init__()

    def setupUi(self, widget):
        self.widget.setupUi(widget)

    def init(self):
        self.dth = DownloadThread()
        self.widget.pushButton_termNumApply.clicked.connect(self.termNumApply)
        # self.widget.pushButton_download.clicked.connect(self.downloadLastestFile)
        self.widget.pushButton_download.clicked.connect(self.dth.start)
        self.dth.sigStart[int].connect(self.download_start)
        self.dth.sigStepDone[int].connect(
            self.widget.progressBar_download.setValue)

    def termNumApply(self):
        num = int(self.widget.comboBox_termNum.currentText())
        self.signalTermNumApply.emit(num)

    def download_start(self, times):
        self.widget.progressBar_download.setValue(0)
        self.widget.progressBar_download.setMaximum(times)
        print('ok')
