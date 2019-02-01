import sys
import serial
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from asa_hmi_data_agent.ui.ui_mainwindow import Ui_MainWindow
from asa_hmi_data_agent.ui.ui_hmi import Ui_MainWidgetHMI
from asa_hmi_data_agent.ui.ui_avrdude import Ui_MainWidgetAvrdude
from asa_hmi_data_agent.ui.ui_asa_prog import Ui_MainWidgetAsaProg

from asa_hmi_data_agent.hmi.hmi import HMI
from asa_hmi_data_agent.avrdude.avrdude import Avrdude
from asa_hmi_data_agent.asaprog.asaprog import Asaprog
from asa_hmi_data_agent.socket_api import AdtSocketHandler
from asa_hmi_data_agent.adt_settings.adt_settings import AdtSettings

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
        self.Asaprog = Asaprog(WidgetAsaProg,self)

        self.adtSettings = AdtSettings()
        self.adtSettings.setupUi(self.tabAdtSettings)
        self.adtSettings.init()
        self.adtSettings.signalTermNumApply.connect(self.ctlHmiTermNum)

        self.serToggle[bool, str].connect(self.serToggleHandler)
        self.adtSocketHandler = AdtSocketHandler()
        self.adtSocketHandler.start()

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
