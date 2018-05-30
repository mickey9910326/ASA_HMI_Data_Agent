import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QCoreApplication

from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_hmi import Ui_MainWidgetHMI
from ui.ui_avrdude import Ui_MainWidgetAvrdude
from ui.ui_asa_prog import Ui_MainWidgetAsaProg
from ui.ui_asa_prog_qc import Ui_MainWidgetAsaProgQc

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        widgetHmi = Ui_MainWidgetHMI()
        widgetAvrdude = Ui_MainWidgetAvrdude()
        widgetAsaProg = Ui_MainWidgetAsaProg()
        widgetHmi.setupUi(self.tabHmi)
        widgetAvrdude.setupUi(self.tabAvrdude)
        widgetAsaProg.setupUi(self.tabAsaProg)

        widgetAsaProg.progressBar.setRange(0,10000)
        widgetAsaProg.progressBar.setValue(0)

        self.AddAsaProgQcTab()
        WidgetAsaProgQc = Ui_MainWidgetAsaProgQc()
        WidgetAsaProgQc.setupUi(self.tabAsaProgQc)
        
    def AddAsaProgQcTab(self):
        self.tabAsaProgQc = QWidget()
        self.tabAsaProgQc.setObjectName("tabAsaProgQc")
        self.tabWidget_main.addTab(self.tabAsaProgQc, "")
        self.verticalLayout.addWidget(self.tabWidget_main)

        _translate = QCoreApplication.translate
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tabAsaProgQc), _translate("MainWindow", "連續燒錄M128"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
