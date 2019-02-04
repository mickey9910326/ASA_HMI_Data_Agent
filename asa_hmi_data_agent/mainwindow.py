import sys
import serial
import time

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from asa_hmi_data_agent.ui.ui_mainwindow import Ui_MainWindow
from asa_hmi_data_agent.ui.ui_hmi import Ui_MainWidgetHMI
from asa_hmi_data_agent.ui.ui_avrdude import Ui_MainWidgetAvrdude
from asa_hmi_data_agent.ui.ui_asa_prog import Ui_MainWidgetAsaProg

from asa_hmi_data_agent.hmi.hmi import HMI
from asa_hmi_data_agent.avrdude.avrdude import Avrdude
from asa_hmi_data_agent.asa_loader import AsaLoader
from asa_hmi_data_agent.socket_api import AdtSocketHandler
from asa_hmi_data_agent.adt_settings.adt_settings import AdtSettings

from asa_hmi_data_agent.listport import serial_ports

class MainWindow(QMainWindow, Ui_MainWindow):
    serToggle = pyqtSignal(bool, str)
    hmiSertIsTerminated = bool(False)

    # ---- __init__ start ------------------------------------------------------
    def __init__(self, parent=None):
        # ---- init ui start ---------------------------------------------------
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        widgetHmi = Ui_MainWidgetHMI()
        widgetHmi2 = Ui_MainWidgetHMI()
        widgetAvrdude = Ui_MainWidgetAvrdude()
        WidgetAsaProg = Ui_MainWidgetAsaProg()
        widgetHmi.setupUi(self.tabHmi_1)
        widgetHmi2.setupUi(self.tabHmi_2)
        widgetAvrdude.setupUi(self.tabAvrdude)
        WidgetAsaProg.setupUi(self.tabAsaProg)
        # ---- init ui end -----------------------------------------------------
        self.HMI = HMI(widgetHmi,self)
        self.HMI2 = HMI(widgetHmi2,self)
        self.tabHmi_2.hide()
        self.Avrdude = Avrdude(widgetAvrdude,self)
        self.asaLoader = AsaLoader(WidgetAsaProg,self)

        self.adtSettings = AdtSettings()
        self.adtSettings.setupUi(self.tabAdtSettings)
        self.adtSettings.init()
        self.adtSettings.signalTermNumApply.connect(self.ctlHmiTermNum)

        self.serToggle[bool, str].connect(self.serToggleHandler)

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
            availablePorts = serial_ports()
            if port in availablePorts:
                err = False
                msg = ''
                target.widget.s_portComboBox.clear()
                for p in availablePorts:
                    target.widget.s_portComboBox.addItem(p)
                target.widget.s_portComboBox.setCurrentIndex(availablePorts.index(port))
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
        self.asaLoader.widget.lineEdit_selectFile.setText(hexfile)
        availablePorts = serial_ports()
        if port in availablePorts:
            self.asaLoader.widget.comboBox_selectPort.clear()
            for p in availablePorts:
                self.asaLoader.widget.comboBox_selectPort.addItem(p)
            self.asaLoader.widget.comboBox_selectPort.setCurrentIndex(availablePorts.index(port))
            self.asaLoader.startProg()
            time.sleep(0.5)
            err = False
            msg = ''
            max = self.asaLoader.shellThread.loader.total_steps
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
            'times': self.asaLoader.shellThread.loader.times
        }
        self.adtSocketHandler.sendRes(res)
