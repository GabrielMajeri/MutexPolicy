from collections import defaultdict

import zmq
import logging

class Mutex:
	def __init__(self):
		self.owner_pid = None
		self.process = set()
		self.queue = []

mutexes = defaultdict(Mutex)

pid_to_mutex = defaultdict(list)

def send_message(socket, address_client, message):
	socket.send_multipart([
		address_client,
		b'',
		message
	])

def main():

	logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)

	logging.info("Hello from daemon")

	ctx = zmq.Context()

	logging.info("Daemon bound to IPC")

	socket = ctx.socket(zmq.ROUTER)
	socket.bind("tcp://*:5555")

	while True:
		address_client, empty, msg = socket.recv_multipart() # Client name, empty string, message

		msg = msg.decode('UTF-8')

		msg_split = msg.split()

		if len(msg_split) == 1 and msg == "list":
			logging.info("Returning per-PID mutex list")

			send_message(socket, address_client, str(pid_to_mutex).encode("UTF-8"))

			continue

		pid, command, mutex_name = msg_split

		logging.info("PID %s - Command %s - Mutex %s", pid, command, mutex_name)

		my_mutex = mutexes[mutex_name]

		if command == 'O': #Open
			if mutex_name in pid_to_mutex[pid]:
				logging.warning("Mutex %s is already opened by process", mutex_name)

				send_message(socket, address_client, b'mutex is already opened') #este in lista deja mutexul
			else:
				logging.info("Process %s opened mutex %s", pid, mutex_name)

				pid_to_mutex[pid].append(mutex_name)
				my_mutex.process.add(pid)

				send_message(socket, address_client, b'Ok')

		elif command == 'C':	#Close
			if mutex_name in pid_to_mutex[pid]:

				logging.info("Closing mutex %s", mutex_name)

				my_mutex.process.remove(pid)
				pid_to_mutex[pid].remove(mutex_name)
				if not pid_to_mutex[pid]:
					del pid_to_mutex[pid]

				send_message(socket, address_client, b'Ok') #s-a sters

				if not my_mutex.process:
					logging.info("Releasing memory for mutex %s", mutex_name)
					del mutexes[mutex_name]

			else:
				logging.error("Mutex %s does not exist", mutex_name)

				send_message(socket, address_client, b'Mutex does not exist')

		elif command == 'L':	#Lock
			if mutex_name in pid_to_mutex[pid]:
				if my_mutex.owner_pid == None:
					my_mutex.owner_pid = pid

					logging.info("Process %s locked mutex %s", pid, mutex_name)

					send_message(socket, address_client, b'Ok') # Ai dat lock
				elif my_mutex.owner_pid == pid:
					logging.warning("Process %s already locked mutex %s!", pid, mutex_name)

					send_message(socket, address_client, b'Cannot lock mutex twice')
				else:
					logging.info("Process %s added to waiting queue", pid)

					my_mutex.queue.append((pid, address_client))
			else:
				logging.error("Mutex %s does not exist", mutex_name)

				send_message(socket, address_client, b'Mutex does not exist')

		elif command == 'U':	#Unlock
			if mutex_name in pid_to_mutex[pid]:
				if my_mutex.owner_pid == pid:
					logging.info("Process %s unlocked mutex %s", pid, mutex_name)

					send_message(socket, address_client, b'Ok') # A dat unlock

					if my_mutex.queue:
						next_guy, address_client = my_mutex.queue.pop(0)
						my_mutex.owner_pid = next_guy

						logging.info("Process %s locked mutex %s", my_mutex.owner_pid, mutex_name)

						send_message(socket, address_client, b'Ok') # A dat lock
					else:
						my_mutex.owner_pid = None
				else:
					logging.warning("Process %s tried to unlock mutex, already locked by process %s", pid, my_mutex.owner_pid)

					send_message(socket, address_client, b'Cannot unlock mutex if not locked')
			else:
				logging.warning("Mutex %s does not exist!", mutex_name)

				send_message(socket, address_client, b'Inexistent mutex')

		else:
			logging.warning("Unknown command: %s", msg)

			send_message(socket, address_client, b'Unknown command')


if __name__ == '__main__':
	main()
