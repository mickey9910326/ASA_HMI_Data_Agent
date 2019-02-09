from asa_hmi_data_agent.listport import getAvailableSerialPorts
from asa_hmi_data_agent.hmi.hmi_save_dialog import HmiSaveDialog
from asa_hmi_data_agent.hmi.hmi_load_dialog import HmiLoadDialog
from asa_hmi_data_agent.hmi.text_to_data import getFirstArray, getFirstStruct, textToData
from asa_hmi_data_agent.hmi.data_to_text import arToStr, stToStr
from asa_hmi_data_agent.ui.ui_hmi import Ui_MainWidgetHMI
from asa_hmi_data_agent import hmipac
import asa_hmi_data_agent.hmipac.type as tp

from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QFileDialog

import numpy as np
import datetime
import scipy.io
import serial
import sys
import os

# ---- class Serial Thread Start -----------------------------------------------
class SerialThread(QThread):
    sigGetLine       = pyqtSignal(str)
    sigGetArrayData  = pyqtSignal(np.ndarray)
    sigGetStructData = pyqtSignal(np.ndarray)
    sigLoseConnect   = pyqtSignal()
    sigFatalError    = pyqtSignal()

    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser

    def run(self):
        de = hmipac.Decoder()

        while (self.ser.isOpen()):
            try:
                ch = self.ser.read(1)
            except serial.serialutil.SerialException as e:
                self.sigLoseConnect.emit()
                break
            else:
                de.add_text(ch)
                try:
                    type, data = de.get()
                except:
                    sigFatalError.emit()
                else:
                    if type is 0:
                        pass
                    elif type is 1:
                        self.sigGetArrayData.emit(data)
                    elif type is 2:
                        self.sigGetStructData.emit(data)
                    elif type is 3:
                        self.sigGetLine.emit(data)

# ---- class Serial Thread End -------------------------------------------------

