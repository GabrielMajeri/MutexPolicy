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

	logging.basicConfig(filename='../example.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

	#logging.debug('This message should go to the log file')
	#logging.info('So should this')
	#logging.warning('And this, too')

	logging.info("Hello from daemon")

	ctx = zmq.Context()

	logging.info("Daemon bound to IPC")

	socket = ctx.socket(zmq.ROUTER)
	socket.bind("tcp://*:5555")

	while True:
		address_client, empty, msg = socket.recv_multipart() #nume client, empty, mesaj

		msg = msg.decode('UTF-8')

		msg_split = msg.split()

		if len(msg_split) == 1 and msg == "list":
			logging.info("A fost afisata lista cu piduri!")

			send_message(socket, address_client, str(pid_to_mutex).encode("UTF-8"))

			continue

		pid, command, mutex_name = msg_split

		logging.info("Pid-ul %s cu comanda %s si mutex nameul %s", pid, command, mutex_name)

		my_mutex = mutexes[mutex_name]

		if command == 'O': #Open
			if mutex_name in pid_to_mutex[pid]:
				logging.warning("Mutexul %s este deja in lista", mutex_name)

				send_message(socket, address_client, b'Nu este Ok') #este in lista deja mutexul
			else:
				logging.info("Pid-ul %s a deschis mutexul %s", pid, mutex_name)

				pid_to_mutex[pid].append(mutex_name)
				my_mutex.process.add(pid)

				send_message(socket, address_client, b'Ok')

		elif command == 'C':	#Close
			if mutex_name in pid_to_mutex[pid]:

				logging.info("S-a sters mutexul %s", mutex_name)

				my_mutex.process.remove(pid)
				del pid_to_mutex[pid]

				send_message(socket, address_client, b'Ok') #s-a sters

				if not my_mutex.process:
					del mutexes[mutex_name]

			else:
				logging.error("Mutexul %s nu exista!", mutex_name)

				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif command == 'L':	#Lock
			if mutex_name in pid_to_mutex[pid]:
				if my_mutex.owner_pid == None:
					my_mutex.owner_pid = pid

					logging.info("Pid-ul %s a dat lock la mutexul %s", pid, mutex_name)

					send_message(socket, address_client, b'Ok') # Ai dat lock
				elif my_mutex.owner_pid == pid:
					logging.warning("Pid-ul %s deja a dat lock!", pid)

					send_message(socket, address_client, b'Ai dat lock de doua ori!')
				else:
					logging.info("Pid-ul %s a fost adaugat in coada", pid)

					my_mutex.queue.append((pid, address_client))
			else:
				logging.error("Mutexul %s nu exista!", mutex_name)

				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif command == 'U':	#Unlock
			if mutex_name in pid_to_mutex[pid]:
				if my_mutex.owner_pid == pid:
					logging.info("Pid-ul %s a dat unlock", pid)

					send_message(socket, address_client, b'Ok') # Ai dat lock

					if my_mutex.queue:
						next_guy, address_client = my_mutex.queue.pop(0)
						my_mutex.owner_pid = next_guy

						logging.info("Pid-ul %s a luat lock", owner_pid)

						send_message(socket, address_client, b'Ok') # Ai dat lock
					else:
						my_mutex.owner_pid = None
				else:
					logging.warning("Owner_pid %s != actual pid %s", my_mutex.owner_pid, pid)

					send_message(socket, address_client, b'Nume client != nume actual')
			else:
				logging.warning("Mutexul %s nu exista!", mutex_name)

				send_message(socket, address_client, b'Nu exista adresa specificata')

		else:
			print("Comanda necunoscuta:", msg)
			logging.warning("Nu ai ales nici o optiune buna. Incearca O/C/L/U")

			send_message(socket, address_client, b'Nu ai ales bine. Mai incearca')


if __name__ == '__main__':
	main()
