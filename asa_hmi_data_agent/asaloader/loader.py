from asa_hmi_data_agent.listport import getAvailableSerialPorts
from asa_hmi_data_agent.ui.ui_widget_asa_loader import Ui_WidgetAsaLoader
from asa_hmi_data_agent.util import ADTPATH

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog

from time import sleep
import datetime
import asaprog
import serial
import math
import os

# ---- class LoaderThread Start -------------------------------------------------
class LoaderThread(QThread):
    sigState = pyqtSignal(bool, int, str)
    sigChkAsaDevice = pyqtSignal(bool)
    sigStart = pyqtSignal(int)
    sigStepDone = pyqtSignal(int)
    sigEnd = pyqtSignal(bool)
    sigGetSerialException = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.cmd = str()

    def setParameter(self, port, hexfile):
        self.port = port
        self.hexfile = hexfile
        self.max = 0

    def run(self):
        loader = asaprog.Loader(self.port, self.hexfile)
        self.loader = loader
        self.sigStart.emit(loader.total_steps-1)

        for i in range(loader.total_steps):
            try:
                loader.step()
            except asaprog.ChkDeviceException as e:
                self.sigChkAsaDevice.emit(False)
                debugLog('Error: The device is not asa-board.')
                break
            except asaprog.CantOpenComportException as e:
                self.sigGetSerialException.emit()
                debugLog('Error: Cannot open the comport \'{}\'.'.format(loader.port))
                break
            except asaprog.EndingException as e:
                self.sigEnd.emit(False)
                debugLog('Error: The device ignored the ending command .')
                break
            except serial.serialutil.SerialException as e:
                self.sigGetSerialException.emit()
                break

            if i == 0:
                self.sigStepDone.emit(i)
                self.sigChkAsaDevice.emit(True)
            elif i == loader.total_steps-1:
                self.sigStepDone.emit(i)
                self.sigEnd.emit(True)
            else:
                self.sigStepDone.emit(i)

    def stop(self):
        self.terminate()

