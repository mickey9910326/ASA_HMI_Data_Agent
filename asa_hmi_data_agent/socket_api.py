from PyQt5.QtCore import QThread
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from asa_hmi_data_agent.cli_tools.commands import *

import zmq
import json

STATE_REC = 1
STATE_REP = 2

class AdtSocketReceiver(QThread):
    signalTermOpen  = pyqtSignal(int, str, int)
    signalTermClose = pyqtSignal(int)
    signalTermClear = pyqtSignal(int)
    signalLoaderStart = pyqtSignal(str, str)
    signalLoaderState = pyqtSignal()

    def __init__(self, context, socket):
        QThread.__init__(self)
        self.context = context
        self.socket = socket
        self.status = STATE_REC

    def run(self):
        i = 0
        while self.context.closed is False:
            if self.status is STATE_REP:
                continue
            elif self.status is STATE_REC:
                cmd = json.loads(self.socket.recv_json())
                if cmd['cmd'] == AdtCmd.LOADER:
                    self.doCmdLoader(cmd)
                elif cmd['cmd'] == AdtCmd.TERM:
                    self.doCmdTerm(cmd)
                self.status = STATE_REP

    def doCmdLoader(self, cmd):
        if cmd['subcmd'] == AdtSubCmdLoader.START:
            self.signalLoaderStart.emit(cmd['port'], cmd['hexfile'])
        elif cmd['subcmd'] == AdtSubCmdLoader.STATE:
            self.signalLoaderState.emit()

    def doCmdTerm(self, cmd):
        if cmd['subcmd'] == AdtSubCmdTerm.OPEN:
            self.signalTermOpen.emit(cmd['id'], cmd['port'], cmd['baudrate'])
        elif cmd['subcmd'] == AdtSubCmdTerm.CLOSE:
            self.signalTermClose.emit(cmd['id'])
        elif cmd['subcmd'] == AdtSubCmdTerm.CLEAR:
            self.signalTermClear.emit(cmd['id'])

class AdtSocketHandler(QObject):
    signalTermOpen  = pyqtSignal(int, str, int)
    signalTermClose = pyqtSignal(int)
    signalTermClear = pyqtSignal(int)
    signalLoaderStart = pyqtSignal(str, str)
    signalLoaderState = pyqtSignal()

    def __init__(self):
        super(AdtSocketHandler, self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind('tcp://*:8787')

        self.receiver = AdtSocketReceiver(self.context, self.socket)
        self.receiver.start()

        self.receiver.signalTermOpen[int, str, int].connect(self.signalTermOpen.emit)
        self.receiver.signalTermClose[int].connect(self.signalTermClose.emit)
        self.receiver.signalTermClear[int].connect(self.signalTermClear.emit)
        self.receiver.signalLoaderStart[str, str].connect(self.signalLoaderStart.emit)
        self.receiver.signalLoaderState.connect(self.signalLoaderState.emit)

    def sendRes(self, res):
        self.socket.send_json(json.dumps(res))
        self.receiver.status = STATE_REC
