import os
import zmq


class MutexPolicy:
    def __init__(self, address="127.0.0.1"):
        "Connects to the mutex policy daemon running at the specified address"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{address}:5555")

    def open(self, mutex_name):
        """Opens a mutex identified by an unique name.

        The caller must eventually call `close()` on the returned mutex to
        free up the resources used for it by the daemon.
        """

        msg = f"{os.getpid()} O {mutex_name}"
        self.socket.send_string(msg)

        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

        return Mutex(mutex_name, self.socket)

    def lst(self):
        """Returns a list representing all the mutexes
        currently open in the system."""
        self.socket.send_string("list")

        return self.socket.recv_string()


class Mutex:
    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

    def close(self):
        "Close the given mutex "

        msg = f"{os.getpid()} C {self.name}"
        self.socket.send_string(msg)

        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

    def lock(self):
        "Lock the mutex or blocks until we are able to lock it."

        msg = f"{os.getpid()} L {self.name}"

        self.socket.send_string(msg)
        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

    def unlock(self):
        "Unlocks the mutex and allows the next process to take it."

        msg = f"{os.getpid()} U {self.name}"

        self.socket.send_string(msg)
        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")
