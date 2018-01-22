import sys
import serial
from decodeASAformat import *
from listport import serial_ports
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

class HMI(object):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget, mainWindow):
        # super(MainWindow, self).__init__(parent)
        self.widget = widget
        self.mainWindow = mainWindow

        # ---- Serial object Init Start ----------------------------------------
        self.ser = serial.Serial()
        self.ser.isOpen = False
        self.ser.baudrate = 38400
        self.ser.timeout = 10
        self.ser.isOpen = False
        # ---- Serial object Init End ------------------------------------------

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
        self.widget.rec_btnSave.clicked.connect(self.rec_textEditSave)
        self.widget.rec_btnMoveToSend.clicked.connect(self.rec_textEditMovetoSend)
        self.widget.rec_btnUi8ToString.clicked.connect(self.rec_textEditUi8ToString)
        self.widget.rec_btnStringToUi8.clicked.connect(self.rec_textEditStringToUi8)
        # 發送區
        self.widget.send_btnClear.clicked.connect(self.send_textEditClear)
        self.widget.send_btnSave.clicked.connect(self.send_textEditSave)
        self.widget.send_btnReadFile.clicked.connect(self.send_textEditReadFile)
        self.widget.send_btnUi8ToString.clicked.connect(self.send_textEditUi8ToString)
        self.widget.send_btnStringToUi8.clicked.connect(self.send_textEditStringToUi8)
        # self.widget.send_btnSendStruct.clicked.connect(self.send)
        # self.widget.send_btnSendArray.clicked.connect(self.send)
        # ---- Function Linking end --------------------------------------------

    # ---- 串列埠設定區功能實現 start --------------------------------------------
    # Update port list in s_portComboBox
    def s_updatePortlist(self):
        if self.ser.isOpen is True :
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
        if (self.widget.s_portComboBox.currentText() is '') and (self.ser.isOpen is False) :
            pass
        elif (self.ser.isOpen is False):
            self.ser.port = self.widget.s_portComboBox.currentText()
            print('sys : Try to open port : ' + self.ser.port )
            try:
                self.ser.open()
            except serial.serialutil.SerialException as e:
                print('sys : Open port ' + self.ser.port + ' failed ')
                print('     Exception : ', end='')
                print(e)
                self.widget.text_terminal.append('( log : Open port ' + self.ser.port + ' failed! )')
            else :
                self.ser.isOpen = True
                self.widget.s_btnPortToggle.setText("關閉串列埠")
                self.widget.text_terminal.append('( log: Open ' + self.ser.port +' success! )')
                # SerialThread訊號槽
                # self.SerialThread = SerialThread(self.ser)
                # self.SerialThread.signalGetLine.connect(self.terminalAppendGetLine)
                # self.SerialThread.signalGetArrayData.connect(self.textGetAppendArray)
                # self.SerialThread.signalGetStructData.connect(self.textGetAppendStruct)
                # self.SerialThread.start()
        elif (self.ser.isOpen is True):
            print('sys : Try to close port : ' + self.ser.port )
            self.ser.close()
            self.ser.isOpen = False
            self.widget.s_btnPortToggle.setText("開啟串列埠")
            self.widget.text_terminal.append('( log: Close ' + self.ser.port +' success! )')
            # SerialThread
            # self.SerialThread.terminate()
    # ---- 串列埠設定區功能實現 end ----------------------------------------------

    # ---- 文字對話區功能實現 start ----------------------------------------------
    # Append the line from serial in terminal
    @pyqtSlot(str)
    def text_terminalAppendLineFromDevice(self, line):
        self.widget.text_terminal.append('>>  '+line)
        print('sys : Get line from devive: ' + line)

    # Send line to serial
    def text_sendLineToDevice(self):
        if self.ser.isOpen is False:
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
    def send_btnSendArray(self):
        pass
        # TODO implement
        # sendArray()
    def send_btnSendStruct(self):
        pass
        # TODO implement
        # sendStruct()
    def send_verifyShowOK(self):
        self.widget.send_textBrowserVerify.clear()
        self.widget.send_textBrowserVerify.append('OK')
    def send_verifyShowFAIL(self):
        self.widget.send_textBrowserVerify.clear()
        self.widget.send_textBrowserVerify.append('FAIL')
    # ---- 發送區功能實現 end ---------------------------------------------------
