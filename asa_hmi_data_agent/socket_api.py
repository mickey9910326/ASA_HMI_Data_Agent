from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import zmq
from adt_scripts.util import *
import json

class AdtSocketHandler(QThread):
    signalTermOpen  = pyqtSignal(int, str, int)
    signalTermClose = pyqtSignal(int)
    signalTermClear = pyqtSignal(int)

    """docstring for ADTSocketHandler."""
    def __init__(self):
        QThread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind('tcp://*:8787')

    def run(self):
        i = 0
        while self.context.closed is False:
            cmd = json.loads(self.socket.recv_json())
            if cmd['cmd'] == AdtCmd.LOADER:
                self.doCmdLoader(cmd)
            elif cmd['cmd'] == AdtCmd.TERM:
                self.doCmdTerm(cmd)

    def doCmdLoader(self, cmd):
        if cmd['subcmd'] == AdtSubCmdLoader.START:
            res = {
                'times' : 100
            }
            self.socket.send_json(json.dumps(res))
        elif cmd['subcmd'] == AdtSubCmdLoader.STATE:
            i = i+1
            res = {
                'times' : i
            }
            print(res)
            self.socket.send_json(json.dumps(res))

    def doCmdTerm(self, cmd):
        if cmd['subcmd'] == AdtSubCmdTerm.OPEN:
            self.signalTermOpen.emit(cmd['id'], cmd['port'], cmd['baudrate'])
            res = {
                'err' : False,
                'msg' : ''
            }
            self.socket.send_json(json.dumps(res))
        elif cmd['subcmd'] == AdtSubCmdTerm.CLOSE:
            self.signalTermClose.emit(cmd['id'])
            res = {
                'err' : False,
                'msg' : ''
            }
            self.socket.send_json(json.dumps(res))
        elif cmd['subcmd'] == AdtSubCmdTerm.CLEAR:
            self.signalTermClear.emit(cmd['id'])
            res = {
                'err' : False,
                'msg' : ''
            }
            self.socket.send_json(json.dumps(res))
