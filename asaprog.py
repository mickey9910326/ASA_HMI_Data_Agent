from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from listport import serial_ports
import subprocess
import time

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

        self.p = subprocess.Popen(self.cmd.split(' ') , stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        while self.p.poll() is None:
            s = self.p.stderr.readline()
            print(s)
            if(s.decode("utf-8", "replace") is not ''):
                self.signalGetLine.emit(s.decode("utf-8", "replace"))
        times = time.strftime("%H:%M:%S", time.gmtime())
        self.signalGetLine.emit('\n' + '[' + times + '] ' + 'Complete!' + '\n')
        self.shellIsRunning = False

    def stop(self):
        if self.shellIsRunning or self.p.poll() is None:
            times = time.strftime("%H:%M:%S", time.gmtime())
            self.signalGetLine.emit('[' + times + '] ' + 'Stop!' + '\n')
            self.shellIsRunning = False
            self.p.kill()
        else:
            pass
        self.terminate()

# ---- class ShellThread End ---------------------------------------------------

class Asaprog(object):
    # ---- __init__ start ------------------------------------------------------
    def __init__(self, widget, mainWindow):
        self.widget = widget
        self.mainWindow = mainWindow

        # ---- Shell Thread Init start -----------------------------------------
        self.shellThread = ShellThread()
        self.shellThread.signalGetLine[str].connect(self.terminalInsertText)
        # ---- Shell Thread Init end -------------------------------------------

        # ---- Serial Group start ----------------------------------------------
        self.serial_updatePortlist()
        self.widget.pushButton_updatePortList.clicked.connect(self.serial_updatePortlist)
        # ---- Serial Group end ------------------------------------------------

        # ---- Select File Group start -----------------------------------------
        self.widget.pushButton_selectFile.clicked.connect(self.chooseProgFile)
        # ---- Select File Group end -------------------------------------------

        # ---- basic Tools Group start -----------------------------------------
        self.widget.pushButton_startProg.clicked.connect(self.startProg)
        self.widget.pushButton_stopProg.clicked.connect(self.stopProg)
        # ---- basic Tools Group end -------------------------------------------

        self.serial_updatePortlist()

        # TODO: complete this two btn function
        # self.widget.pushButton_settings.clicked.connect()
        # self.widget.pushButton_progStk500.clicked.connect()

    def terminalInsertText(self, s):
        self.widget.textBrowser_terminal.insertPlainText(s)

    # ---- Serial Group start --------------------------------------------------
    # Update port list in s_portComboBox
    def serial_updatePortlist(self):
        availablePorts = serial_ports()
        print('sys : Update port list in portComboBox, available port : ', end='')
        print(availablePorts)
        self.widget.comboBox_selectPort.clear()
        for port in availablePorts:
            self.widget.comboBox_selectPort.addItem(port)
    # ---- Serial Group end ----------------------------------------------------

    # ---- Choose File Group start ---------------------------------------------
    def chooseProgFile(self):
        name, _ = QFileDialog.getOpenFileName(self.mainWindow, 'Open File','', 'All Files (*);;Hex Files (*.hex)' ,initialFilter='Hex Files (*.hex)')
        if name is not '':
            self.widget.lineEdit_selectFile.setText(name)
    # ---- Choose File Group end -----------------------------------------------

    # ---- Basic Tools Group start ---------------------------------------------
    def startProg(self):
        cmd = 'tools\\cmd_ASA_loader'
        cmd += ' -p ' + self.widget.comboBox_selectPort.currentText().split('COM')[1]
        cmd += ' -h ' + self.widget.lineEdit_selectFile.text()
        self.shellThread.setCmd(cmd)
        self.shellThread.start()

    def stopProg(self):
        self.shellThread.stop()
    # ---- Basic Tools Group end -----------------------------------------------

    # ---- Special Tools Group start -------------------------------------------

    # ---- Special Tools Group end ---------------------------------------------
