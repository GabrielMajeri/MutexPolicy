
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

print(zmq.zmq_version())

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.11.192.134:5555")

#  Do 10 requests, waiting each time for a response
print("Sending request.")
socket.send(b"Omutex1")
print("Sent request.")
#  Get the reply.

print("Waiting reply")
message = socket.recv()
print("Received reply %", message)