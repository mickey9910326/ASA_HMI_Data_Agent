from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from asa_hmi_data_agent.listport import getAvailableSerialPorts
from time import sleep

import asaprog
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
        self.max = 0

    def run(self):
        loader = asaprog.Loader(self.port, self.hexfile)
        self.loader = loader
        self.signalInitProgressbar.emit(0, loader.total_steps-1)

        for i in range(loader.total_steps):
            try:
                loader.step()
            except asaprog.ChkDeviceException as e:
                self.signalCheckIsAsaDevice.emit(False)
                progdbg('Error: The device is not asa-board.')
                break
            except asaprog.CantOpenComportException as e:
                self.signalGetSerialException.emit()
                progdbg('Error: Cannot open the comport \'{}\'.'.format(loader.port))
                break
            except asaprog.EndingException as e:
                self.signalLastData.emit(False)
                progdbg('Error: The device ignored the ending command .')
                break
            except serial.serialutil.SerialException as e:
                self.signalGetSerialException.emit()
                break

            if i == 0:
                self.signalSetProgressbar.emit(i)
                self.signalCheckIsAsaDevice.emit(True)
            elif i == loader.total_steps-1:
                self.signalSetProgressbar.emit(i)
                self.signalLastData.emit(True)
            else:
                self.signalSetProgressbar.emit(i)

    def stop(self):
        self.terminate()

# ---- class ShellThread End ---------------------------------------------------

class AsaLoader(object):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget, mainWindow):
        self.widget = widget
        self.mainWindow = mainWindow
        self.widget.progressBar.setValue(0)

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
        # self.widget.lineEdit_selectFile.textChanged.connect()
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
        availablePorts = getAvailableSerialPorts()
        progdbg('Update ports: ' + str(availablePorts))
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
            self.checkIsHexFile(name)

    def checkIsHexFile(self, filename):
        try:
            hexbin = asaprog.parseIHex(filename)
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
        elif self.checkIsHexFile(hexfile) is False:
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
        if self.shellThread.isRunning():
            return
        port = self.widget.comboBox_selectPort.currentText()
        if port == '':
            self.widget.label_statusContent.setText(u"未選擇串列埠")
            return
        hexfile = 'tools\\m128_stk500.hex'
        self.checkIsHexFile(hexfile)

        self.mainWindow.serToggle.emit(True, port)
        self.widget.label_statusContent.setText(u"確認裝置中...")
        self.shellThread.setParameter(port, hexfile)
        self.shellThread.start()
    # ---- Special Functions Group end -----------------------------------------

# hmi debug log
def progdbg(s):
    s = 'prog log: ' + s
    print(s)
