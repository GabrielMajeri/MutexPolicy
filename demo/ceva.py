
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import mpolicy

#  Socket to talk to server
print("Connecting to hello world server…")

mp = mpolicy.MutexPolicy()

#  Do 10 requests, waiting each time for a response
mtx = mp.open("mutex1")

mtx.lock()
print("In mutex")
mtx.unlock()

mtx.lock()
print("In mutex")
mtx.unlock()

mtx.close()
