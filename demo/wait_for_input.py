
import mpolicy

mp = mpolicy.MutexPolicy()

mtx = mp.open("mutex10")

print("starting program...")

mtx.lock()
input("press enter: ")
mtx.unlock()

mtx.close()