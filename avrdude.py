from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import serial
from listport import serial_ports
import subprocess
import time

from avrdudeConfParser import AvrdudeConfParser
from configparser import ConfigParser

# ---- class ShellThread Start -------------------------------------------------
class ShellThread(QThread):

    signalGetLine = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.cmd = str()

    def setCmd(self, cmd):
        self.cmd = cmd

    def run(self):
        times = time.strftime("%H:%M:%S", time.gmtime())
        self.signalGetLine.emit('[' + times + '] ' + self.cmd + '\n')
        self.shellIsRunning = True

        self.p = subprocess.Popen(self.cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        while self.p.poll() is None:
            s = self.p.stderr.readline()
            if(s.decode("big5") is not ''):
                self.signalGetLine.emit(s.decode("big5"))

    def stop(self):
        if self.shellIsRunning or self.p.poll() is None:
            self.shellIsRunning = False
            self.p.kill()
        else:
            pass
        self.terminate()

# ---- class ShellThread End ---------------------------------------------------

# ---- class radioButtonClick Start --------------------------------------------
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

        # ---- Settings Group start --------------------------------------------
        self.settingsFile = 'avrdude_settings.ini'
        self.conf = ConfigParser()
        self.settingsListUpdate()
        self.settingsLoad()
        self.widget.pushButton_configSave.clicked.connect(self.settingsSave)
        self.widget.pushButton_configDelete.clicked.connect(self.settingsDelete)
        self.widget.comboBox_config.currentIndexChanged.connect(self.settingsLoad)
        # ---- Settings Group end ----------------------------------------------

        # ---- Serial object Init Start ----------------------------------------
        self.ser = serial.Serial()
        self.ser.baudrate = 38400
        self.ser.timeout = 10
        self.ser.isOpen = False
        # ---- Serial object Init End ------------------------------------------

        # ---- Shell Thread Init Start -----------------------------------------
        self.shellThread = ShellThread()
        self.shellThread.signalGetLine[str].connect(self.terminalAppendLine)
        # ---- Shell Thread Init End -------------------------------------------

        # ---- Serial Group start ----------------------------------------------
        self.serial_updatePortlist()
        self.widget.pushButton_updatePort.clicked.connect(self.serial_updatePortlist)
        self.widget.lineEdit_serialSetBaud.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_serialSetBaud.setText('38400')
        # ---- Serial Group end ------------------------------------------------

        # ---- Flash Group start -----------------------------------------------
        self.widget.toolButton_flash.clicked.connect(self.flash_chooseBinaryFile)
        self.widget.pushButton_flashGo.clicked.connect(self.flash_execute)
        self.widget.radioButton_flashWrite.clicked.connect (lambda:self.flash_radioButtonClick(self.widget.radioButton_flashWrite))
        self.widget.radioButton_flashRead.clicked.connect  (lambda:self.flash_radioButtonClick(self.widget.radioButton_flashRead))
        self.widget.radioButton_flashVerify.clicked.connect(lambda:self.flash_radioButtonClick(self.widget.radioButton_flashVerify))
        # ---- Flash Group end -------------------------------------------------

        # ---- Eeprom Group start ----------------------------------------------
        self.widget.toolButton_eeprom.clicked.connect(self.eeprom_chooseBinaryFile)
        self.widget.pushButton_eepromGo.clicked.connect(self.eeprom_execute)
        self.widget.radioButton_eepromWrite.clicked.connect (lambda:self.eeprom_radioButtonClick(self.widget.radioButton_eepromWrite))
        self.widget.radioButton_eepromRead.clicked.connect  (lambda:self.eeprom_radioButtonClick(self.widget.radioButton_eepromRead))
        self.widget.radioButton_eepromVerify.clicked.connect(lambda:self.eeprom_radioButtonClick(self.widget.radioButton_eepromVerify))
        # ---- Eeprom Group end ------------------------------------------------

        # ---- Fuse & Lock Group start ---------------------------------------
        self.widget.lineEdit_lock.setText('0x00')
        self.widget.lineEdit_fuseHigh.setText('0x00')
        self.widget.lineEdit_fuseLow.setText('0x00')
        self.widget.lineEdit_fuseExtra.setText('0x00')
        # ---- Fuse & Lock Group end -----------------------------------------

        # ---- MCU Group start -------------------------------------------------
        self.praser = AvrdudeConfParser()
        descList = self.praser.listAllPartDesc()

        self.widget.pushButton_mcuDetect.clicked.connect(self.mcu_detect)
        self.widget.comboBox_mcuSelect.clear()
        self.widget.comboBox_mcuSelect.addItem('請選擇MCU...')
        for desc in descList:
            self.widget.comboBox_mcuSelect.addItem(desc)
        # ---- MCU Group end ---------------------------------------------------

        # ---- need updateCammand items start ----------------------------------
        self.widget.comboBox_serialSetPort.currentIndexChanged.connect(self.updateCammand)
        self.widget.comboBox_mcuSelect.currentIndexChanged.connect(self.updateCammand)

        self.widget.checkBox_lockSet.clicked.connect(self.updateCammand)
        self.widget.checkBox_fuseSet.clicked.connect(self.updateCammand)
        self.widget.checkBox_eraseChip.clicked.connect(self.updateCammand)
        self.widget.checkBox_cancelVerify.clicked.connect(self.updateCammand)

        self.widget.lineEdit_lock.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_flash.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_eeprom.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_fuseHigh.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_fuseLow.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_fuseExtra.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_serialSetBaud.textChanged.connect(self.updateCammand)
        self.widget.lineEdit_additionalParameter.textChanged.connect(self.updateCammand)
        # ---- need updateCammand items end ------------------------------------

        self.widget.checkBox_eraseChip.setChecked(True)
        self.updateCammand()
        self.widget.pushButton_startProgram.clicked.connect(self.startProgram)
        self.widget.pushButton_stopProgram.clicked.connect(self.stopProgram)

    def startProgram(self):
        self.updateCammand()
        self.shellThread.setCmd(self.widget.textBrowser_cmd.toPlainText())
        self.shellThread.start()

    def stopProgram(self):
        self.shellThread.stop()

    def getBasicParameter(self):
        cmd = str()
        cmd += 'avrdude'
        cmd += ' -c stk500'

        if  self.widget.comboBox_mcuSelect.currentIndex() > 0:
            desc = self.widget.comboBox_mcuSelect.currentText()
            desc, id, signature = self.praser.GetBasicInfoByDesc(desc)
            cmd += ' -p ' + id

        cmd += ' -b ' + self.widget.lineEdit_serialSetBaud.text()

        if self.widget.comboBox_serialSetPort.currentText() is not '':
            cmd += ' -P ' + self.widget.comboBox_serialSetPort.currentText()
        return cmd

    # check all items and update cmd in line
    def updateCammand(self):
        cmd = str()
        cmd += 'avrdude'
        cmd += ' -c stk500'

        if  self.widget.comboBox_mcuSelect.currentIndex() > 0:
            desc = self.widget.comboBox_mcuSelect.currentText()
            desc, id, signature = self.praser.GetBasicInfoByDesc(desc)
            cmd += ' -p ' + id

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
            cmd += ' -U flash:' + tmp + ':"' + self.widget.lineEdit_flash.text() + '":i'

        tmp = self.eeprom_radioButtonCheck()
        if tmp is not '':
            cmd += ' -U eeprom:' + tmp + ':' + self.widget.lineEdit_flash.text() + '":i'

        if self.widget.checkBox_fuseSet.isChecked():
            cmd += ' -U hfuse:w:' + self.widget.lineEdit_fuseHigh.text()  + ':m'
            cmd += ' -U lfuse:w:' + self.widget.lineEdit_fuseLow.text()   + ':m'
            cmd += ' -U efuse:w:' + self.widget.lineEdit_fuseExtra.text() + ':m'

        if self.widget.checkBox_lockSet.isChecked():
            cmd += ' -U lock:w:' + self.widget.lineEdit_lock.text() + ':m'

        self.widget.textBrowser_cmd.clear()
        self.widget.textBrowser_cmd.append(cmd)

    def terminalAppendLine(self, s):
        self.widget.textBrowser_cmdterminal.insertPlainText(s)

    # ---- Settings Group start ------------------------------------------------
    def settingsListUpdate(self):
        self.conf.read(self.settingsFile)
        self.widget.comboBox_config.clear()
        for section in self.conf.sections():
            self.widget.comboBox_config.addItem(section)

    def settingsSave(self):
        section = self.widget.comboBox_config.currentText()
        if self.conf.has_section(section) is False:
            self.conf.add_section(section)
        self.conf.set(section, 'port', self.widget.comboBox_serialSetPort.currentText())
        self.conf.set(section, 'baud', self.widget.lineEdit_serialSetBaud.text())
        self.conf.set(section, 'mcu', self.widget.comboBox_mcuSelect.currentText())
        self.conf.set(section, 'flashFile', self.widget.lineEdit_flash.text())
        self.conf.set(section, 'flashExecType', self.flash_radioButtonCheck())
        self.conf.set(section, 'eepromFile', self.widget.lineEdit_eeprom.text())
        self.conf.set(section, 'eepromExecType', self.eeprom_radioButtonCheck())
        self.conf.set(section, 'fuseL', self.widget.lineEdit_fuseLow.text())
        self.conf.set(section, 'fuseH', self.widget.lineEdit_fuseHigh.text())
        self.conf.set(section, 'fuseE', self.widget.lineEdit_fuseExtra.text())
        self.conf.set(section, 'lock', self.widget.lineEdit_lock.text())
        self.conf.set(section, 'fuseSet', str(self.widget.checkBox_fuseSet.isChecked()))
        self.conf.set(section, 'lockSet', str(self.widget.checkBox_lockSet.isChecked()))

        self.conf.set(section, 'cancelVerify', str(self.widget.checkBox_cancelVerify.isChecked()))
        self.conf.set(section, 'earseChip',    str(self.widget.checkBox_eraseChip.isChecked()))
        self.conf.set(section, 'additionalParameter', self.widget.lineEdit_additionalParameter.text())

        with open(self.settingsFile, 'w') as configfile:
            self.conf.write(configfile)
        self.widget.comboBox_config.setCurrentText(section)
        self.settingsListUpdate()

    def settingsLoad(self):
        section = self.widget.comboBox_config.currentText()
        if section is '':
            return
        self.widget.comboBox_serialSetPort.setCurrentText(self.conf[section]['port'])
        self.widget.lineEdit_serialSetBaud.setText(self.conf[section]['baud'])
        self.widget.comboBox_mcuSelect.setCurrentText(self.conf[section]['mcu'])
        self.widget.lineEdit_flash.setText(self.conf[section]['flashfile'])
        self.flash_radioButtonSet(self.conf[section]['flashexectype'])
        self.widget.lineEdit_eeprom.setText(self.conf[section]['eepromfile'])
        self.eeprom_radioButtonSet(self.conf[section]['eepromexectype'])
        self.widget.lineEdit_fuseLow.setText(self.conf[section]['fusel'])
        self.widget.lineEdit_fuseHigh.setText(self.conf[section]['fuseh'])
        self.widget.lineEdit_fuseExtra.setText(self.conf[section]['fusee'])
        self.widget.lineEdit_lock.setText(self.conf[section]['lock'])
        self.widget.checkBox_fuseSet.setChecked(self.conf.getboolean(section,'fuseset'))
        self.widget.checkBox_lockSet.setChecked(self.conf.getboolean(section,'lockset'))
        self.widget.checkBox_cancelVerify.setChecked(self.conf.getboolean(section,'cancelverify'))
        self.widget.checkBox_eraseChip.setChecked(self.conf.getboolean(section,'earsechip'))
        self.widget.lineEdit_additionalParameter.setText(self.conf[section]['additionalparameter'])

    def settingsDelete(self):
        section = self.widget.comboBox_config.currentText()
        self.conf.remove_section(section)
        with open(self.settingsFile, 'w') as configfile:
            self.conf.write(configfile)
        self.settingsListUpdate()
    # ---- Settings Group end --------------------------------------------------

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

    def flash_radioButtonSet(self, execType):
        if execType is 'w':
            self.widget.radioButton_flashWrite.setChecked(True)
            self.widget.radioButton_flashRead.setChecked(False)
            self.widget.radioButton_flashVerify.setChecked(False)
        elif execType is 'r':
            self.widget.radioButton_flashWrite.setChecked(False)
            self.widget.radioButton_flashRead.setChecked(True)
            self.widget.radioButton_flashVerify.setChecked(False)
        elif execType is 'v':
            self.widget.radioButton_flashWrite.setChecked(False)
            self.widget.radioButton_flashRead.setChecked(False)
            self.widget.radioButton_flashVerify.setChecked(True)
        else:
            self.widget.radioButton_flashWrite.setChecked(False)
            self.widget.radioButton_flashRead.setChecked(False)
            self.widget.radioButton_flashVerify.setChecked(False)

    def flash_execute(self):
        cmd = self.getBasicParameter()
        tmp = self.flash_radioButtonCheck()
        if tmp is not '':
            cmd += ' -U flash:' + tmp + ':"' + self.widget.lineEdit_flash.text() + '":i'
        times = time.strftime("%H:%M:%S", time.gmtime())
        self.terminalAppendLine('[' + times + '] ' + 'Flash Go!' + '\n')
        self.shellThread.setCmd(cmd)
        self.shellThread.start()
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

    def eeprom_radioButtonSet(self, execType):
        if execType is 'w':
            self.widget.radioButton_eepromWrite.setChecked(True)
            self.widget.radioButton_eepromRead.setChecked(False)
            self.widget.radioButton_eepromVerify.setChecked(False)
        elif execType is 'r':
            self.widget.radioButton_eepromWrite.setChecked(False)
            self.widget.radioButton_eepromRead.setChecked(True)
            self.widget.radioButton_eepromVerify.setChecked(False)
        elif execType is 'v':
            self.widget.radioButton_eepromWrite.setChecked(False)
            self.widget.radioButton_eepromRead.setChecked(False)
            self.widget.radioButton_eepromVerify.setChecked(True)
        else:
            self.widget.radioButton_eepromWrite.setChecked(False)
            self.widget.radioButton_eepromRead.setChecked(False)
            self.widget.radioButton_eepromVerify.setChecked(False)

    def eeprom_execute(self):
        cmd = self.getBasicParameter()
        tmp = self.eeprom_radioButtonCheck()
        if tmp is not '':
            cmd += ' -U eeprom:' + tmp + ':' + self.widget.lineEdit_flash.text() + '":i'
        times = time.strftime("%H:%M:%S", time.gmtime())
        self.terminalAppendLine('[' + times + '] ' + 'EEPROM Go!' + '\n')
        self.shellThread.setCmd(cmd)
        self.shellThread.start()
    # ---- Eeprom Group end ----------------------------------------------------

    # ---- MCU Group start -----------------------------------------------------
    # detect MCU is correct or wrong
    def mcu_detect(self):
        cmd = self.getBasicParameter()
        self.shellThread.setCmd(cmd)
        self.shellThread.start()
    # ---- MCU Group end -------------------------------------------------------

# ---- class radioButtonClick End ----------------------------------------------
