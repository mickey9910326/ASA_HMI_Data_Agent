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

class MainWindow(QMainWindow, Ui_MainWindow):
    serToggle = pyqtSignal(bool, str)
    hmiSertIsTerminated = bool(False)

    # ---- __init__ start ------------------------------------------------------
    def __init__(self, parent=None):
        # ---- init ui start ---------------------------------------------------
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        widgetHmi = Ui_MainWidgetHMI()
        widgetAvrdude = Ui_MainWidgetAvrdude()
        WidgetAsaProg = Ui_MainWidgetAsaProg()
        widgetHmi.setupUi(self.tabHmi)
        widgetAvrdude.setupUi(self.tabAvrdude)
        WidgetAsaProg.setupUi(self.tabAsaProg)
        # ---- init ui end -----------------------------------------------------
        self.HMI = HMI(widgetHmi,self)
        self.Avrdude = Avrdude(widgetAvrdude,self)
        self.Asaprog = Asaprog(WidgetAsaProg,self)

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
