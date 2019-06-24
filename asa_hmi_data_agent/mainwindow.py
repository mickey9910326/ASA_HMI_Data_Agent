from asa_hmi_data_agent.ui.ui_mainwindow import Ui_MainWindow

from asa_hmi_data_agent.adt_settings.adt_settings import AdtSettings
from asa_hmi_data_agent.listport import getAvailableSerialPorts
from asa_hmi_data_agent.socket_api import AdtSocketHandler
from asa_hmi_data_agent.asaloader import AsaLoader
from asa_hmi_data_agent.avrdude import Avrdude
from asa_hmi_data_agent.hmi import HMI

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

import serial
import time
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    hmiSertIsTerminated = bool(False)

    # ---- __init__ start ------------------------------------------------------
    def __init__(self, parent=None):
        # ---- init ui start ---------------------------------------------------
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # ---- init ui end -----------------------------------------------------
        self.HMI = HMI(self.tabHmi_1)
        self.HMI.sigChangeWindowTitle.connect(
            lambda s: self.setWindowTitle(s)
        )

        self.HMI2 = HMI(self.tabHmi_2)
        self.tabHmi_2.hide()

        self.avrdude = Avrdude(self.tabAvrdude)
        self.avrdude.sigSerialPortCheck[bool, str].connect(self.serToggleHandler)

        self.asaLoader = AsaLoader(self.tabAsaProg)
        self.asaLoader.sigSerialPortCheck[bool, str].connect(self.serToggleHandler)

        self.adtSettings = AdtSettings()
        self.adtSettings.setupUi(self.tabAdtSettings)
        self.adtSettings.init()
        self.adtSettings.signalTermNumApply.connect(self.ctlHmiTermNum)

        self.adtSocketHandler = AdtSocketHandler()
        self.adtSocketHandler.signalTermOpen[int, str, int].connect(self.ctlHmiTermOpen)
        self.adtSocketHandler.signalTermClose[int].connect(self.ctlHmiTermClose)
        self.adtSocketHandler.signalTermClear[int].connect(self.ctlHmiTermClear)
        self.adtSocketHandler.signalLoaderStart[str, str].connect(self.ctlLoaderStart)
        self.adtSocketHandler.signalLoaderState.connect(self.ctlLoaderState)

    # --------------------------------------------------------------------------
    def serToggleHandler(self, b, port):
        if(
            b
            and self.HMI.ser.isOpen()
            and self.HMI.ser.port == port
        ):
            self.HMI.s_portToggle()
            self.hmiSertIsTerminated = True
        elif(
            b is False
            and self.hmiSertIsTerminated
            and not self.HMI.ser.isOpen()
            and self.HMI.ser.port == port
        ):
            self.HMI.s_portToggle()
            self.hmiSertIsTerminated = False

    def ctlHmiTermNum(self, num):
        if num is 1:
            self.tabHmi_2.hide()
        elif num is 2:
            self.tabHmi_2.show()

    def ctlHmiTermOpen(self, id, port, baudrate):
        if id is 1:
            target = self.HMI
            isHidden = self.tabHmi_1.isHidden()
        elif id is 2:
            target = self.HMI2
            isHidden = self.tabHmi_2.isHidden()

        if isHidden:
            err = True
            msg = 'Terminal {} is not available now, plz open it at adt tab settings'.format(id)
        elif target.ser.isOpen():
            err = True
            msg = 'Terminal {} has been opened.'.format(id)
        else:
            availablePorts = getAvailableSerialPorts()
            if port in availablePorts:
                err = False
                msg = ''
                target.ui.s_portComboBox.clear()
                for p in availablePorts:
                    target.ui.s_portComboBox.addItem(p)
                target.ui.s_portComboBox.setCurrentIndex(availablePorts.index(port))
                target.ser.baudrate = baudrate
                target.s_portToggle()
            else:
                err = True
                msg = 'port {} is not available.'.format(port)
        res = { 'err' : err, 'msg' : msg }
        self.adtSocketHandler.sendRes(res)

    def ctlHmiTermClose(self, id):
        if id is 1:
            target = self.HMI
            isHidden = self.tabHmi_1.isHidden()
        elif id is 2:
            target = self.HMI2
            isHidden = self.tabHmi_2.isHidden()

        if isHidden:
            err = True
            msg = 'Terminal {} is not available now, plz open it at adt tab settings'.format(id)
        elif target.ser.isOpen() is False:
            err = True
            msg = 'Terminal {} has been closed.'.format(id)
        else:
            err = False
            msg = ''
            target.s_portToggle()
        res = { 'err' : err, 'msg' : msg }
        self.adtSocketHandler.sendRes(res)

    def ctlHmiTermClear(self, id):
        if id is 1:
            target = self.HMI
            isHidden = self.tabHmi_1.isHidden()
        elif id is 2:
            target = self.HMI2
            isHidden = self.tabHmi_2.isHidden()

        if isHidden:
            err = True
            msg = 'Terminal {} is not available now, plz open it at adt tab settings'.format(id)
        else:
            err = False
            msg = ''
            target.text_terminalClear()
        res = { 'err' : err, 'msg' : msg }
        self.adtSocketHandler.sendRes(res)

    # --------------------------------------------------------------------------
    def ctlLoaderStart(self, port, hexfile):
        self.asaLoader.ui.lineEdit_selectFile.setText(hexfile)
        availablePorts = getAvailableSerialPorts()
        if port in availablePorts:
            self.asaLoader.ui.comboBox_selectPort.clear()
            for p in availablePorts:
                self.asaLoader.ui.comboBox_selectPort.addItem(p)
            self.asaLoader.ui.comboBox_selectPort.setCurrentIndex(availablePorts.index(port))
            self.asaLoader.startLoad()
            time.sleep(0.5) # wait loader get total_steps done
            err = False
            msg = ''
            max = self.asaLoader.loaderThread.loader.total_steps
        else:
            err = True
            msg = 'port {} is not available.'.format(port)
            max = 0
        res = {
            'err': err,
            'msg': msg,
            'max': max
        }
        self.adtSocketHandler.sendRes(res)

    def ctlLoaderState(self):
        res = {
            'err': False,
            'msg': '',
            'times': self.asaLoader.loaderThread.loader.times
        }
        self.adtSocketHandler.sendRes(res)
