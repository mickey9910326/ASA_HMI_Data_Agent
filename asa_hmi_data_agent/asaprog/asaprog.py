from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from asa_hmi_data_agent.listport import serial_ports
from time import sleep
import py_asa_loader
import serial
import math

# ---- class ShellThread Start -------------------------------------------------
class ShellThread(QThread):
    signalCheckIsAsaDevice = pyqtSignal(bool)
    signalLastData = pyqtSignal(bool)
    signalInitProgressbar = pyqtSignal(int,int)
    signalSetProgressbar = pyqtSignal(int)
    signalGetSerialException = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.cmd = str()

    def setParameter(self, port, hexfile):
        self.port = port
        self.hexfile = hexfile

    def run(self):
        try:
            loader = py_asa_loader.Loader(self.port, self.hexfile)

            isAsaDevice = loader.checkIsAsaDevice()
            self.signalCheckIsAsaDevice.emit(isAsaDevice)

            if isAsaDevice is False:
                return

            times = math.floor(len(loader.bin)/256)
            remain = len(loader.bin)%256

            if remain is not 0:
                self.signalInitProgressbar.emit(0,times+1)
            else:
                self.signalInitProgressbar.emit(0,times)

            delay = 0.03
            for i in range(times):
                loader.loadData(loader.bin[i*256:(i+1)*256])
                self.signalSetProgressbar.emit(i)
                sleep(delay)

            if remain is not 0:
                i = i+1
                loader.loadData(loader.bin[i*256:-1])
                self.signalSetProgressbar.emit(i)
                sleep(delay)

            isOK = loader.lastData()
            if isOK:
                i = i+1
                self.signalSetProgressbar.emit(i)
            self.signalLastData.emit(isOK)
        except serial.serialutil.SerialException as e:
            self.signalGetSerialException.emit()

    def stop(self):
        self.terminate()

# ---- class ShellThread End ---------------------------------------------------

