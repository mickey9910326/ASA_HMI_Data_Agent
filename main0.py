import sys
import serial
from decodeASAformat import *
from listport import serial_ports
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from ui_mainwindow import Ui_MainWindow
from ui_hmi import Ui_MainWidgetHMI
from ui_avrdude import Ui_MainWidgetAvrdude
from ui_asa_prog import Ui_MainWidgetAsaProg

class MainWindow(QMainWindow, Ui_MainWindow):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, parent=None):
        # ---- init ui start ---------------------------------------------------
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.widgetHmi = Ui_MainWidgetHMI()
        self.widgetAvrdude = Ui_MainWidgetAvrdude()
        self.WidgetAsaProg = Ui_MainWidgetAsaProg()
        self.widgetHmi.setupUi(self.tabHmi)
        self.widgetAvrdude.setupUi(self.tabAvrdude)
        self.WidgetAsaProg.setupUi(self.tabAsaProg)
        # ---- init ui end -----------------------------------------------------

        # ---- Public Objects Start --------------------------------------------
        self.ser = serial.Serial()
        self.isPortOpen = False
        self.ser.baudrate = 38400
        self.ser.timeout = 10
        # ---- Public Objects end ----------------------------------------------

        # ---- Button Function Linking start -----------------------------------
        # ------ HMI start -----------------------------------------------------
        # 串列埠設定區
        self.updatePortlist()
        self.widgetHmi.btnPortToggle.clicked.connect(self.portToggle)
        self.widgetHmi.btnUpdatePortList.clicked.connect(self.updatePortlist)
        # 文字對話區
        self.widgetHmi.text_lineEditToBeSend.returnPressed.connect(self.text_sendLineToDevice)
        self.widgetHmi.text_btnSend.clicked.connect(self.text_sendLineToDevice)
        self.widgetHmi.text_btnClearTerminal.clicked.connect(self.text_terminalClear)
        self.widgetHmi.text_btnSaveTerminal.clicked.connect(self.text_terminalSave)
        # 接收區
        self.widgetHmi.rec_btnClear.clicked.connect(self.rec_textEditClear)
        self.widgetHmi.rec_btnSave.clicked.connect(self.rec_textEditSave)
        self.widgetHmi.rec_btnMoveToSend.clicked.connect(self.rec_textEditMovetoSend)
        self.widgetHmi.rec_btnUi8ToString.clicked.connect(self.rec_textEditUi8ToString)
        self.widgetHmi.rec_btnStringToUi8.clicked.connect(self.rec_textEditStringToUi8)
        # 發送區
        self.widgetHmi.send_btnClear.clicked.connect(self.send_textEditClear)
        self.widgetHmi.send_btnSave.clicked.connect(self.send_textEditSave)
        self.widgetHmi.send_btnReadFile.clicked.connect(self.send)
        self.widgetHmi.send_btnUi8ToString.clicked.connect(self.send_textEditUi8ToString)
        self.widgetHmi.send_btnStringToUi8.clicked.connect(self.send_textEditStringToUi8)
        self.widgetHmi.send_btnSendStruct.clicked.connect(self.send)
        self.widgetHmi.send_btnSendArray.clicked.connect(self.send)
        # ------ HMI end -----------------------------------------------------
        # ---- Button Function Linking end -------------------------------------
    # ---- __init__ end --------------------------------------------------------



    # ---- 串列埠設定區功能實現 start --------------------------------------------
    # Update port list in portComboBox
    @pyqtSlot()
    def updatePortlist(self):
        print('sys : Update port list in portComboBox, available port : ', end='')
        availablePorts = serial_ports()
        print(availablePorts)
        self.widgetHmi.portComboBox.clear()
        for port in availablePorts:
            self.widgetHmi.portComboBox.addItem(port)

    # Open/Close serial port
    @pyqtSlot()
    def portToggle(self):
        if (self.widgetHmi.portComboBox.currentText() is '') and (self.isPortOpen is False) :
            pass
        elif (self.isPortOpen is False):
            self.ser.port = self.widgetHmi.portComboBox.currentText()
            print('sys : Try to open port : ' + self.ser.port )
            try:
                self.ser.open()
            except serial.serialutil.SerialException as e:
                print('sys : Open port ' + self.ser.port + ' failed ')
                print('     Exception : ', end='')
                print(e)
                self.widgetHmi.text_terminal.append('( log : Open port ' + self.ser.port + ' failed! )')
            else :
                self.isPortOpen = True
                self.widgetHmi.btnPortToggle.setText("關閉串列埠")
                self.widgetHmi.text_terminal.append('( log: Open ' + self.ser.port +' success! )')
                # SerialThread訊號槽
                # self.SerialThread = SerialThread(self.ser)
                # self.SerialThread.signalGetLine.connect(self.terminalAppendGetLine)
                # self.SerialThread.signalGetArrayData.connect(self.textGetAppendArray)
                # self.SerialThread.signalGetStructData.connect(self.textGetAppendStruct)
                # self.SerialThread.start()
        elif (self.isPortOpen is True):
            print('sys : Try to close port : ' + self.ser.port )
            self.ser.close()
            self.isPortOpen = False
            self.widgetHmi.btnPortToggle.setText("開啟串列埠")
            self.widgetHmi.text_terminal.append('( log: Close ' + self.ser.port +' success! )')
            # SerialThread
            # self.SerialThread.terminate()
    # ---- 串列埠設定區功能實現 end ----------------------------------------------

    # ---- 文字對話區功能實現 start ----------------------------------------------
    # Append the line from serial in terminal
    @pyqtSlot(str)
    def text_terminalAppendLineFromDevice(self, line):
        self.widgetHmi.text_terminal.append('>>  '+line)
        print('sys : Get line from devive: ' + line)

    # Send line to serial
    @pyqtSlot()
    def text_sendLineToDevice(self):
        if self.isPortOpen is False:
            return False
        else:
            line = self.widgetHmi.text_lineEditToBeSend.text()
            self.widgetHmi.text_lineEditToBeSend.clear()
            self.ser.write(bytes(line+'\n', encoding = "utf-8") )
            self.widgetHmi.text_terminal.append('<<  '+line)
            print('sys : Send line to devive: ' + line)

    # Svae the text in text terminal
    def text_terminalSave(self):
        text = self.widgetHmi.text_terminal.toPlainText()
        self.file_save(text)

    # Clear the text in text terminal
    def text_terminalClear(self):
        text = self.widgetHmi.text_terminal.clear()
    # ---- 文字對話區功能實現 end ------------------------------------------------

    # ---- 檔案讀寫 function start ----------------------------------------------
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
    # ---- 檔案讀寫 function end ------------------------------------------------

    # ---- 接收區功能實現 start -------------------------------------------------
    def rec_textEditClear(self):
        self.widgetHmi.rec_textEdit.clear()
    def rec_textEditSave(self):
        text = self.widgetHmi.rec_textEdit.toPlainText()
        self.file_save(text)
    def rec_textEditMovetoSend(self):
        text = self.widgetHmi.rec_textEdit.toPlainText()
        self.widgetHmi.rec_textEdit.clear()
        self.widgetHmi.textEditSend.append(text)
    def rec_textEditUi8ToString(self):
        res, resText = transUi8ToString(self.widgetHmi.rec_textEdit.toPlainText())
        self.widgetHmi.rec_textEdit.clear()
        self.widgetHmi.rec_textEdit.append(resText)
    def rec_textEditStringToUi8(self):
        res, resText = transStringToUi8(self.widgetHmi.rec_textEdit.toPlainText())
        self.widgetHmi.rec_textEdit.clear()
        self.widgetHmi.rec_textEdit.append(resText)
    # ---- 接收區功能實現 end ---------------------------------------------------

    # ---- 發送區功能實現 start -------------------------------------------------
    def send_textEditClear(self):
        self.widgetHmi.send_textEdit.clear()
    def send_textEditSave(self):
        text = self.widgetHmi.send_textEdit.toPlainText()
        self.file_save(text)
    def send_textEditUi8ToString(self):
        res, resText = transUi8ToString(self.widgetHmi.send_textEdit.toPlainText())
        self.widgetHmi.send_textEdit.clear()
        self.widgetHmi.send_textEdit.append(resText)
    def send_textEditStringToUi8(self):
        res, resText = transStringToUi8(self.widgetHmi.send_textEdit.toPlainText())
        self.widgetHmi.send_textEdit.clear()
        self.widgetHmi.send_textEdit.append(resText)
    def send_btnSendArray(self):
        # TODO implement
        # sendArray()
    def send_btnSendStruct(self):
        # TODO implement
        # sendStruct()
    def send_verifyShowOK(self):
        self.widgetHmi.send_textBrowserVerify.clear()
        self.widgetHmi.send_textBrowserVerify.append('OK')
    def send_verifyShowFAIL(self):
        self.widgetHmi.send_textBrowserVerify.clear()
        self.widgetHmi.send_textBrowserVerify.append('FAIL')
    # ---- 發送區功能實現 end ---------------------------------------------------

    # def btnSendStruct(self):
    #     res = -1;
    #     res, resText = transStringToUi8(self.textEditSend.toPlainText())
    #     try:
    #         lineIdx, typeNumList, dataListList, res =decodeTextToStruct(resText)
    #     except (ValueError,SyntaxError,TypeError):
    #         res = -1
    #         pass
    #     if res != 0:
    #         self.verifyFAIL()
    #         print('sys : error')
    #     else:
    #         self.verifyOK()
    #         if self.isPortOpen != True:
    #             return False
    #         structTypeString = str();
    #         structTypeStringByte = 0;
    #         structBytes = 0
    #         chkSum = 0
    #         for idx in range(len(typeNumList)):
    #             structTypeString += getTypeStr(typeNumList[idx]) + 'x' + str(len(dataListList[idx]))
    #             structBytes      += getTypeSize(typeNumList[idx]) * len(dataListList[idx])
    #             if idx != len(typeNumList)-1:
    #                 structTypeString += ','
    #         structTypeStringByte = len(structTypeString)
    #         if structBytes >= 255:
    #             print ('sys : error bytes >= 255')
    #             return False
    #         self.ser.write(b'\xab\xab\xab')
    #         self.ser.write(pack('>B',structBytes))
    #         self.ser.write(pack('>B',structTypeStringByte))
    #         self.ser.write(bytes(structTypeString, encoding = "ascii"))
    #         testData = bytearray();
    #         chkSum += sum(bytes(structTypeString, encoding = "ascii"));
    #         print(bytes(structTypeString, encoding = "ascii"))
    #         for idx, dataList in enumerate(dataListList):
    #             for data in dataList:
    #                 self.ser.write(pack('<'+decodePackStr(typeNumList[idx]),data))
    #                 chkSum += sum(pack('<'+decodePackStr(typeNumList[idx]),data));
    #                 testData+=(pack('<'+decodePackStr(typeNumList[idx]),data))
    #                 print(pack('<'+decodePackStr(typeNumList[idx]),data))
    #         self.ser.write(pack('>B',chkSum%256))
    #         print('chksum ' + str(chkSum%256))
    #         print(testData)
    #         print('formatString : ' + structTypeString)
    #         self.textEditSend.clear()
    #         self.widgetHmi.text_terminal.append('( log: send struct of ' + structTypeString +'. )')
    #
    #         # typeNumList, dataListList = decode_struct(structBytes,structTypeString,testData)
    #         # self.textGetAppendStruct(typeNumList, dataListList)
    #         # for value in variable:
    #         #     pass
    #         # print()
    #
    # def btnSendArray(self):
    #     # print(self.textEditSend.toPlainText())
    #     res = -1;
    #     try:
    #         typeNum, dataList, res, resText = decodeTextToArrey(self.textEditSend.toPlainText())
    #     except (ValueError,SyntaxError,TypeError):
    #         res = -1
    #         pass
    #     if res != 0:
    #         self.verifyFAIL()
    #         print('sys : error')
    #     else:
    #         self.textEditSend.clear();
    #         self.textEditSend.append(resText)
    #         self.verifyOK()
    #         if self.isPortOpen != True:
    #             return False
    #         self.ser.write(b'\xab\xab\xab')
    #         self.ser.write(pack('>B',typeNum))
    #         print(pack('>B',typeNum))
    #         dataBytes =len(dataList)*getTypeSize(typeNum)
    #         self.ser.write(pack('>B',dataBytes))
    #         print(pack('>B',len(dataList)))
    #         chkSum = 0
    #         for data in dataList:
    #             self.ser.write(pack('<'+decodePackStr(typeNum),data))
    #             chkSum += sum(pack('<'+decodePackStr(typeNum),data));
    #             print(pack('<'+decodePackStr(typeNum),data))
    #             print(chkSum)
    #         self.ser.write(pack('>B',chkSum%256))
    #         self.widgetHmi.text_terminal.append('( log: send ' + str(dataBytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')

    # # SerialThread訊號槽function
    # # 顯示array data
    # def textGetAppendArray(self,typeNum,bytes,array):
    #     print('sys : textGet append array data:' + str(array))
    #     self.textEditGet.append(getTypeStr(typeNum)+' : ')
    #     s = '  '
    #     for idx, data in enumerate(array):
    #         s += str(data)
    #         if idx+1 != len(array):
    #             s += ',  '
    #         else:
    #             self.textEditGet.append(s)
    #         if len(s) > 100: #換行
    #             self.textEditGet.append(s)
    #             s = '  '
    #     self.textEditGet.append('')
    #     self.widgetHmi.text_terminal.append('( log: get  ' + str(bytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')
    #
    # # 顯示Struct data
    # def textGetAppendStruct(self, typeNumList, dataListList, formatString):
    #     for idx in range(len(typeNumList)):
    #         typeNum = typeNumList[idx]
    #         dataList = dataListList[idx]
    #         self.textEditGet.append(getTypeStr(typeNum)+' : ')
    #         s = '  '
    #         for idx2, data in enumerate(dataList):
    #             s += str(data)
    #             if idx2+1 != len(dataList):
    #                 s += ',  '
    #             else:
    #                 self.textEditGet.append(s)
    #             if len(s) > 100: #換行
    #                 self.textEditGet.append(s)
    #                 s = '  '
    #         self.textEditGet.append('')
    #     self.widgetHmi.text_terminal.append('( log: get struct of ' + formatString +'. )')
    #



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
