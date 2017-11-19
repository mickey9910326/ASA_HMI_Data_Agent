import sys
import serial
from pyqtwindow import Ui_MainWindow
from listport import serial_ports
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

class SerialThread(QThread):
    signalGetLine = pyqtSignal(str)
    signalGetData = pyqtSignal(list)

    #初始化
    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser
        self.line = str()

    #執行序（可以很多個）
    def run(self):
        while (self.ser.isOpen()):
            ch = self.ser.read(1)
            if ch == b'\n':
                self.signalGetLine.emit(self.line)
                self.line = str()
            # 可顯示字元
            elif ch >= b'\x20' and ch <= b'\x7E':
                self.line += ch.decode("ascii");
        #完成，發出信號（帶一個 list 參數）
        # self.signalGetLine.emit(nPath)

    #中止序
    # def stop(self):
    #     with QMutexLocker(self.mutex): self.stoped = True

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # init ui
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # varables
        self.isPortOpen = 0;
        self.ser = serial.Serial();
        self.ser.baudrate = 38400;
        self.ser.timeout = 10;
        # 串列埠設定區功能
        self.updateSerialPortlist()
        self.buttonPortToggle.clicked.connect(self.portToggle)
        # 文字對話區功能
        self.buttonTerminalSend.clicked.connect(self.serialSendLine)
        self.lineEditTerminalSend.returnPressed.connect(self.serialSendLine)
        # 發送區功能
        self.buttonSendClear.clicked.connect(self.btnSendClear)
        self.buttonSendStruct.clicked.connect(self.btnSendStruct)
        self.buttonSendArray.clicked.connect(self.btnSendArray)
        self.buttonSendReadFile.clicked.connect(self.btnSendReadFile)
        self.buttonSendSaveFile.clicked.connect(self.btnSendSaveFile)
        # 接收區功能
        self.buttonGetClear.clicked.connect(self.btnGetClear)
        self.buttonGetSaveFile.clicked.connect(self.btnGetSaveFile)
        self.buttomGetMovetoSend.clicked.connect(self.btnGetMovetoSend)

    def updateSerialPortlist(self):
        availablePorts = serial_ports()
        for port in availablePorts:
            self.portComboBox.addItem(port)

    # open/close serial port
    @pyqtSlot()
    def portToggle(self):
        # TODO 失敗例外
        if (self.isPortOpen == 0):
            self.ser.port = self.portComboBox.currentText()
            self.ser.open()
            self.isPortOpen = 1
            self.SerialThread = SerialThread(self.ser)
            self.SerialThread.signalGetLine.connect(self.terminalAppendGetLine)
            self.SerialThread.start()
            self.buttonPortToggle.setText("關閉串列埠")
            self.textTerminal.append(self.ser.port +' open')
        elif (self.isPortOpen == 1):
            self.SerialThread.terminate()
            self.ser.close()
            self.isPortOpen = 0
            self.buttonPortToggle.setText("開啟串列埠")
            self.textTerminal.append(self.ser.port+' close')

    # append the line from serial in terminal
    @pyqtSlot(str)
    def terminalAppendGetLine(self, line):
        self.textTerminal.append('>>  '+line)

    # Send line to serial
    @pyqtSlot()
    def serialSendLine(self):
        line = self.lineEditTerminalSend.text()
        self.lineEditTerminalSend.clear()
        print(line)
        if (self.isPortOpen == 1):
            self.ser.write(bytes(line+'\n', encoding = "utf-8") )
            self.textTerminal.append('<<  '+line)

    # 發送區功能 implement
    def btnSendClear(self):
        text = self.textEditSend.clear()
    def btnSendStruct(self):
        pass
    def btnSendArray(self):
        pass
    def btnSendSaveFile(self):
        text = self.textEditSend.toPlainText()
        self.file_save(text)
    def btnSendReadFile(self):
        file = self.file_open()
        self.textEditSend.append(file.read())
        file.close()
    # 接收區功能 implement
    def btnGetClear(self):
        text = self.textEditGet.clear()
    def btnGetSaveFile(self):
        text = self.textEditGet.toPlainText()
        self.file_save(text)
    def btnGetMovetoSend(self):
        file = self.file_open()
        self.textEditSend.append(file.read())
        file.close()


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
