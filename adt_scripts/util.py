import enum
import zmq
import json

class AdtCmd(enum.IntEnum):
    TERM = 1
    LOADER = 2
    STK500 = 3

class AdtSubCmdLoader(enum.IntEnum):
    START = 1
    STATE = 2

class AdtSubCmdTerm(enum.IntEnum):
    OPEN  = 1
    CLOSE = 2
    CLEAR = 3

class AdtSocketHandler(object):
    def __init__(self):
        super(AdtSocketHandler, self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)

        self.socket.connect("tcp://127.0.0.1:8787")

    def close(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.poll.unregister(self.socket)

    def send_cmd(self, cmd):
        self.socket.send_json(json.dumps(cmd))
        socks = dict(self.poll.poll(3000))
        if socks.get(self.socket) == zmq.POLLIN:
            res = self.socket.recv_json()
            return json.loads(res)
        else:
            self.close()
            return None

#
# stanard res
# res = {
#     'err' : bool
#     'msg' : str
# }
