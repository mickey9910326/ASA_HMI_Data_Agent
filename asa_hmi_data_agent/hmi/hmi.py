from asa_hmi_data_agent.listport import getAvailableSerialPorts
from asa_hmi_data_agent.hmi.hmi_save_dialog import HmiSaveDialog
from asa_hmi_data_agent.hmi.hmi_load_dialog import HmiLoadDialog
from asa_hmi_data_agent.hmi.hmi_new_data_dialog import HmiNewDataDialog
from asa_hmi_data_agent.hmi.text_to_data import getFirstArray, getFirstStruct, getFirstMatrix
from asa_hmi_data_agent.hmi.text_to_data import isTextFormated, getFirstDataType, decodeText
from asa_hmi_data_agent.hmi.data_to_text import arToStr, stToStr, mtToStr
from asa_hmi_data_agent.ui.ui_hmi import Ui_MainWidgetHMI
from asa_hmi_data_agent import hmipac
import asa_hmi_data_agent.hmipac.type as tp
from asa_hmi_data_agent.hmicmd.decode import decode_cmd

from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QFileDialog, QGraphicsEllipseItem, QGraphicsScene
from PyQt5.QtGui import QColor

import numpy as np
import datetime
import scipy.io
import serial
import time
import sys
import os

# ---- class Serial Thread Start -----------------------------------------------
class SerialThread(QThread):
    sigGetStr        = pyqtSignal(str)
    sigGetLine       = pyqtSignal(str)
    sigGetArrayData  = pyqtSignal(np.ndarray)
    sigGetMatrixData = pyqtSignal(np.ndarray)
    sigGetStructData = pyqtSignal(np.ndarray)
    sigLoseConnect   = pyqtSignal()
    sigFatalError    = pyqtSignal()
    sigGetCmd = pyqtSignal(dict)
    
    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser
        self.hpd = hmipac.Decoder() # hmi packet decoder
        self.ch_buf = bytes()
        self.tbd = bytes()
        self.tbss = bytes()
        self.cmd_state = int(1)

    def run(self):
        while (self.ser.isOpen()):
            try:
                ch = self.ser.read(1)
                print("ch = {}".format(ch))
            except serial.serialutil.SerialException as e:
                self.sigLoseConnect.emit()
                break
            else:
                if ch == b'':
                    continue
                
                # decoder for data packet
                self.hpd.put(ch[0])
                if self.hpd.state is hmipac.DecoderState.NOTPROCESSING:
                    if len(self.ch_buf) > 0:
                        self.tbd += self.ch_buf
                    self.tbd += ch
                elif self.hpd.state is hmipac.DecoderState.PROCESSING:
                    self.ch_buf += ch
                elif self.hpd.state is hmipac.DecoderState.DONE:
                    packet = self.hpd.get()
                    if packet['type'] == hmipac.PacType.PAC_TYPE_AR:
                        self.ch_buf = bytes()
                        if packet['data'] is not None:
                            self.sigGetArrayData.emit(packet['data'])
                    elif packet['type'] == hmipac.PacType.PAC_TYPE_MT:
                        self.ch_buf = bytes()
                        if packet['data'] is not None:
                            self.sigGetMatrixData.emit(packet['data'])
                    elif packet['type'] == hmipac.PacType.PAC_TYPE_ST:
                        self.ch_buf = bytes()
                        if packet['data'] is not None:
                            self.sigGetStructData.emit(packet['data'])

                # decoder for cmd
                for c in self.tbd:
                    if self.cmd_state == 1:
                        if c == b'~'[0]:
                            self.cmd = b'~'
                            self.cmd_state = 2
                    elif self.cmd_state == 2:
                        if c == b'\r'[0] or c == b'\n'[0]:
                            try:
                                res = decode_cmd(self.cmd)
                            except:
                                pass
                            else:
                                if res:
                                    self.sigGetCmd.emit(res)
                            self.cmd_state = 1
                        else:
                            self.cmd += bytes([c])

                self.tbss += self.tbd
                self.tbd = bytes()

                try:
                    s = self.tbss.decode('utf8')
                    print("s={}".format(self.tbss))
                except:
                    pass
                else:
                    self.sigGetStr.emit(s)
                    self.tbss = bytes()
# ---- class Serial Thread End -------------------------------------------------