# ---- class LoaderThread End ---------------------------------------------------
class AsaLoader(QObject):
    sigChangeWindowTitle = pyqtSignal(bool, str)
    sigSerialPortCheck = pyqtSignal(bool, str)

    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget):
        super(AsaLoader, self).__init__()
        self.ui = Ui_WidgetAsaLoader()
        self.ui.setupUi(widget)
        self.ui.progressBar.setValue(0)

        # ---- Thread Init start -----------------------------------------------
        self.loaderThread = LoaderThread()
        self.loaderThread.sigChkAsaDevice[bool].connect(self.updateStatus_isAsaDevice)
        self.loaderThread.sigStart[int].connect(self.initProgressbar)
        self.loaderThread.sigStepDone[int].connect(self.setProgressbar)
        self.loaderThread.sigEnd[bool].connect(self.updateStatus_end)
        self.loaderThread.sigGetSerialException.connect(self.updateStatus_serialException)
        self.loaderThread.finished.connect(
            lambda: self.sigSerialPortCheck.emit(
                False, self.ui.comboBox_selectPort.currentText()
            )
        )
        # ---- Thread Init end -------------------------------------------------

        # ---- Serial Group start ----------------------------------------------
        self.serial_updatePortlist()
        self.ui.pushButton_updatePortList.clicked.connect(self.serial_updatePortlist)
        # ---- Serial Group end ------------------------------------------------

        # ---- Basic Functions Group start -------------------------------------
        self.ui.pushButton_selectFile.clicked.connect(self.chooseProgFile)
        self.ui.pushButton_startProg.clicked.connect(self.startLoad)
        self.ui.pushButton_stopProg.clicked.connect(self.stopLoading)
        # ---- Basic Functions Group end ---------------------------------------

        # ---- Special Functions Group start -----------------------------------
        self.ui.pushButton_progStk500.clicked.connect(self.startLoadStk500)
        # ---- Special Functions Group end -------------------------------------

    # ---- LoaderThread Related functions start --------------------------------
    def initProgressbar(self, max):
        self.ui.progressBar.setRange(0, max)

    def setProgressbar(self, val):
        self.ui.progressBar.setValue(val)

    def updateStatus_isAsaDevice(self, isAsaDevice):
        if isAsaDevice:
            self.ui.label_statusContent.setText(u"確認裝置為ASA_M128，開始燒錄")
        else:
            self.ui.label_statusContent.setText(u"請確認連接裝置為ASA_M128，並按下reset按鈕")

    def updateStatus_end(self ,isOK):
        if isOK:
            self.ui.label_statusContent.setText(u"燒錄成功！")
        else:
            self.ui.label_statusContent.setText(u"燒錄失敗！")

    def updateStatus_serialException(self):
        self.ui.label_statusContent.setText(u"與串列埠失去連線，請檢察USB線是否有連接好")
    # ---- LoaderThread Related functions end ----------------------------------

    # ---- Serial Related functions start --------------------------------------
    def serial_updatePortlist(self):
        """Update port list in comboBox_selectPort."""
        availablePorts = getAvailableSerialPorts()
        debugLog('Update ports: ' + str(availablePorts))
        self.ui.comboBox_selectPort.clear()
        for port in availablePorts:
            self.ui.comboBox_selectPort.addItem(port)
    # ---- Serial Related functions end ----------------------------------------

    # ---- Basic Functions Group start -----------------------------------------
    def chooseProgFile(self):
        name, _ = QFileDialog.getOpenFileName(
            filter='All Files (*);;Hex Files (*.hex)',
            initialFilter='Hex Files (*.hex)'
        )
        if name is not '':
            self.ui.lineEdit_selectFile.setText(name)
            self.checkIsHexFile(name)

    def checkIsHexFile(self, filename):
        try:
            hexbin = asaprog.parseIHex(filename)
        except (NameError,UnicodeDecodeError):
            self.ui.label_programSizeContent.setText(u"非HEX檔案格式，請重新選擇檔案")
            self.ui.label_etcContent.setText('-')
            return False
        else:
            size = len(hexbin)/1024
            self.ui.label_programSizeContent.setText('{:0.2f} KB'.format(size))
            etc = math.ceil(len(hexbin)/256)*0.03
            self.ui.label_etcContent.setText('{:0.2f} s'.format(etc))
            return True

    def startLoad(self):
        if self.loaderThread.isRunning():
            return
        port = self.ui.comboBox_selectPort.currentText()
        if port == '':
            self.ui.label_statusContent.setText(u"未選擇串列埠")
            return
        hexfile = self.ui.lineEdit_selectFile.text()
        if hexfile == '':
            self.ui.label_statusContent.setText(u"未選擇燒錄檔案")
            return
        elif self.checkIsHexFile(hexfile) is False:
            self.ui.label_statusContent.setText(u"請重新選擇燒錄檔案")
            return

        self.sigSerialPortCheck.emit(True, port)
        self.ui.label_statusContent.setText(u"確認裝置中...")
        self.loaderThread.setParameter(port, hexfile)
        self.loaderThread.start()

    def stopLoading(self):
        if self.loaderThread.isRunning():
            self.loaderThread.stop()
            self.sigSerialPortCheck.emit(False, self.ui.comboBox_selectPort.currentText())
            self.ui.label_statusContent.setText(u"已強制終止")
    # ---- Basic Functions Group end -------------------------------------------

    # ---- Special Functions Group start ---------------------------------------
    def startLoadStk500(self):
        if self.loaderThread.isRunning():
            return
        port = self.ui.comboBox_selectPort.currentText()
        if port == '':
            self.ui.label_statusContent.setText(u"未選擇串列埠")
            return
        hexfile = os.path.join(ADTPATH, 'tools\m128_stk500.hex')
        self.checkIsHexFile(hexfile)

        self.sigSerialPortCheck.emit(True, port)
        self.ui.label_statusContent.setText(u"確認裝置中...")
        self.loaderThread.setParameter(port, hexfile)
        self.loaderThread.start()
    # ---- Special Functions Group end -----------------------------------------

def debugLog(msg):
    s = '[{}] loader   log: {}'.format(
        datetime.datetime.now().strftime("%H:%M:%S"),
        msg
    )
    print(s)
