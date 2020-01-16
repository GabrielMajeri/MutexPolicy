
import os
import mpolicy
from time import sleep

fisier = "nume_fisier2.txt"

mp = mpolicy.MutexPolicy()

mtx = mp.open("mutex1")


def process1():
    mtx.lock()
    f = open(fisier, 'r')
    val = f.readline()
    val = int(val)
    print(type(val))
    print(val)
    print(f"Value read from file: {val}")
    sleep(2)
    val += 1
    print(f"Value wrote to file: {val}")
    g = open(fisier, 'w')
    print(val, file=g)
    f.close()
    g.close()
    mtx.unlock()


process1()

mtx.close()