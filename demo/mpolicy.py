import os
import zmq
import logging

class MutexPolicy:
    def __init__(self, address="127.0.0.1"):
        "Connects to the mutex policy daemon running at the specified address"
        logging.info("Connecting to mutex policy daemon...")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{address}:5555")
        logging.info("Connected to mutex policy daemon")

    def open(self, mutex_name):
        """Opens a mutex identified by an unique name.
        The caller must eventually call `close()` on the returned mutex to
        free up the resources used for it by the daemon.
        """
        logging.info("Opening mutex...")

        msg = f"{os.getpid()} O {mutex_name}"
        self.socket.send_string(msg)

        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")

        logging.info("Mutex successfully opened")
        return Mutex(mutex_name, self.socket)

    def lst(self):
        """Returns a list representing all the mutexes
        currently open in the system."""
        logging.info("Returning mutex list...")
        self.socket.send_string("list")
        logging.info("Returned mutex list successfully")
        return self.socket.recv_string()

class Mutex:
    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

    def close(self):
        "Close the given mutex "
        logging.info("Closing mutex...")

        msg = f"{os.getpid()} C {self.name}"
        self.socket.send_string(msg)

        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")
        logging.info("Mutex successfully closed")

    def lock(self):
        "Lock the mutex or blocks until we are able to lock it."
        logging.info("Locking mutex...")

        msg = f"{os.getpid()} L {self.name}"

        self.socket.send_string(msg)
        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")
        logging.info("Mutex successfully locked")

    def unlock(self):
        "Unlocks the mutex and allows the next process to take it."
        logging.info("Unlocking mutex...")

        msg = f"{os.getpid()} U {self.name}"

        self.socket.send_string(msg)
        msg_rec = self.socket.recv_string()

        if msg_rec != "Ok":
            raise Exception(f"Error: {msg_rec}")
        logging.info("Mutex successfully unlocked")