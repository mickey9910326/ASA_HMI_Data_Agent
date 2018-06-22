import sys
import serial
from asa_hmi_data_agent.listport import serial_ports
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from asa_hmi_data_agent.hmi.decodeASAformat import *
from asa_hmi_data_agent.hmi.hmi_save_dialog import HmiSaveDialog
from asa_hmi_data_agent.hmi.hmi_load_dialog import HmiLoadDialog

# ---- class Serial Thread Start -----------------------------------------------
class SerialThread(QThread):
    signalGetLine = pyqtSignal(str)
    signalGetArrayData = pyqtSignal(int,int,tuple)
    signalGetStructData = pyqtSignal(list,list,str)
    signalLoseConnect   = pyqtSignal()

    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser
        self.line = bytes()
        self.header = bytearray(b'\00\00\00')
        self.resumingMode = False
        self.resumingType = None
        self.resumingByte = 0
        self.resumingData = None

    def run(self):
        while (self.ser.isOpen()):
            try:
                ch = self.ser.read(1)
                if ch == b'\n' or ch == b'\r':
                    if len(self.line) > 0:
                        try:
                            self.signalGetLine.emit(self.line.decode('utf8'))
                        except UnicodeDecodeError as e:
                            try:
                                self.signalGetLine.emit(self.line.decode('big5'))
                            except UnicodeDecodeError as e:
                                pass
                        self.line = bytes()
                    # print(self.line)
                    # print(self.line.decode('big5'))
                else:
                    self.line += ch

                self.header[0] = self.header[1]
                self.header[1] = self.header[2]
                self.header[2] = int.from_bytes(ch, byteorder='big')

                if self.header == b'\xaa\xaa\xaa':
                    self.line = self.line[0:-3] # remove header
                    if len(self.line) > 0:
                        self.signalGetLine.emit(self.line.decode('big5'))

                    arrTypeNum = int.from_bytes(self.ser.read(1), byteorder='big')
                    arrBytesH = int.from_bytes(self.ser.read(1), byteorder='big')
                    arrBytesL = int.from_bytes(self.ser.read(1), byteorder='big')
                    arrBytes = arrBytesH<<8 | arrBytesL

                    if self.resumingMode is False:
                        chkSum = arrBytesH + arrBytesL
                        data = bytearray()
                        for index in range(0,arrBytes):
                            data.append(int.from_bytes(self.ser.read(1), byteorder='little'))
                            chkSum += data[index];
                        getChkSum = int.from_bytes(self.ser.read(1), byteorder='big')
                        if (getChkSum != chkSum%256):
                            print('get array chksum Error')
                        else:
                            arr = decode_array(arrTypeNum,data)
                            print('sys : Get ArrayData from devive: ' + str(arr))
                            self.signalGetArrayData.emit(arrTypeNum,arrBytes,arr)
                            self.header = bytearray(b'\00\00\00')
                    else:
                        print('th1 error point 1')
                elif self.header == b'\xbb\xbb\xbb':
                    self.line = self.line[0:-3] # remove header
                    if len(self.line) > 0:
                        self.signalGetLine.emit(self.line.decode('big5'))

                    getBytesH = int.from_bytes(self.ser.read(1), byteorder='big')
                    getBytesL = int.from_bytes(self.ser.read(1), byteorder='big')
                    getBytes = getBytesH<<8 | getBytesL
                    chkSum = getBytesH + getBytesL

                    getFormatBytes = int.from_bytes(self.ser.read(1), byteorder='big')
                    dataBytes = getBytes-getFormatBytes-1
                    chkSum += getFormatBytes

                    formatString = bytearray()
                    data = bytearray()
                    for index in range(0,getFormatBytes):
                        formatString += self.ser.read(1)
                        chkSum += int(formatString[index])
                    formatString = formatString.decode("ascii")
                    print(formatString)
                    for index in range(0,dataBytes):
                        data.append(int.from_bytes(self.ser.read(1), byteorder='little'))
                        chkSum += data[index];
                    getChkSum = int.from_bytes(self.ser.read(1), byteorder='big')
                    if (getChkSum != chkSum%256):
                        print('get struct chksum Error')
                    else:
                        # arr = decode_array(arrTypeNum,data)
                        # print('sys : Get ArrayData from devive: ' + str(arr))
                        self.header = bytearray(b'\00\00\00')
                        typeNumList, dataListList = decode_struct(getBytes,formatString,data)
                        self.signalGetStructData.emit(typeNumList, dataListList,formatString)
            except serial.serialutil.SerialException as e:
                self.signalLoseConnect.emit()
                break

# ---- class Serial Thread End -------------------------------------------------