class HMI(QObject):
    sigChangeWindowTitle = pyqtSignal(str)
    sigSerialPortCheck = pyqtSignal(bool, str)

    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget):
        super(HMI, self).__init__()
        self.ui = Ui_MainWidgetHMI()
        self.ui.setupUi(widget)
        self.hmiSaveDialog = HmiSaveDialog()
        self.hmiLoadDialog = HmiLoadDialog()

        # ---- Serial object Init Start ----------------------------------------
        self.ser = serial.Serial()
        self.ser.baudrate = 38400
        self.ser.timeout = 10
        # ---- Serial object Init End ------------------------------------------

        # ---- Serial Thread Init Start ----------------------------------------
        self.SerialThread = SerialThread(self.ser)
        self.SerialThread.sigGetLine[str].connect(self.text_terminalAppendLineFromDevice)
        self.SerialThread.sigGetArrayData[np.ndarray].connect(self.rec_AppendArray)
        self.SerialThread.sigGetStructData[np.ndarray].connect(self.rec_AppendStruct)
        self.SerialThread.sigLoseConnect.connect(self.loseConnectHandler)
        self.SerialThread.sigFatalError.connect(lambda:self.loseConnectHandler)
        # ---- Serial Thread Init End ------------------------------------------

        # ---- Function Linking start ------------------------------------------
        # 串列埠設定區
        self.s_updatePortlist()
        self.ui.s_btnPortToggle.clicked.connect(self.s_portToggle)
        self.ui.s_btnUpdatePortList.clicked.connect(self.s_updatePortlist)
        # 文字對話區
        self.ui.text_lineEditToBeSend.returnPressed.connect(self.text_sendLineToDevice)
        self.ui.text_btnSend.clicked.connect(self.text_sendLineToDevice)
        self.ui.text_btnClearTerminal.clicked.connect(self.text_terminalClear)
        self.ui.text_btnSaveTerminal.clicked.connect(self.text_terminalSave)
        # 接收區
        self.ui.rec_btnClear.clicked.connect(self.rec_textEditClear)
        self.ui.rec_btnMoveToSend.clicked.connect(self.rec_textEditMovetoSend)
        self.ui.rec_btnSave.clicked.connect(lambda : self.hmiSaveDialog.showAndLoadText(self.ui.rec_textEdit.toPlainText()))
        self.ui.rec_btnQuickSave.clicked.connect(lambda : self.quickSave(self.ui.rec_textEdit.toPlainText()))
        # 發送區
        self.ui.send_btnClear.clicked.connect(self.send_textEditClear)
        self.ui.send_btnReadFile.clicked.connect(self.hmiLoadDialog.show)
        self.ui.send_btnSendArray.clicked.connect(self.send_btnSendArray)
        self.ui.send_btnSendStruct.clicked.connect(self.send_btnSendStruct)
        self.ui.send_btnSave.clicked.connect(lambda : self.hmiSaveDialog.showAndLoadText(self.ui.send_textEdit.toPlainText()))
        self.ui.send_btnQuickSave.clicked.connect(lambda : self.quickSave(self.ui.send_textEdit.toPlainText()))
        # ---- Function Linking end --------------------------------------------

        # ---- HmiSaveDialog section start -------------------------------------
        self.hmiSaveDialog.accepted.connect(lambda : debugLog('HmiSaveDialog close'))
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
            availablePorts = getAvailableSerialPorts()
            debugLog('Update ports: {}'.format(str(availablePorts)))
            self.ui.s_portComboBox.clear()
            for port in availablePorts:
                self.ui.s_portComboBox.addItem(port)

    # Open/Close serial port
    def s_portToggle(self):
        if (self.ui.s_portComboBox.currentText() is '') and (self.ser.isOpen() is False) :
            pass
        elif (self.ser.isOpen() is False):
            self.ser.port = self.ui.s_portComboBox.currentText()
            debugLog('Try to open port: {}'.format(self.ser.port))
            try:
                self.ser.open()
                self.sigChangeWindowTitle.emit('ASA_HMI_Data_Agent  - {} is opened.'.format(self.ser.port))

            except serial.serialutil.SerialException as e:
                debugLog('Open port {} failed!'.format(self.ser.port))
                self.hmilog('Open port {} failed!'.format(self.ser.port))
            else :
                self.ui.s_btnPortToggle.setText("關閉串列埠")
                self.hmilog('Open {} success!'.format(self.ser.port))
                self.SerialThread.start()
        elif (self.ser.isOpen()):
            debugLog('Try to close port: {}'.format(self.ser.port))
            self.SerialThread.terminate()
            self.ser.close()
            self.sigChangeWindowTitle.emit('ASA_HMI_Data_Agent  - {} is closed.'.format(self.ser.port))
            self.ui.s_btnPortToggle.setText("開啟串列埠")
            debugLog('Close {} success!'.format(self.ser.port))
            self.hmilog('Close {} success!'.format(self.ser.port))
    # ---- 串列埠設定區功能實現 end ----------------------------------------------

    # ---- 文字對話區功能實現 start ----------------------------------------------
    # Append the line from serial in terminal
    def text_terminalAppendLineFromDevice(self, line):
        self.ui.text_terminal.append('>>  '+line)
        debugLog('Get  line: ' + line)

    # Send line to serial
    def text_sendLineToDevice(self):
        if self.ser.isOpen() is False:
            return False
        else:
            line = self.ui.text_lineEditToBeSend.text()
            self.ui.text_lineEditToBeSend.clear()
            self.ser.write(bytes(line+'\n', encoding = "utf-8") )
            self.ui.text_terminal.append('<<  '+line)
            debugLog('Send line: ' + line)

    # Svae the text in text terminal
    def text_terminalSave(self):
        name, _ = QFileDialog.getSaveFileName(
            filter='txt Files (*.txt);;All Files(*)',
            initialFilter='txt Files (*.txt)'
        )
        if name is '':
            return
        text = self.ui.text_terminal.toPlainText()
        with open(name, 'w') as f:
            f.write(text)

    # Clear the text in text terminal
    def text_terminalClear(self):
        text = self.ui.text_terminal.clear()

    def hmilog(self, s):
        self.ui.text_terminal.append('(log: {})'.format(s))
    # ---- 文字對話區功能實現 end ------------------------------------------------

    # ---- 接收區功能實現 start -------------------------------------------------
    def rec_textEditClear(self):
        self.ui.rec_textEdit.clear()

    def rec_textEditMovetoSend(self):
        text = self.ui.rec_textEdit.toPlainText()
        self.ui.rec_textEdit.clear()
        self.ui.send_textEdit.append(text)

    def rec_AppendArray(self, data):
        self.ui.rec_textEdit.append(arToStr(data))
        self.hmilog('Get  {} {} array data.'.format(
            str(data.size),
            tp.getTypeStr(tp.getTypeNum(data.dtype.name))
        ))
        debugLog('Get array: '+ str(data))

    def rec_AppendStruct(self, data):
        self.ui.rec_textEdit.append(stToStr(data))
        self.hmilog('Get  {} struct data.'.format(tp.getFs(data.dtype)))
        debugLog('Get struct: '+ str(data))

    # ---- 接收區功能實現 end ---------------------------------------------------

    # ---- 發送區功能實現 start -------------------------------------------------
    def send_textEditClear(self):
        self.ui.send_textEdit.clear()

    def send_verifyShowOK(self):
        self.ui.send_textBrowserVerify.clear()
        self.ui.send_textBrowserVerify.append('OK')

    def send_verifyShowFAIL(self):
        self.ui.send_textBrowserVerify.clear()
        self.ui.send_textBrowserVerify.append('FAIL')

    def send_btnSendArray(self):
        text = self.ui.send_textEdit.toPlainText()
        try:
            usedLines, data = getFirstArray(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            debugLog('getFirstArray exception:' + str(type(e)))
            self.send_verifyShowFAIL()
        else:
            self.ser.write(hmipac.encodeArToPac(data))
            lines = text.split('\n')
            if usedLines == len(lines):
                text = ''
            else:
                text = '\n'.join(l for l in lines[usedLines::])
            self.ui.send_textEdit.clear()
            self.ui.send_textEdit.append(text)
            self.hmilog('Send {} {} array data.'.format(
                str(data.size),
                tp.getTypeStr(tp.getTypeNum(data.dtype.name))
            ))

    def send_btnSendStruct(self):
        text = self.ui.send_textEdit.toPlainText()
        try:
            usedLines, data = getFirstStruct(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            debugLog('getFirstStruct exception:' + str(type(e)))
            self.send_verifyShowFAIL()
        else:
            self.ser.write(hmipac.encodeStToPac(data))
            lines = text.split('\n')
            text = '\n'.join(l for l in lines[usedLines::])
            self.ui.send_textEdit.clear()
            self.ui.send_textEdit.append(text)
            self.hmilog('Send {} struct data.'.format(tp.getFs(data.dtype)))

    # ---- 發送區功能實現 end ---------------------------------------------------

    def updateTextFromLoadDialog(self):
        if self.hmiLoadDialog.resText != '':
            self.ui.send_textEdit.append(self.hmiLoadDialog.resText)

    def loseConnectHandler(self):
        self.hmilog('log: Lost connect with '+self.ser.port+'!')
        self.ser.close()
        self.ui.s_btnPortToggle.setText("開啟串列埠")
        self.sigChangeWindowTitle.emit('ASA_HMI_Data_Agent  - Lost connect with {}!'.format(self.ser.port))
        self.s_updatePortlist()

    def fatalErrorHandler(self):
        self.hmilog('log: Fatal error 請確認M128程式正確，並重新開啟串列埠!')
        self.ser.close()
        self.ui.s_btnPortToggle.setText("開啟串列埠")
        self.sigChangeWindowTitle.emit('ASA_HMI_Data_Agent  - {} is closed.'.format(self.ser.port))
        self.s_updatePortlist()

    def quickSave(self, text):
        name, _ = QFileDialog.getSaveFileName(
            filter='Mat Files (*.mat);;txt Files (*.txt)',
            initialFilter='Mat Files (*.mat)'
        )
        if name is '':
            return

        file_extension = os.path.splitext(name)[-1]
        if file_extension == '.txt':
            with open(name, 'w') as f:
                f.write(text)
        elif file_extension == '.mat':
            try:
                datalist = textToData(text)
            except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
                # TODO ERROR Dialog
                debugLog('quickSave exception: ' + str(type(e)) )
                pass
            else:
                d = dict()
                for i in range(len(datalist)):
                    d['data'+str(i)] = datalist[i]
                scipy.io.savemat(name, d)
        elif file_extension == '.csv':
            pass
        else:
            with open(name, 'w') as f:
                f.write(text)

def debugLog(msg):
    s = '[{}] terminal log: {}'.format(
        datetime.datetime.now().strftime("%H:%M:%S"),
        msg
    )
    print(s)
