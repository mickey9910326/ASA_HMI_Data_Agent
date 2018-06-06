from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from listport import serial_ports
from time import sleep
import py_asa_loader
import math
import serial

stepText = """
1. PC -> QC_M128 : 'S'
2. QC_M128 -> PC : 'O'
3. PC -> QC_M128 : '1'
4. QC_M128 切通道
5. QC_M128 -> PC : '1'
6. PC開始燒錄，並完成
7. 回到步驟 3. 數字增加
"""

# ---- class ShellThread Start -------------------------------------------------
class ShellThread(QThread):
    signalCheckIsAsaDevice = pyqtSignal(bool)
    signalLastData = pyqtSignal(bool)
    signalInitProgressbar = pyqtSignal(int,int)
    signalSetProgressbar = pyqtSignal(int)
    signalGetSerialException = pyqtSignal()
    signalUpdateStatus = pyqtSignal(str)
    signalComplete = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cmd = str()

    def setParameter(self, ser, hexfile, num):
        self.serialQcM128 = ser
        self.hexfile = hexfile
        self.num = num

    def checkSerIsQcM128(self):
        self.serialQcM128.write(b'S')
        ch = self.serialQcM128.read(1)
        if ch == b's':
            self.signalUpdateStatus.emit('success')
        else:
            self.signalUpdateStatus.emit('連接之裝置非QC程序控制治具')
            return False
        return True

    def run(self):
        if self.checkSerIsQcM128() is False:
            return

        try:
            for channel in range(self.num):
                # send channel cmd
                self.serialQcM128.write(bytes([channel]))
                ch = self.serialQcM128.read(1)
                if ch == b'a':
                    self.signalUpdateStatus.emit('切換通道'+str(channel)+'成功，開始燒錄')
                else:
                    self.signalUpdateStatus.emit('切換通道失敗，請確認周邊硬體裝置')
                    return

                # search asa device
                availablePorts = serial_ports()
                loader = None
                for port in availablePorts:
                    loader = py_asa_loader.Loader(port, self.hexfile)
                    if loader.checkIsAsaDevice() is False:
                        loader = None
                    else:
                        break
                if loader is None:
                    self.signalUpdateStatus.emit('找不到待燒錄裝置')
                    return

                # start prog
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
                    self.signalComplete.emit(channel+1)
                    self.signalUpdateStatus.emit('連接裝置'+str(channel)+'成功')
                else:
                    self.signalUpdateStatus.emit('燒錄裝置'+str(channel)+'失敗')
                    return
            # end for
        except serial.serialutil.SerialException as e:
            self.signalGetSerialException.emit()

        # send stop cmd
        self.serialQcM128.write(b'T')
        ch = self.serialQcM128.read(1)
        if ch == b'a':
            self.signalUpdateStatus.emit('完成所有燒錄，且QC_M128結束燒錄程式成功')
        else:
            self.signalUpdateStatus.emit('完成所有燒錄，但QC_M128結束燒錄程式失敗')
            return

    def stop(self):
        self.terminate()

# ---- class ShellThread End ---------------------------------------------------

class AsaprogQc(object):
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
        self.shellThread.signalUpdateStatus[str].connect(self.updateStatusText)
        self.shellThread.signalComplete[int].connect(self.setCompleteNum)
        self.shellThread.finished.connect(self.closeQcPort)
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

        # ---- Serial object Init Start ----------------------------------------
        self.serialQcM128 = serial.Serial()
        self.serialQcM128.isOpen = False
        self.serialQcM128.baudrate = 38400
        self.serialQcM128.timeout = 1
        # ---- Serial object Init End ------------------------------------------

        self.widget.label_steps.setText(stepText)

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
        # check thread is running
        if self.shellThread.isRunning():
            return
        # check port
        port = self.widget.comboBox_selectPort.currentText()
        if port == '':
            self.updateStatusText(u'未選擇串列埠')
            return
        # check hex file
        hexfile = self.widget.lineEdit_selectFile.text()
        if hexfile == '':
            self.widget.label_statusContent.setText(u'未選擇燒錄檔案')
            return
        elif self.checkIsHexFile() is False:
            self.widget.label_statusContent.setText(u'請重新選擇燒錄檔案')
            return
        # check num of DUT.
        try:
            num = int(self.widget.lineEdit_num.text())
        except ValueError as e:
            self.updateStatusText(u'輸入數量錯誤，範圍為1~12')
            return
        if num < 1 or num > 12:
            self.updateStatusText(u'輸入數量錯誤，範圍為1~12')
            return

        self.openQcPort()
        self.shellThread.setParameter(self.serialQcM128, hexfile, num)
        self.shellThread.start()

    def stopProg(self):
        if self.shellThread.isRunning():
            self.closeQcPort()
            self.shellThread.stop()
            self.widget.label_statusContent.setText(u'已強制終止')

    def updateStatusText(self, s):
        self.widget.label_statusContent.setText(s)

    def setCompleteNum(self, num):
        self.widget.label_progedNumContent.setText(str(num))
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

    def openQcPort(self):
        self.serialQcM128.port = self.widget.comboBox_selectPort.currentText()
        self.serialQcM128.open()

    def closeQcPort(self):
        self.serialQcM128.close()

    def frezzedBtns(self):
        pass

    def Btns(self):
        pass
