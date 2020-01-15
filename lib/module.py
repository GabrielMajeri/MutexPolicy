class MutexPolicy:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = ctx.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:5555")

    def open(self, mutex_name):
        msg = "O" + mutex_name
        msg.encode('UTF-8')
        self.socket.send(msg)

        msg_rec = self.socket.recv()
        msg_rec = msg_rec.decode("UTF-8")
        if msg_rec == "Ok":
            return
        else:
            raise Exception("Error: opening a mutex")

        mtx = Mutex(mutex_nume, self.socket)
        return mtx


class Mutex:
    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

    def close(self):
        msg = "C" + self.name
        msg.encode('UTF-8')
        self.socket.send(msg)

        msg_rec = self.socket.recv()
        msg_rec = msg_rec.decode("UTF-8")
        if msg_rec == "Ok":
            return
        else:
            raise Exception("Error: closing a mutex")

        mtx = Mutex(mutex_nume, self.socket)
        return mtx

    def lock(self):
        msg = "L" + self.mutex_name
        msg.encode('UTF-8')
        self.socket.send(msg)
        msg_rec = self.socket.recv()
        msg_rec = msg_rec.decode("UTF-8")
        if msg_rec == "Ok":
            return
        else:
            raise Exception("Error: locking a mutex")

    def unlock(self):
        msg = "U" + self.mutex_name
        msg.encode('UTF-8')
        self.socket.send(msg)
        msg_rec = self.socket.recv()
        msg_rec = msg_rec.decode("UTF-8")
        if msg_rec == "Ok":
            return
        else:
            raise Exception("Error: unlocking a mutex")