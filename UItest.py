import sys
import serial
from decodeASAformat import *
from pyqtwindow import Ui_MainWindow
from listport import serial_ports
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from ui_mainwindow import Ui_MainWindow
from ui_hmi import Ui_MainWidgetHMI
from ui_avrdude import Ui_MainWidgetAvrdude
from ui_asa_prog import Ui_MainWidgetAsaProg

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.widgetHmi = Ui_MainWidgetHMI()
        self.widgetAvrdude = Ui_MainWidgetAvrdude()
        self.WidgetAsaProg = Ui_MainWidgetAsaProg()
        self.widgetHmi.setupUi(self.tabHmi)
        self.widgetAvrdude.setupUi(self.tabAvrdude)
        self.WidgetAsaProg.setupUi(self.tabAsaProg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
