import logging
import mpolicy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

#  Socket to talk to server
print("Connecting to hello world server...")

mp = mpolicy.MutexPolicy()

print(f"Currently open mutexes: {mp.lst()}")

mtx = mp.open("mutex1")
mtx2 = mp.open("mutex2")

mtx2.lock()
print("in mutex2")


mtx.lock()
print("In mutex")

print(f"Currently open mutexes: {mp.lst()}")

mtx.unlock()
mtx2.unlock()

print(f"Currently open mutexes: {mp.lst()}")

mtx.lock()
print("In mutex")
mtx.unlock()

mtx.lock()
print("In mutex")
mtx.unlock()

mtx.close()
mtx2.close()
print(f"Currently open mutexes: {mp.lst()}")
