import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_hmi import Ui_MainWidgetHMI
from ui.ui_avrdude import Ui_MainWidgetAvrdude
from ui.ui_asa_prog import Ui_MainWidgetAsaProg

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

        widgetAsaProg.progressBar.setRange(0,10000);
        widgetAsaProg.progressBar.setValue(0);

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
