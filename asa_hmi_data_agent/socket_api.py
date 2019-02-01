from PyQt5.QtCore import QThread
import zmq
from adt_scripts.util import *
import json

class AdtSocketHandler(QThread):
    """docstring for ADTSocketHandler."""
    def __init__(self):
        QThread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind('tcp://*:8787')

    def run(self):
        i = 0
        while self.context.closed is False:
            data = json.loads(self.socket.recv_json())
            if data['cmd'] == AdtCmd.LOADER:
                if data['subcmd'] == AdtSubCmdLoader.START:
                    res = {
                        'times' : 100
                    }
                    self.socket.send_json(json.dumps(res))
                elif data['subcmd'] == AdtSubCmdLoader.STATE:
                    i = i+1
                    res = {
                        'times' : i
                    }
                    print(res)
                    self.socket.send_json(json.dumps(res))