class HMI(QObject):
    sigChangeWindowTitle = pyqtSignal(str)
    sigSerialPortCheck = pyqtSignal(bool, str)
    text_newline_flag = bool(True)

    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget):
        super(HMI, self).__init__()
        self.ui = Ui_MainWidgetHMI()
        self.ui.setupUi(widget)
        self.hmiSaveDialog = HmiSaveDialog()
        self.hmiLoadDialog = HmiLoadDialog()
        self.hmiNewDataDialog = HmiNewDataDialog()
        
        # TODO 修改成非HARDCODE形式
        self.request_cmd = {
            'cmd': '',
            'class': '',
            'fs': ''
        }
        self.ack_flag = False
        
        self.send_updateBtnSend()
        self.send_updateWarningLight()
        self.rec_updateWarningLight()
        self.ui.rec_btnAddData.setEnabled(False)
        self.ui.rec_btnSend.setEnabled(False)
        self.ui.rec_btnReadFile.setEnabled(False)

        # ---- Serial object Init Start ----------------------------------------
        self.ser = serial.Serial()
        self.ser.baudrate = 38400
        self.ser.timeout = 1
        # ---- Serial object Init End ------------------------------------------

        # ---- Serial Thread Init Start ----------------------------------------
        self.SerialThread = SerialThread(self.ser)
        self.SerialThread.sigGetStr[str].connect(self.text_appendStrFromDevice)
        self.SerialThread.sigGetLine[str].connect(self.text_terminalAppendLineFromDevice)
        self.SerialThread.sigGetArrayData[np.ndarray].connect(self.rec_AppendArray)
        self.SerialThread.sigGetMatrixData[np.ndarray].connect(self.rec_AppendMatrix)
        self.SerialThread.sigGetStructData[np.ndarray].connect(self.rec_AppendStruct)
        self.SerialThread.sigLoseConnect.connect(self.loseConnectHandler)
        self.SerialThread.sigFatalError.connect(lambda:self.loseConnectHandler)
        self.SerialThread.sigGetCmd[dict].connect(self.doCmd)
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
        self.ui.rec_btnQuickSave.clicked.connect(lambda: self.quickSave(self.ui.rec_textEdit.toPlainText()))
        self.ui.rec_textEdit.textChanged.connect(self.rec_updateWarningLight)
        # 發送區
        self.ui.send_btnClear.clicked.connect(self.send_textEditClear)
        self.ui.send_btnMoveToSend.clicked.connect(self.rec_textEditMovetoSend)
        self.ui.send_btnReadFile.clicked.connect(self.hmiLoadDialog.show)
        self.ui.send_btnSend.clicked.connect(self.send_firstData)
        self.ui.send_btnSave.clicked.connect(lambda : self.hmiSaveDialog.showAndLoadText(self.ui.send_textEdit.toPlainText()))
        self.ui.send_btnQuickSave.clicked.connect(lambda : self.quickSave(self.ui.send_textEdit.toPlainText()))
        self.ui.send_textEdit.textChanged.connect(self.send_updateBtnSend)
        self.ui.send_textEdit.textChanged.connect(self.send_updateWarningLight)
        self.ui.send_btnAddData.clicked.connect(self.hmiNewDataDialog.show)
        # ---- Function Linking end --------------------------------------------

        # ---- HmiSaveDialog section start -------------------------------------
        self.hmiSaveDialog.accepted.connect(lambda : debugLog('HmiSaveDialog close'))
        # ---- HmiSaveDialog section end ---------------------------------------

        # ---- HmiLoadDialog section start -------------------------------------
        self.hmiLoadDialog.accepted.connect(self.updateTextFromLoadDialog)
        # ---- HmiLoadDialog section end ---------------------------------------

        self.hmiNewDataDialog.sigArrayAccept.connect(self.send_AppendArray)
        self.hmiNewDataDialog.sigMatrixAccept.connect(self.send_AppendMatrix)
        self.hmiNewDataDialog.sigStructAccept.connect(self.send_AppendStruct)

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
            try:
                self.ser.baudrate = self.ui.s_lineEditBaudrate.text()
                self.ser.baudrate = self.ui.s_lineEditBaudrate.text()
            except:
                debugLog('Baudrate setting is error!')
                self.hmilog('Baudrate setting is error!')
                return
            else:
                pass
            debugLog('Try to open port: {}'.format(self.ser.port))
            try:
                self.ser.open()
                self.sigChangeWindowTitle.emit('ASA_HMI_Data_Agent  - {} is opened.'.format(self.ser.port))

            except serial.serialutil.SerialException as e:
                debugLog('Open port {} failed!'.format(self.ser.port))
                self.hmilog('Open port {} failed!'.format(self.ser.port))
            else :
                self.s_updateUi_closeSerial()
                self.hmilog('Open {} success!'.format(self.ser.port))
                self.SerialThread.start()
        elif (self.ser.isOpen()):
            debugLog('Try to close port: {}'.format(self.ser.port))
            self.SerialThread.terminate()
            self.ser.close()
            self.sigChangeWindowTitle.emit('ASA_HMI_Data_Agent  - {} is closed.'.format(self.ser.port))
            self.s_updateUi_openSerial()
            debugLog('Close {} success!'.format(self.ser.port))
            self.hmilog('Close {} success!'.format(self.ser.port))
    
    def s_updateUi_closeSerial(self):
        self.ui.s_btnPortToggle.setText("關閉串列埠")
        self.ui.s_btnUpdatePortList.setEnabled(False)
        self.ui.s_portComboBox.setEnabled(False)
        self.ui.s_lineEditBaudrate.setEnabled(False)

    def s_updateUi_openSerial(self):
        self.ui.s_btnPortToggle.setText("開啟串列埠")
        self.ui.s_btnUpdatePortList.setEnabled(True)
        self.ui.s_portComboBox.setEnabled(True)
        self.ui.s_lineEditBaudrate.setEnabled(True)
    # ---- 串列埠設定區功能實現 end ----------------------------------------------

    # ---- 文字對話區功能實現 start ----------------------------------------------
    # Append the string from serial in terminal
    def text_appendStrFromDevice(self, s):
        for ch in s:
            if ch != '\n' and ch != '\r':
                if self.text_newline_flag:
                    self.text_appendStr('\n>>  ')
                    self.text_newline_flag = False
                self.text_appendStr(ch)

            elif ch == '\n':
                if self.text_newline_flag:
                    self.text_appendStr('\n>>  ')
                    self.text_newline_flag = False
                self.text_newline_flag = True

    # Append the line from serial in terminal
    def text_terminalAppendLineFromDevice(self, line):
        self.ui.text_terminal.append('>>  '+line)
        debugLog('Get  line: ' + line)
    
    def text_appendStr(self, s):
        text = self.ui.text_terminal.toPlainText() + s
        self.ui.text_terminal.setText(text)

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

    def text_send(self, s):
        if self.ser.isOpen() is False:
            return False
        else:
            line = s
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
    
    def rec_AppendMatrix(self, data):
        self.ui.rec_textEdit.append(mtToStr(data))
        y, x = data.shape
        self.hmilog('Get {t}_{y}x{x} matrix data.'.format(
            t = data.dtype.name,
            y = y,
            x = x
        ))
        debugLog('Get matrix: ' + str(data))

    def rec_AppendStruct(self, data):
        self.ui.rec_textEdit.append(stToStr(data))
        self.hmilog('Get  {} struct data.'.format(tp.getFs(data.dtype)))
        debugLog('Get struct: '+ str(data))

    def rec_updateWarningLight(self):
        text = self.ui.rec_textEdit.toPlainText()
        if isTextFormated(text):
            self.rec_setWarnLightGreen()
            self.ui.rec_btnQuickSave.setEnabled(True)
            self.ui.rec_btnSave.setEnabled(True)
        else:
            self.rec_setWarnLightRed()
            self.ui.rec_btnQuickSave.setEnabled(False)
            self.ui.rec_btnSave.setEnabled(False)

    def rec_setWarnLightGreen(self):
        scene = QGraphicsScene()
        item = QGraphicsEllipseItem(0, 30, 15, 15)
        item.setPen(QColor(65, 128, 17))
        item.setBrush(QColor(128, 174, 93))
        scene.addItem(item)
        self.ui.rec_graphicWarn.setScene(scene)

    def rec_setWarnLightRed(self):
        scene = QGraphicsScene()
        item = QGraphicsEllipseItem(0, 30, 15, 15)
        item.setPen(QColor(144, 25, 19))
        item.setBrush(QColor(196, 109, 104))
        scene.addItem(item)
        self.ui.rec_graphicWarn.setScene(scene)
    # ---- 接收區功能實現 end ---------------------------------------------------

    # ---- 發送區功能實現 start -------------------------------------------------
    def send_textEditClear(self):
        self.ui.send_textEdit.clear()
    
    def send_clear_request_cmd(self):
        self.request_cmd = {
            'cmd': '',
            'class': '',
            'fs': ''
        }

    def send_firstData(self):
        text = self.ui.send_textEdit.toPlainText()
        title = self.ui.send_btnSend.text()
        print(title)
        print(title == "ACK及發送陣列")
        print(title[0:3] == "ACK")
        if title[0:3] == "ACK":
            self.text_send("~Ready")
            time.sleep(0.1)
        t = getFirstDataType(text)
        if t == 1:
            usedLines, data = getFirstArray(text)
            packet = hmipac.encodeArToPac(data)
            self.hmilog('Send array data.')
        elif t == 2:
            usedLines, data = getFirstMatrix(text)
            packet = hmipac.encodeMtToPac(data)
            self.hmilog('Send matrix data.')
        elif t == 3:
            usedLines, data = getFirstStruct(text)
            packet = hmipac.encodeStToPac(data)
            self.hmilog('Send struct data.')

        self.ser.write(packet)
        lines = text.split('\n')
        text = '\n'.join(l for l in lines[usedLines::])
        self.ui.send_textEdit.clear()
        self.ui.send_textEdit.append(text)
        self.send_clear_request_cmd()


    def send_updateBtnSend(self):
        text = self.ui.send_textEdit.toPlainText()
        if isTextFormated(text):
            t = getFirstDataType(text)
            print(self.request_cmd)

            if self.request_cmd['cmd'] == 'put':
                if t == 1 and self.request_cmd['class'] == 'array':
                    usedLines, data = getFirstArray(text)
                    fs = tp.getArrayFs(data)
                    print(fs)
                    print(fs == self.request_cmd['fs'].decode('ascii'))
                    if fs == self.request_cmd['fs'].decode('ascii'):
                        self.ui.send_btnSend.setText("ACK及發送陣列")
                        self.ui.send_btnSend.setEnabled(True)
                    else:
                        self.ui.send_btnSend.setText("發送陣列")
                        self.ui.send_btnSend.setEnabled(True)
                elif t == 2 and self.request_cmd['class'] == 'matrix':
                    usedLines, data = getFirstMatrix(text)
                    fs = tp.getMatrixFs(data)
                    if fs == self.request_cmd['fs'].decode('ascii'):
                        self.ui.send_btnSend.setText("ACK及發送矩陣")
                        self.ui.send_btnSend.setEnabled(True)
                    else:
                        self.ui.send_btnSend.setText("發送矩陣")
                        self.ui.send_btnSend.setEnabled(True)
                elif t == 3 and self.request_cmd['class'] == 'struct':
                    usedLines, data = getFirstStruct(text)
                    fs = tp.getStructFs(data)
                    if fs == self.request_cmd['fs'].decode('ascii'):
                        self.ui.send_btnSend.setText("ACK及發送結構")
                        self.ui.send_btnSend.setEnabled(True)
                    else:
                        self.ui.send_btnSend.setText("發送結構")
                        self.ui.send_btnSend.setEnabled(True)
                else:
                    self.ui.send_btnSend.setText("發送資料")
                    self.ui.send_btnSend.setEnabled(False)
            else:
                if t == 1:
                    self.ui.send_btnSend.setText("發送陣列")
                    self.ui.send_btnSend.setEnabled(True)
                elif t == 2:
                    self.ui.send_btnSend.setText("發送矩陣")
                    self.ui.send_btnSend.setEnabled(True)
                elif t == 3:
                    self.ui.send_btnSend.setText("發送結構")
                    self.ui.send_btnSend.setEnabled(True)
                else:
                    self.ui.send_btnSend.setText("發送資料")
                    self.ui.send_btnSend.setEnabled(False)
        else:
            self.ui.send_btnSend.setText("發送資料")
            self.ui.send_btnSend.setEnabled(False)

    def send_updateWarningLight(self):
        text = self.ui.send_textEdit.toPlainText()
        if isTextFormated(text):
            self.send_setWarnLightGreen()
            self.ui.send_btnQuickSave.setEnabled(True)
            self.ui.send_btnSave.setEnabled(True)
        else:
            self.send_setWarnLightRed()
            self.ui.send_btnQuickSave.setEnabled(False)
            self.ui.send_btnSave.setEnabled(False)
    
    def send_setWarnLightGreen(self):
        scene = QGraphicsScene()
        item = QGraphicsEllipseItem(0, 30, 15, 15)
        item.setPen(QColor(65, 128, 17))
        item.setBrush(QColor(128,174,93))
        scene.addItem(item)
        self.ui.send_graphicWarn.setScene(scene)

    def send_setWarnLightRed(self):
        scene = QGraphicsScene()
        item = QGraphicsEllipseItem(0, 30, 15, 15)
        item.setPen(QColor(144, 25, 19))
        item.setBrush(QColor(196, 109, 104))
        scene.addItem(item)
        self.ui.send_graphicWarn.setScene(scene)
    
    def send_AppendArray(self, data):
        self.ui.send_textEdit.append(arToStr(data))

    def send_AppendMatrix(self, data):
        self.ui.send_textEdit.append(mtToStr(data))

    def send_AppendStruct(self, data):
        self.ui.send_textEdit.append(stToStr(data))
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
        self.ui.s_btnUpdatePortList.setEnabled(True)
        self.ui.s_portComboBox.setEnabled(True)
        self.ui.s_lineEditBaudrate.setEnabled(True)

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
                datalist = decodeText(text)
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
    
    # ---------------------
    def doCmd(self, cmd):
        print(cmd)
        if cmd['cmd'] == 'get':
            self.text_send('~ACK')
        elif cmd['cmd'] == 'put':
            self.request_cmd = cmd
            text = self.ui.send_textEdit.toPlainText()
            if isTextFormated(text):
                t = getFirstDataType(text)
                if t == 1 and cmd['class'] == 'array':
                    usedLines, data = getFirstArray(text)
                    print(data)
                    fs = tp.getArrayFs(data)
                    print(fs)
                    if fs == cmd['fs'].decode('ascii'):
                        self.send_firstData()
                    else:
                        self.text_send('~BZ')
                        self.updateUi_NewData(1, cmd['fs'])
                elif t == 2 and cmd['class'] == 'matrix':
                    usedLines, data = getFirstMatrix(text)
                    fs = tp.getMatrixFs(data)
                    if fs == cmd['fs'].decode('ascii'):
                        self.send_firstData()
                    else:
                        self.text_send('~BZ')
                        self.updateUi_NewData(2, cmd['fs'])
                elif t == 3 and cmd['class'] == 'struct':
                    usedLines, data = getFirstStruct(text)
                    fs = tp.getStructFs(data)
                    if fs == cmd['fs'].decode('ascii'):
                        self.send_firstData()
                    else:
                        self.text_send('~BZ')
                        self.updateUi_NewData(3, cmd['fs'])
                else:
                    self.text_send('~BZ')
                    if cmd['class'] == 'array':
                        self.updateUi_NewData(1, cmd['fs'])
                    elif cmd['class'] == 'matrix':
                        self.updateUi_NewData(2, cmd['fs'])
                    elif cmd['class'] == 'struct':
                        self.updateUi_NewData(3, cmd['fs'])
            else:
                self.text_send('~BZ')
                if cmd['class'] == 'array':
                    self.updateUi_NewData(1, cmd['fs'])
                elif cmd['class'] == 'matrix':
                    self.updateUi_NewData(2, cmd['fs'])
                elif cmd['class'] == 'struct':
                    self.updateUi_NewData(3, cmd['fs'])

    def updateUi_NewData(self, t, fs):
        fs = fs.decode('ascii')
        if t == 1:
            ss = fs.split('_')
            self.hmiNewDataDialog.comboBox_atype.setCurrentText(ss[0])
            self.hmiNewDataDialog.lineEdit_anum.setText(ss[1])
            self.hmiNewDataDialog.tabWidget.setCurrentIndex(0)
        elif t == 2:
            ss = fs.split('_')
            dim1, dim2 = ss[1].split('x')
            self.hmiNewDataDialog.comboBox_mtype.setCurrentText(ss[0])
            self.hmiNewDataDialog.lineEdit_dim1.setText(dim1)
            self.hmiNewDataDialog.lineEdit_dim2.setText(dim2)
            self.hmiNewDataDialog.tabWidget.setCurrentIndex(1)
        elif t == 3:
            self.hmiNewDataDialog.struct_addWithData(fs)
            self.hmiNewDataDialog.tabWidget.setCurrentIndex(2)
        else:
            pass


def debugLog(msg):
    s = '[{}] terminal log: {}'.format(
        datetime.datetime.now().strftime("%H:%M:%S"),
        msg
    )
    print(s)
