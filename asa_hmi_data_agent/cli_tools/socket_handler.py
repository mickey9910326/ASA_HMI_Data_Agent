import zmq
import json

class SocketHandler(object):
    def __init__(self):
        super(SocketHandler, self).__init__()
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