class Asaprog(object):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget, mainWindow):
        self.widget = widget
        self.mainWindow = mainWindow
        self.widget.progressBar.setValue(0);

        # ---- Thread Init start -----------------------------------------------
        self.shellThread = ShellThread()
        self.shellThread.signalInitProgressbar[int,int].connect(self.initProgressbar)
        self.shellThread.signalSetProgressbar[int].connect(self.setProgressbar)
        self.shellThread.signalCheckIsAsaDevice[bool].connect(self.updateStatusIsAsaDevice)
        self.shellThread.signalLastData[bool].connect(self.updateStatusLastData)
        self.shellThread.signalGetSerialException.connect(self.getSerialException)
        self.shellThread.finished.connect(
            lambda : self.mainWindow.serToggle.emit(False, self.widget.comboBox_selectPort.currentText())
        )
        # ---- Thread Init end -------------------------------------------------

        # ---- Serial Group start ----------------------------------------------
        self.serial_updatePortlist()
        self.widget.pushButton_updatePortList.clicked.connect(self.serial_updatePortlist)
        # ---- Serial Group end ------------------------------------------------

        # ---- Basic Functions Group start -------------------------------------
        self.widget.pushButton_selectFile.clicked.connect(self.chooseProgFile)
        self.widget.lineEdit_selectFile.textChanged.connect(self.checkIsHexFile)
        self.widget.pushButton_startProg.clicked.connect(self.startProg)
        self.widget.pushButton_stopProg.clicked.connect(self.stopProg)
        # ---- Basic Functions Group end ---------------------------------------

        # ---- Special Functions Group start -----------------------------------
        # TODO: complete pushButton_progStk500 btn function
        self.widget.pushButton_progStk500.clicked.connect(self.startProgStk500)
        # ---- Special Functions Group end -------------------------------------

    # ---- Serial Group start --------------------------------------------------
    # Update port list in s_portComboBox
    def serial_updatePortlist(self):
        availablePorts = serial_ports()
        print('sys : Update port list in portComboBox, available port : ', end='')
        print(availablePorts)
        self.widget.comboBox_selectPort.clear()
        for port in availablePorts:
            self.widget.comboBox_selectPort.addItem(port)
    # ---- Serial Group end ----------------------------------------------------

    # ---- Basic Functions Group start -----------------------------------------
    def chooseProgFile(self):
        name, _ = QFileDialog.getOpenFileName(self.mainWindow,
                                              'Open File',
                                              '',
                                              'All Files (*);;Hex Files (*.hex)',
                                              initialFilter='Hex Files (*.hex)')
        if name is not '':
            self.widget.lineEdit_selectFile.setText(name)
            self.checkIsHexFile()

    def checkIsHexFile(self):
        file = self.widget.lineEdit_selectFile.text()
        try:
            hexbin = py_asa_loader.parseHex(file)
        except (NameError,UnicodeDecodeError):
            self.widget.label_programSizeContent.setText(u"非HEX檔案格式，請重新選擇檔案")
            self.widget.label_etcContent.setText('-')
            return False
        else:
            size = len(hexbin)/1024
            self.widget.label_programSizeContent.setText('{:0.2f} KB'.format(size))
            etc = math.ceil(len(hexbin)/256)*0.03
            self.widget.label_etcContent.setText('{:0.2f} s'.format(etc))
            return True

    def startProg(self):
        if self.shellThread.isRunning():
            return
        port = self.widget.comboBox_selectPort.currentText()
        if port == '':
            self.widget.label_statusContent.setText(u"未選擇串列埠")
            return
        hexfile = self.widget.lineEdit_selectFile.text()
        if hexfile == '':
            self.widget.label_statusContent.setText(u"未選擇燒錄檔案")
            return
        elif self.checkIsHexFile() is False:
            self.widget.label_statusContent.setText(u"請重新選擇燒錄檔案")
            return

        self.mainWindow.serToggle.emit(True, port)
        self.widget.label_statusContent.setText(u"確認裝置中...")
        self.shellThread.setParameter(port, hexfile)
        self.shellThread.start()

    def stopProg(self):
        if self.shellThread.isRunning():
            self.shellThread.stop()
            self.mainWindow.serToggle.emit(False, self.widget.comboBox_selectPort.currentText())
            self.widget.label_statusContent.setText(u"已強制終止")
    # ---- Basic Functions Group end -------------------------------------------

    # ---- th Group start ------------------------------------------------------
    def initProgressbar(self, min, max):
        self.widget.progressBar.setRange(min, max)

    def setProgressbar(self, val):
        self.widget.progressBar.setValue(val)

    def updateStatusIsAsaDevice(self, isAsaDevice):
        if isAsaDevice:
            self.widget.label_statusContent.setText(u"確認裝置為ASA_M128，開始燒錄")
        else:
            self.widget.label_statusContent.setText(u"請確認連接裝置為ASA_M128，並按下reset按鈕")

    def updateStatusLastData(self ,isOK):
        if isOK:
            self.widget.label_statusContent.setText(u"燒錄成功！")
        else:
            self.widget.label_statusContent.setText(u"燒錄失敗！")

    def getSerialException(self):
        self.widget.label_statusContent.setText(u"與串列埠失去連線，請檢察USB線是否有連接好")

    # ---- th Group end --------------------------------------------------------

    # ---- Special Functions Group start ---------------------------------------
    def startProgStk500(self):
        # TODO: ADD STK500 hex file
        pass
        # if self.shellThread.isRunning():
        #     return
        # port = self.widget.comboBox_selectPort.currentText()
        # if port == '':
        #     self.widget.label_statusContent.setText(u"未選擇串列埠")
        #     return
        # hexfile = ''
        #
        # self.widget.label_statusContent.setText(u"確認裝置中...")
        # self.shellThread.setParameter(port, hexfile)
        # self.shellThread.start()
    # ---- Special Functions Group end -----------------------------------------
