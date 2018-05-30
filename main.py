import sys
import serial
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QCoreApplication

from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_hmi import Ui_MainWidgetHMI
from ui.ui_avrdude import Ui_MainWidgetAvrdude
from ui.ui_asa_prog import Ui_MainWidgetAsaProg
from ui.ui_asa_prog_qc import Ui_MainWidgetAsaProgQc

from hmi.hmi import HMI
from avrdude.avrdude import Avrdude
from asaprog.asaprog import Asaprog
from asaprogqc.asaprogqc import AsaprogQc

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

        self.AddAsaProgQcTab()
        WidgetAsaProgQc = Ui_MainWidgetAsaProgQc()
        WidgetAsaProgQc.setupUi(self.tabAsaProgQc)
        self.AsaprogQc = AsaprogQc(WidgetAsaProgQc,self)

    def AddAsaProgQcTab(self):
        self.tabAsaProgQc = QWidget()
        self.tabAsaProgQc.setObjectName("tabAsaProgQc")
        self.tabWidget_main.addTab(self.tabAsaProgQc, "")
        self.verticalLayout.addWidget(self.tabWidget_main)

        _translate = QCoreApplication.translate
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabAsaProgQc), _translate("MainWindow", "連續燒錄M128"))

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
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
