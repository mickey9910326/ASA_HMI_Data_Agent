import sys
import serial
from asa_hmi_data_agent.listport import serial_ports
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
# from asa_hmi_data_agent.hmi.decodeASAformat import *
from asa_hmi_data_agent.hmi.hmi_save_dialog import HmiSaveDialog
from asa_hmi_data_agent.hmi.hmi_load_dialog import HmiLoadDialog
from asa_hmi_data_agent import hmipac
from .text_to_data import getFirstArray, getFirstStruct
from .data_to_text import arToStr, stToStr

import numpy as np

# ---- class Serial Thread Start -----------------------------------------------
class SerialThread(QThread):
    signalGetLine = pyqtSignal(str)
    signalGetArrayData = pyqtSignal(np.ndarray)
    signalGetStructData = pyqtSignal(np.ndarray)
    signalLoseConnect   = pyqtSignal()

    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser

    def run(self):
        de = hmipac.Decoder()

        while (self.ser.isOpen()):
            try:
                ch = self.ser.read(1)
            except serial.serialutil.SerialException as e:
                self.signalLoseConnect.emit()
                break
            else:
                de.add_text(ch)
                type, data = de.get()
                # print(de.get_text())
                if type is 0:
                    pass
                elif type is 1:
                    print(data)
                    self.signalGetArrayData.emit(data)
                elif type is 2:
                    print(data)
                    self.signalGetStructData.emit(data)
                elif type is 3:
                    self.signalGetLine.emit(data)

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
        self.SerialThread.signalGetArrayData[np.ndarray].connect(self.rec_AppendArray)
        self.SerialThread.signalGetStructData[np.ndarray].connect(self.rec_AppendStruct)
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

    def rec_AppendArray(self, data):
        # print('sys : textGet append array data:' + str(array))
        self.widget.rec_textEdit.append(arToStr(data))
        # self.widget.text_terminal.append('( log: get  ' + str(bytes) + ' bytes of ' + getTypeStr(typeNum) +' data. )')

    def rec_AppendStruct(self, data):
        self.widget.rec_textEdit.append(stToStr(data))
        # self.widget.text_terminal.append('( log: get struct of ' + formatString +'. )')
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
        text = self.widget.send_textEdit.toPlainText()
        try:
            usedLines, data = getFirstArray(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            print('sys : error')
            self.send_verifyShowFAIL()
        else:
            self.ser.write(hmipac.encodeArToPac(data))
            lines = text.split('\n')
            if usedLines == len(lines):
                text = ''
            else:
                text = '\n'.join(l for l in lines[usedLines::])
            self.widget.send_textEdit.clear()
            self.widget.send_textEdit.append(text)

    def send_btnSendStruct(self):
        text = self.widget.send_textEdit.toPlainText()
        try:
            usedLines, data = getFirstStruct(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            print('sys : error')
            self.send_verifyShowFAIL()
        else:
            self.ser.write(hmipac.encodeStToPac(data))
            lines = text.split('\n')
            text = '\n'.join(l for l in lines[usedLines::])
            self.widget.send_textEdit.clear()
            self.widget.send_textEdit.append(text)

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
