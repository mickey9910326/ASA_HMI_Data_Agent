import sys
import serial
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from ui_mainwindow import Ui_MainWindow
from ui_hmi import Ui_MainWidgetHMI
from ui_avrdude import Ui_MainWidgetAvrdude
from ui_asa_prog import Ui_MainWidgetAsaProg
from hmi import HMI
from avrdude import Avrdude
from asaprog import Asaprog

class MainWindow(QMainWindow, Ui_MainWindow):
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

    def file_open(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File','', 'All Files (*);;Text Files (*.txt)' ,initialFilter='Text Files (*.txt)')
        if name!='':
            file = open(name,'r')
            return file;
        else:
            return None
    def file_save(self,text):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File','', 'All Files (*);;Text Files (*.txt)' ,initialFilter='Text Files (*.txt)')
        if name == '':
            pass
        else:
            file = open(''.join(name),'w')
            file.write(text)
            file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
