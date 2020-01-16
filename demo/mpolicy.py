import os
import zmq

class MutexPolicy:
    def __init__(self, address="127.0.0.1"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{address}:5555")

    def open(self, mutex_name):
        msg = f"{os.getpid()} O {mutex_name}"
        self.socket.send_string(msg)

        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

        return Mutex(mutex_name, self.socket)

class Mutex:
    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

    def close(self):
        msg = f"{os.getpid()} C {self.name}"
        self.socket.send_string(msg)

        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

    def lock(self):
        msg = f"{os.getpid()} L {self.name}"

        self.socket.send_string(msg)
        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

    def unlock(self):
        msg = f"{os.getpid()} U {self.name}"

        self.socket.send_string(msg)
        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")
