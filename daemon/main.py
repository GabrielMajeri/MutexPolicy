from collections import defaultdict

import zmq

class Mutex:
	def __init__(self):
		self.actual_name = None
		self.process = set()
		self.queue = []

mutexes = defaultdict(Mutex)

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

		mutex_name = msg[1:]

		print("Toni incearca sa se conecteze pe laptopul meu")
		print(address_client, msg)

		my_mutex = mutexes[mutex_name]

		print(msg[0])

		if msg[0] == 'O': #Open
			if address_client in my_mutex.process:
				send_message(socket, address_client, b'Nu este Ok')
			else:
				my_mutex.process.add(address_client)
				send_message(socket, address_client, b'Ok')

		elif msg[0] == 'C':	#Close
			if address_client in my_mutex.process:
				my_mutex.process.remove(address_client)
				send_message(socket, address_client, b'S-a sters')
				if not my_mutex.process:
					del mutexes[mutex_name]

			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif msg[0] == 'L':	#Lock
			if address_client in my_mutex.process:
				if my_mutex.actual_name == None:
					send_message(socket, address_client, b'Ok') # Ai dat lock
				else:
					my_mutex.queue.append(address_client)
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif msg[0] == 'U':	#Unlock
			if address_client in mutexes[mutex_name].process:
				if my_mutex.actual_name == address_client:
					send_message(socket, address_client, b'Ok') # Ai dat lock

					if my_mutex.queue:
						next_guy = my_mutex.queue.pop(0)
						my_mutex.actual_name = next_guy
						send_message(socket, address_client, b'Ok') # Ai dat lock
					else:
						my_mutex.actual_name = None
				else:
					send_message(socket, address_client, b'Nume client != nume actual')
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		else:
			print("Comanda necunoscuta:", msg)
			send_message(socket, address_client, b'Nu ai ales bine. Mai incearca')


if __name__ == '__main__':
	main()
