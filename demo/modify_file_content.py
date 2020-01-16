from time import sleep
import mpolicy

fisier = "nume_fisier2.txt"

mp = mpolicy.MutexPolicy()

mtx = mp.open("mutex1")


def increment_input_from_file():
    mtx.lock()
    with open(fisier, 'r') as f:
        val = f.readline()
    val = int(val)
    print(type(val))
    print(val)
    print(f"Value read from file: {val}")
    sleep(2)
    val += 1
    print(f"Value wrote to file: {val}")
    with open(fisier, 'w') as f:
        print(val, file=f)
    mtx.unlock()


increment_input_from_file()

mtx.close()
