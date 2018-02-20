from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import serial
from listport import serial_ports

def radioButtonClick(btn):
    print(btn.text())
    # print(btn.isChecked())
    if btn.isChecked() is True:
        print(btn.text())
        # btn.setChecked(False)
        btn.setAutoExclusive(False)
        btn.setChecked(False)
        btn.setAutoExclusive(True)


class Avrdude(object):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget, mainWindow):
        self.widget = widget
        self.mainWindow = mainWindow

        # ---- Serial object Init Start ----------------------------------------
        self.ser = serial.Serial()
        self.ser.baudrate = 38400
        self.ser.timeout = 10
        self.ser.isOpen = False
        # ---- Serial object Init End ------------------------------------------

        # ---- Serial Group start ----------------------------------------------
        self.serial_updatePortlist()
        self.widget.pushButton_updatePort.clicked.connect(self.serial_updatePortlist)
        self.widget.lineEdit_serialSetBaud.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_serialSetBaud.setText("38400")
        # ---- Serial Group end ------------------------------------------------

        # ---- Flash Group start -----------------------------------------------
        self.widget.toolButton_flash.clicked.connect(self.flash_chooseBinaryFile)
        self.widget.radioButton_flashWrite.setAutoExclusive(False)
        self.widget.radioButton_flashRead.setAutoExclusive(False)
        self.widget.radioButton_flashVerify.setAutoExclusive(False)
        self.widget.radioButton_flashWrite.clicked.connect (lambda:self.flash_radioButtonClick(self.widget.radioButton_flashWrite))
        self.widget.radioButton_flashRead.clicked.connect  (lambda:self.flash_radioButtonClick(self.widget.radioButton_flashRead))
        self.widget.radioButton_flashVerify.clicked.connect(lambda:self.flash_radioButtonClick(self.widget.radioButton_flashVerify))
        # ---- Flash Group end -------------------------------------------------

        # ---- Eeprom Group start ----------------------------------------------
        self.widget.toolButton_eeprom.clicked.connect(self.eeprom_chooseBinaryFile)
        self.widget.radioButton_eepromWrite.setAutoExclusive(False)
        self.widget.radioButton_eepromRead.setAutoExclusive(False)
        self.widget.radioButton_eepromVerify.setAutoExclusive(False)
        self.widget.radioButton_eepromWrite.clicked.connect (lambda:self.eeprom_radioButtonClick(self.widget.radioButton_eepromWrite))
        self.widget.radioButton_eepromRead.clicked.connect  (lambda:self.eeprom_radioButtonClick(self.widget.radioButton_eepromRead))
        self.widget.radioButton_eepromVerify.clicked.connect(lambda:self.eeprom_radioButtonClick(self.widget.radioButton_eepromVerify))
        # ---- Eeprom Group end ------------------------------------------------

        self.widget.checkBox_eraseChip.setChecked(True)
        self.updateCammand()
        self.widget.pushButton_startProgram.clicked.connect(self.updateCammand)



    # check all items and update cmd in line
    def updateCammand(self):
        cmd = str()
        cmd += 'avrdude'
        cmd += ' -c stk500'

        if  self.widget.comboBox_mcuSelect.currentIndex() > 0:
            cmd += ' -p ' + self.widget.comboBox_mcuSelect.currentText()

        cmd += ' -b ' + self.widget.lineEdit_serialSetBaud.text()

        if self.widget.comboBox_serialSetPort.currentText() is not '':
            cmd += ' -P ' + self.widget.comboBox_serialSetPort.currentText()

        if self.widget.checkBox_eraseChip.isChecked():
            cmd += ' -e'

        if self.widget.checkBox_cancelVerify.isChecked():
            cmd += ' -V'

        if self.widget.lineEdit_additionalParameter.text() is not '':
            cmd += ' ' + self.widget.lineEdit_additionalParameter.text()

        tmp = self.flash_radioButtonCheck()
        if tmp is not '':
            cmd += ' -U flash:' + tmp + ':' + self.widget.lineEdit_flash.text()
            if tmp is 'r':
                cmd += ':i'

        tmp = self.eeprom_radioButtonCheck()
        if tmp is not '':
            cmd += ' -U eeprom:' + tmp + ':' + self.widget.lineEdit_flash.text()
            if tmp is 'r':
                cmd += ':i'

        if self.widget.checkBox_fuseSet.isChecked():
            cmd += ' -U hfuse:w:' + self.widget.lineEdit_fuseHigh.text()  + ':m'
            cmd += ' -U lfuse:w:' + self.widget.lineEdit_fuseLow.text()   + ':m'
            cmd += ' -U efuse:w:' + self.widget.lineEdit_fuseExtra.text() + ':m'

        if self.widget.checkBox_lockSet.isChecked():
            cmd += ' -U lock:w:' + self.widget.lineEdit_lock.text() + ':m'

        self.widget.textBrowser_cmd.clear()
        self.widget.textBrowser_cmd.append(cmd)

    # ---- Serial Group start --------------------------------------------------
    # Update port list in s_portComboBox
    def serial_updatePortlist(self):
        availablePorts = serial_ports()
        print('sys : Update port list in portComboBox, available port : ', end='')
        print(availablePorts)
        self.widget.comboBox_serialSetPort.clear()
        for port in availablePorts:
            self.widget.comboBox_serialSetPort.addItem(port)
    # ---- Serial Group end ----------------------------------------------------

    # ---- Flash Group start ---------------------------------------------------
    def flash_chooseBinaryFile(self):
        name, _ = QFileDialog.getOpenFileName(self.mainWindow, 'Open File','', 'All Files (*);;Hex Files (*.hex)' ,initialFilter='Hex Files (*.hex)')
        if name is not '':
            self.widget.lineEdit_flash.setText(name)

    def flash_radioButtonClick(self,btn):
        if btn is not self.widget.radioButton_flashWrite:
            self.widget.radioButton_flashWrite.setChecked(0)
        if btn is not self.widget.radioButton_flashRead:
            self.widget.radioButton_flashRead.setChecked(0)
        if btn is not self.widget.radioButton_flashVerify:
            self.widget.radioButton_flashVerify.setChecked(0)
        self.updateCammand();

    def flash_radioButtonCheck(self):
        if self.widget.radioButton_flashWrite.isChecked():
            return 'w'
        elif self.widget.radioButton_flashRead.isChecked():
            return 'r'
        elif self.widget.radioButton_flashVerify.isChecked():
            return 'v'
        else:
            return ''

    def flash_execute(self):
        pass
    # ---- Flash Group end -----------------------------------------------------

    # ---- Eeprom Group start --------------------------------------------------
    def eeprom_chooseBinaryFile(self):
        name, _ = QFileDialog.getOpenFileName(self.mainWindow, 'Open File','', 'All Files (*);;Hex Files (*.hex)' ,initialFilter='Hex Files (*.hex)')
        if name is not '':
            self.widget.lineEdit_eeprom.setText(name)

    def eeprom_radioButtonClick(self,btn):
        if btn is not self.widget.radioButton_eepromWrite:
            self.widget.radioButton_eepromWrite.setChecked(0)
        if btn is not self.widget.radioButton_eepromRead:
            self.widget.radioButton_eepromRead.setChecked(0)
        if btn is not self.widget.radioButton_eepromVerify:
            self.widget.radioButton_eepromVerify.setChecked(0)
        self.updateCammand();

    def eeprom_radioButtonCheck(self):
        if self.widget.radioButton_eepromWrite.isChecked():
            return 'w'
        elif self.widget.radioButton_eepromRead.isChecked():
            return 'r'
        elif self.widget.radioButton_eepromVerify.isChecked():
            return 'v'
        else:
            return ''

    def eeprom_execute(self):
        pass
    # ---- Eeprom Group end ----------------------------------------------------