class HMI(object):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget, mainWindow):
        # super(MainWindow, self).__init__(parent)
        self.widget = widget
        self.mainWindow = mainWindow
        self.hmiSaveDialog = HmiSaveDialog()
        self.hmiLoadDialog = HmiLoadDialog()

        # ---- Serial object Init Start ----------------------------------------
        self.ser = serial.Serial()
        self.ser.baudrate = 38400
        self.ser.timeout = 10
        # ---- Serial object Init End ------------------------------------------

        # ---- Serial Thread Init Start ----------------------------------------
        self.SerialThread = SerialThread(self.ser)
        self.SerialThread.signalGetLine[str].connect(self.text_terminalAppendLineFromDevice)
        self.SerialThread.signalGetArrayData[int,int,tuple].connect(self.rec_AppendArray)
        self.SerialThread.signalGetStructData.connect(self.rec_AppendStruct)
        self.SerialThread.signalLoseConnect.connect(self.loseConnectHandler)
        # ---- Serial Thread Init End ------------------------------------------

        # ---- Function Linking start ------------------------------------------
        # 串列埠設定區
        self.s_updatePortlist()
        self.widget.s_btnPortToggle.clicked.connect(self.s_portToggle)
        self.widget.s_btnUpdatePortList.clicked.connect(self.s_updatePortlist)
        # 文字對話區
        self.widget.text_lineEditToBeSend.returnPressed.connect(self.text_sendLineToDevice)
        self.widget.text_btnSend.clicked.connect(self.text_sendLineToDevice)
        self.widget.text_btnClearTerminal.clicked.connect(self.text_terminalClear)
        self.widget.text_btnSaveTerminal.clicked.connect(self.text_terminalSave)
        # 接收區
        self.widget.rec_btnClear.clicked.connect(self.rec_textEditClear)
        self.widget.rec_btnSave.clicked.connect(lambda : self.hmiSaveDialog.showAndLoadText(self.widget.rec_textEdit.toPlainText()))
        self.widget.rec_btnSave.clicked.connect(self.hmiSaveDialog.show)
        self.widget.rec_btnMoveToSend.clicked.connect(self.rec_textEditMovetoSend)
        self.widget.rec_btnUi8ToString.clicked.connect(self.rec_textEditUi8ToString)
        self.widget.rec_btnStringToUi8.clicked.connect(self.rec_textEditStringToUi8)
        # 發送區
        self.widget.send_btnClear.clicked.connect(self.send_textEditClear)
        self.widget.send_btnSave.clicked.connect(lambda : self.hmiSaveDialog.showAndLoadText(self.widget.send_textEdit.toPlainText()))
        self.widget.send_btnReadFile.clicked.connect(self.hmiLoadDialog.show)
        self.widget.send_btnUi8ToString.clicked.connect(self.send_textEditUi8ToString)
        self.widget.send_btnStringToUi8.clicked.connect(self.send_textEditStringToUi8)
        self.widget.send_btnSendArray.clicked.connect(self.send_btnSendArray)
        self.widget.send_btnSendStruct.clicked.connect(self.send_btnSendStruct)
        # ---- Function Linking end --------------------------------------------

        # ---- HmiSaveDialog section start -------------------------------------
        self.hmiSaveDialog.accepted.connect(lambda : print('HmiSaveDialog close'))
        # ---- HmiSaveDialog section end ---------------------------------------

        # ---- HmiLoadDialog section start -------------------------------------
        self.hmiLoadDialog.accepted.connect(self.updateTextFromLoadDialog)
        # ---- HmiLoadDialog section end ---------------------------------------

    # ---- 串列埠設定區功能實現 start --------------------------------------------
    # Update port list in s_portComboBox
    def s_updatePortlist(self):
        if self.ser.isOpen():
            pass
        else :
            availablePorts = serial_ports()
            print('sys : Update port list in portComboBox, available port : ', end='')
            print(availablePorts)
            self.widget.s_portComboBox.clear()
            for port in availablePorts:
                self.widget.s_portComboBox.addItem(port)

    # Open/Close serial port
    def s_portToggle(self):
        if (self.widget.s_portComboBox.currentText() is '') and (self.ser.isOpen() is False) :
            pass
        elif (self.ser.isOpen() is False):
            self.ser.port = self.widget.s_portComboBox.currentText()
            print('sys : Try to open port : ' + self.ser.port )
            try:
                self.ser.open()
                self.mainWindow.setWindowTitle("ASA_HMI_Data_Agent   "+ self.ser.port +' is opened.')

            except serial.serialutil.SerialException as e:
                print('sys : Open port ' + self.ser.port + ' failed ')
                print('     Exception : ', end='')
                print(e)
                self.widget.text_terminal.append('( log : Open port ' + self.ser.port + ' failed! )')
            else :
                self.widget.s_btnPortToggle.setText("關閉串列埠")
                self.widget.text_terminal.append('( log: Open ' + self.ser.port +' success! )')
                self.SerialThread.start()
        elif (self.ser.isOpen()):
            print('sys : Try to close port : ' + self.ser.port )
            self.SerialThread.terminate()
            self.ser.close()
            self.mainWindow.setWindowTitle("ASA_HMI_Data_Agent   "+ self.ser.port +' is closed.')
            self.widget.s_btnPortToggle.setText("開啟串列埠")
            self.widget.text_terminal.append('( log: Close ' + self.ser.port +' success! )')
    # ---- 串列埠設定區功能實現 end ----------------------------------------------

    # ---- 文字對話區功能實現 start ----------------------------------------------
    # Append the line from serial in terminal
    def text_terminalAppendLineFromDevice(self, line):
        self.widget.text_terminal.append('>>  '+line)
        print('sys : Get line from devive: ' + line)

    # Send line to serial
    def text_sendLineToDevice(self):
        if self.ser.isOpen() is False:
            return False
        else:
            line = self.widget.text_lineEditToBeSend.text()
            self.widget.text_lineEditToBeSend.clear()
            self.ser.write(bytes(line+'\n', encoding = "utf-8") )
            self.widget.text_terminal.append('<<  '+line)
            print('sys : Send line to devive: ' + line)

    # Svae the text in text terminal
    def text_terminalSave(self):
        text = self.widget.text_terminal.toPlainText()
        self.mainWindow.file_save(text)

    # Clear the text in text terminal
    def text_terminalClear(self):
        text = self.widget.text_terminal.clear()

    def text_appendLog(self, s):
        self.widget.text_terminal.append('( ' + s + ' )')
    # ---- 文字對話區功能實現 end ------------------------------------------------

    # ---- 接收區功能實現 start -------------------------------------------------
    def rec_textEditClear(self):
        self.widget.rec_textEdit.clear()
    def rec_textEditSave(self):
        text = self.widget.rec_textEdit.toPlainText()
        self.mainWindow.file_save(text)
    def rec_textEditMovetoSend(self):
        text = self.widget.rec_textEdit.toPlainText()
        self.widget.rec_textEdit.clear()
        self.widget.send_textEdit.append(text)
    def rec_textEditUi8ToString(self):
        res, resText = transUi8ToString(self.widget.rec_textEdit.toPlainText())
        self.widget.rec_textEdit.clear()
        self.widget.rec_textEdit.append(resText)
    def rec_textEditStringToUi8(self):
        res, resText = transStringToUi8(self.widget.rec_textEdit.toPlainText())
        self.widget.rec_textEdit.clear()
        self.widget.rec_textEdit.append(resText)
    def rec_AppendArray(self,typeNum,bytes,array):
        print('sys : textGet append array data:' + str(array))
        self.widget.rec_textEdit.append(getTypeStr(typeNum)+' : ')
        s = '  '
        for idx, data in enumerate(array):
            s += str(data)
            if idx+1 != len(array):
                s += ',  '
            else:
                self.widget.rec_textEdit.append(s)
            if len(s) > 100: #換行
                self.widget.rec_textEdit.append(s)
                s = '  '
        self.widget.rec_textEdit.append('')
        self.widget.text_terminal.append('( log: get  ' + str(bytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')
    def rec_AppendStruct(self, typeNumList, dataListList, formatString):
        for idx in range(len(typeNumList)):
            typeNum = typeNumList[idx]
            dataList = dataListList[idx]
            self.widget.rec_textEdit.append(getTypeStr(typeNum)+' : ')
            s = '  '
            for idx2, data in enumerate(dataList):
                s += str(data)
                if idx2+1 != len(dataList):
                    s += ',  '
                else:
                    self.widget.rec_textEdit.append(s)
                if len(s) > 100: #換行
                    self.widget.rec_textEdit.append(s)
                    s = '  '
            self.widget.rec_textEdit.append('')
        self.widget.text_terminal.append('( log: get struct of ' + formatString +'. )')
    # ---- 接收區功能實現 end ---------------------------------------------------

    # ---- 發送區功能實現 start -------------------------------------------------
    def send_textEditClear(self):
        self.widget.send_textEdit.clear()
    def send_textEditSave(self):
        text = self.widget.send_textEdit.toPlainText()
        self.mainWindow.file_save(text)
    def send_textEditReadFile(self):
        file = self.mainWindow.file_open()
        # handle cancel btn
        try:
            self.widget.send_textEdit.append(file.read())
            file.close()
        except AttributeError as e:
            pass
            # raise
    def send_textEditUi8ToString(self):
        res, resText = transUi8ToString(self.widget.send_textEdit.toPlainText())
        self.widget.send_textEdit.clear()
        self.widget.send_textEdit.append(resText)
    def send_textEditStringToUi8(self):
        res, resText = transStringToUi8(self.widget.send_textEdit.toPlainText())
        self.widget.send_textEdit.clear()
        self.widget.send_textEdit.append(resText)
    def send_verifyShowOK(self):
        self.widget.send_textBrowserVerify.clear()
        self.widget.send_textBrowserVerify.append('OK')
    def send_verifyShowFAIL(self):
        self.widget.send_textBrowserVerify.clear()
        self.widget.send_textBrowserVerify.append('FAIL')
    def send_btnSendArray(self):
        res = -1;
        try:
            typeNum, dataList, res, resText = decodeTextToArrey(self.widget.send_textEdit.toPlainText())
        except (ValueError,SyntaxError,TypeError):
            res = -1
            pass
        if res != 0:
            self.send_verifyShowFAIL()
            print('sys : error')
        else:
            self.widget.send_textEdit.clear();
            self.widget.send_textEdit.append(resText)
            self.send_verifyShowOK()
            if self.ser.isOpen() is False:
                return False
            self.ser.write(b'\xab\xab\xab')
            self.ser.write(pack('>B',typeNum))
            print(pack('>B',typeNum))
            dataBytes =len(dataList)*getTypeSize(typeNum)
            self.ser.write(pack('>H',dataBytes))
            print(pack('>B',len(dataList)))
            chkSum = sum(pack('>H',dataBytes))
            for data in dataList:
                self.ser.write(pack('<'+decodePackStr(typeNum),data))
                chkSum += sum(pack('<'+decodePackStr(typeNum),data));
                print(pack('<'+decodePackStr(typeNum),data))
                print(chkSum)
            self.ser.write(pack('>B',chkSum%256))
            self.widget.text_terminal.append('( log: send ' + str(dataBytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')
    def send_btnSendStruct(self):
        res = -1;
        res, resText = transStringToUi8(self.widget.send_textEdit.toPlainText())
        try:
            lineIdx, typeNumList, dataListList, res =decodeTextToStruct(resText)
        except (ValueError,SyntaxError,TypeError):
            res = -1
            pass
        if res != 0:
            self.send_verifyShowFAIL()
            print('sys : error')
        else:
            self.send_verifyShowOK()
            if self.ser.isOpen() is False:
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
            # if structBytes >= 255:
            #     print ('sys : error bytes >= 255')
            #     return False

            self.ser.write(b'\xab\xab\xab')
            structBytesH = structBytes>>8
            structBytesL = structBytes&0xFF
            self.ser.write(pack('>B',structBytesH))
            self.ser.write(pack('>B',structBytesL))
            chkSum += structBytesH + structBytesL

            self.ser.write(pack('>B',structTypeStringByte))
            self.ser.write(bytes(structTypeString, encoding = "ascii"))
            chkSum += sum(bytes(structTypeString, encoding = "ascii"));

            testData = bytearray();
            print(bytes(structTypeString, encoding = "ascii"))
            for idx, dataList in enumerate(dataListList):
                for data in dataList:
                    self.ser.write(pack('<'+decodePackStr(typeNumList[idx]),data))
                    chkSum += sum(pack('<'+decodePackStr(typeNumList[idx]),data));
                    testData+=(pack('<'+decodePackStr(typeNumList[idx]),data))
                    print(pack('<'+decodePackStr(typeNumList[idx]),data))
            self.ser.write(pack('>B',chkSum%256))
            print('chksum ' + str(chkSum%256))
            print(testData)
            print('formatString : ' + structTypeString)
            self.widget.send_textEdit.clear()
            self.widget.text_terminal.append('( log: send struct of ' + structTypeString +'. )')
    # ---- 發送區功能實現 end ---------------------------------------------------

    def updateTextFromLoadDialog(self):
        str = self.hmiLoadDialog.getArrayListStr()
        self.widget.send_textEdit.setText(str)

    def loseConnectHandler(self):
        self.text_appendLog('log: Lost connect with '+self.ser.port+'!')
        self.ser.close()
        self.widget.s_btnPortToggle.setText("開啟串列埠")
        self.mainWindow.setWindowTitle('ASA_HMI_Data_Agent   '+ 'Lost connect with '+self.ser.port+'!')
        self.s_updatePortlist()
