import sys
import serial
from decodeASAformat import *
from pyqtwindow import Ui_MainWindow
from listport import serial_ports
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

class SerialThread(QThread):
    signalGetLine = pyqtSignal(str)
    signalGetArrayData = pyqtSignal(int,int,tuple)
    signalGetStructData = pyqtSignal(list)

    #初始化
    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser
        self.line = str()
        self.header = bytearray(b'\00\00\00')

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
            elif ch == b'\x00':
                pass
            elif ch > b'\x7E':
                self.header[0] = self.header[1]
                self.header[1] = self.header[2]
                self.header[2] = int.from_bytes(ch, byteorder='big')
                if self.header == b'\xaa\xaa\xaa':
                    arrTypeNum = int.from_bytes(self.ser.read(1), byteorder='big')
                    arrBytes = int.from_bytes(self.ser.read(1), byteorder='big')
                    chkSum = arrBytes;
                    data = bytearray()
                    for index in range(0,arrBytes):
                        data.append(int.from_bytes(self.ser.read(1), byteorder='little'))
                        chkSum += data[index];
                    getChkSum = int.from_bytes(self.ser.read(1), byteorder='big')
                    if (getChkSum != chkSum%256):
                        print('Error')
                    else:
                        arr = decode_array(arrTypeNum,data)
                        print('sys : Get ArrayData from devive: ' + str(arr))
                        self.signalGetArrayData.emit(arrTypeNum,arrBytes,arr)
                        self.header = bytearray(b'\00\00\00')

                if self.header == b'\xbb\xbb\xbb':
                    print('struct')
            else :
                pass

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
        self.lineEditTerminalSend.returnPressed.connect(self.serialSendLine)
        self.buttonTerminalSend.clicked.connect(self.serialSendLine)
        self.buttonTerminalSave.clicked.connect(self.terminalSave)
        self.buttonTerminalClear.clicked.connect(self.terminalClear)
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
        if  self.portComboBox.currentText() == '' and self.isPortOpen == 0:
            pass
        elif (self.isPortOpen == 0):
            self.ser.port = self.portComboBox.currentText()
            self.ser.open()
            self.isPortOpen = 1
            # SerialThread訊號槽
            self.SerialThread = SerialThread(self.ser)
            self.SerialThread.signalGetLine.connect(self.terminalAppendGetLine)
            self.SerialThread.signalGetArrayData.connect(self.textGetAppendArray)
            self.SerialThread.start()
            self.buttonPortToggle.setText("關閉串列埠")
            self.textTerminal.append('( log: Open '+self.ser.port +' succeed! )')
        elif (self.isPortOpen == 1):
            self.SerialThread.terminate()
            self.ser.close()
            self.isPortOpen = 0
            self.buttonPortToggle.setText("開啟串列埠")
            self.textTerminal.append('( log: Close '+self.ser.port +' succeed! )')

    # append the line from serial in terminal
    @pyqtSlot(str)
    def terminalAppendGetLine(self, line):
        self.textTerminal.append('>>  '+line)

    # 文字對話區功能
    # Send line to serial
    @pyqtSlot()
    def serialSendLine(self):
        if self.isPortOpen != True:
            return False
        line = self.lineEditTerminalSend.text()
        self.lineEditTerminalSend.clear()
        print('sys : SendLine to devive: '+line)
        if (self.isPortOpen == 1):
            self.ser.write(bytes(line+'\n', encoding = "utf-8") )
            self.textTerminal.append('<<  '+line)
    def terminalSave(self):
        text = self.textTerminal.toPlainText()
        self.file_save(text)
    def terminalClear(self):
        text = self.textTerminal.clear()

    # 發送區功能 implement
    def verifyOK(self):
        self.textBrowserSendVerify.clear()
        self.textBrowserSendVerify.append('OK')
    def verifyFAIL(self):
        self.textBrowserSendVerify.clear()
        self.textBrowserSendVerify.append('FAIL')
    def btnSendClear(self):
        text = self.textEditSend.clear()
        pass
    def btnSendStruct(self):
        res = -1;
        try:
            lineIdx, typeNumList, dataListList, res =decodeTextToStruct(self.textEditSend.toPlainText())
        except (ValueError,SyntaxError,TypeError):
            res = -1
            pass
        if res != 0:
            self.verifyFAIL()
            print('sys : error')
        else:
            self.verifyOK()
            if self.isPortOpen != True:
                return False
            structTypeString = str();
            structTypeStringByte = 0;
            structBytes = 0
            chkSum = 0
            for idx in range(len(typeNumList)):
                structTypeString += getTypeStr(typeNumList[idx]) + 'x' + str(len(dataListList[idx]))
                structBytes      += getTypeSize(typeNumList[idx]) * len(dataListList[idx])
                if idx != len(typeNumList)-1:
                    structTypeString += ','
            structTypeStringByte = len(structTypeString)
            structBytes += structTypeStringByte
            if structBytes >= 255:
                print ('sys : error bytes >= 255')
                return False
            self.ser.write(b'\xaa\xaa\xaa')
            self.ser.write(pack('>B',structBytes))
            self.ser.write(pack('>B',structTypeStringByte))
            self.ser.write(bytes(structTypeString, encoding = "ascii"))
            chkSum += sum(bytes(structTypeString, encoding = "ascii"));
            print(bytes(structTypeString, encoding = "ascii"))
            for idx, dataList in enumerate(dataListList):
                for data in dataList:
                    self.ser.write(pack('<'+decodePackStr(typeNum),data))
                    chkSum += sum(pack('<'+decodePackStr(typeNumList[idx]),data));
                    print(pack('<'+decodePackStr(typeNumList[idx]),data))
            self.ser.write(pack('>B',chkSum%256))
            print('chksum ' + str(chkSum%256))


            # for value in variable:
            #     pass
            # print()

    def btnSendArray(self):
        # print(self.textEditSend.toPlainText())
        res = -1;
        try:
            typeNum, dataList, res, resText = decodeTextToArrey(self.textEditSend.toPlainText())
        except (ValueError,SyntaxError,TypeError):
            res = -1
            pass
        if res != 0:
            self.verifyFAIL()
            print('sys : error')
        else:
            self.textEditSend.clear();
            self.textEditSend.append(resText)
            self.verifyOK()
            if self.isPortOpen != True:
                return False
            self.ser.write(b'\xab\xab\xab')
            self.ser.write(pack('>B',typeNum))
            print(pack('>B',typeNum))
            dataBytes =len(dataList)*getTypeSize(typeNum)
            self.ser.write(pack('>B',dataBytes))
            print(pack('>B',len(dataList)))
            chkSum = 0
            for data in dataList:
                self.ser.write(pack('<'+decodePackStr(typeNum),data))
                chkSum += sum(pack('<'+decodePackStr(typeNum),data));
                print(pack('<'+decodePackStr(typeNum),data))
                print(chkSum)
            self.ser.write(pack('>B',chkSum%256))
            self.textTerminal.append('( log: send ' + str(dataBytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')
    def btnSendSaveFile(self):
        text = self.textEditSend.toPlainText()
        self.file_save(text)
    def btnSendReadFile(self):
        file = self.file_open()
        self.textEditSend.append(file.read())
        file.close()
    # 接收區功能 implement
    def btnGetClear(self):
        self.textEditGet.clear()
    def btnGetSaveFile(self):
        text = self.textEditGet.toPlainText()
        self.file_save(text)
    def btnGetMovetoSend(self):
        text = self.textEditGet.toPlainText()
        self.textEditGet.clear()
        self.textEditSend.append(text)

    # SerialThread訊號槽function
    # 顯示array data
    def textGetAppendArray(self,typeNum,bytes,array):
        print('sys : textGet append array data:' + str(array))
        self.textEditGet.append(getTypeStr(typeNum)+' : ')
        s = '  '
        for idx, data in enumerate(array):
            s += str(data)
            if idx+1 != len(array):
                s += ',  '
            else:
                self.textEditGet.append(s)
            if len(s) > 100: #換行
                self.textEditGet.append(s)
                s = '  '
        self.textEditGet.append('')
        self.textTerminal.append('( log: get  ' + str(bytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')

    # 顯示Struct data
    def textGetAppendStruct(self,typeNum,struct):
        self.textEditGet.append(getTypeStr(typeNum)+' : ')
        s = '  '
        for idx, data in enumerate(array):
            s += str(data)
            print(s)
            print(str(data))
            if idx+1 != len(array):
                s += ',  '
            else:
                self.textEditGet.append(s)
            if len(s) > 100: #換行
                self.textEditGet.append(s)
                s = '  '
        self.textEditGet.append('')

    # 檔案讀寫 function
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
