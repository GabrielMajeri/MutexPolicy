from collections import defaultdict

import zmq

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
	print("Hello from daemon")

	ctx = zmq.Context()

	print("Daemon bound to IPC")

	socket = ctx.socket(zmq.ROUTER)
	socket.bind("tcp://*:5555")

	while True:
		address_client, empty, msg = socket.recv_multipart() #nume client, empty, mesaj

		msg = msg.decode('UTF-8')

		pid, command, mutex_name = msg.split()

		#mutex_name = msg[1:]

		print("Toni incearca sa se conecteze pe laptopul meu")
		print(address_client, msg)

		my_mutex = mutexes[mutex_name]

		print(command)

		if command == 'O': #Open
			if mutex_name in pid_to_mutex[pid]:#address_client in my_mutex.process:
				send_message(socket, address_client, b'Nu este Ok') #este in lista deja mutexul
			else:
				pid_to_mutex[pid].append(mutex_name)
				my_mutex.process.add(pid)
				send_message(socket, address_client, b'Ok')

		elif command == 'C':	#Close
			if mutex_name in pid_to_mutex[pid]:#address_client in my_mutex.process:
				my_mutex.process.remove(pid)
				del pid_to_mutex[pid]
				send_message(socket, address_client, b'Ok') #s-a sters
				if not my_mutex.process:
					del mutexes[mutex_name]

			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif command == 'L':	#Lock
			print(pid_to_mutex[pid])
			if mutex_name in pid_to_mutex[pid]:#address_client in my_mutex.process:
				if my_mutex.owner_pid == None:
					my_mutex.owner_pid = pid
					send_message(socket, address_client, b'Ok') # Ai dat lock
				else:
					my_mutex.queue.append((pid, address_client))
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif command == 'U':	#Unlock
			if mutex_name in pid_to_mutex[pid]:#address_client in mutexes[mutex_name].process:
				print(my_mutex.owner_pid, pid)
				if my_mutex.owner_pid == pid:
					send_message(socket, address_client, b'Ok') # Ai dat lock

					if my_mutex.queue:
						next_guy, address_client = my_mutex.queue.pop(0)
						my_mutex.owner_pid = next_guy
						send_message(socket, address_client, b'Ok') # Ai dat lock
					else:
						my_mutex.owner_pid = None
				else:
					send_message(socket, address_client, b'Nume client != nume actual')
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		else:
			print("Comanda necunoscuta:", msg)
			send_message(socket, address_client, b'Nu ai ales bine. Mai incearca')


if __name__ == '__main__':
	main()
