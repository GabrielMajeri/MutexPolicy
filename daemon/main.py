import zmq

from collections import defaultdict

class Mutex:
	def __init__(self):
		self.actual_name = None
		self.process = set()
		self.coada = []

mutecsii = defaultdict(Mutex)

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

		name_mutex = msg[1:]

		print("Toni incearca sa se conecteze pe laptopul meu")
		print(address_client, msg)

		my_mutex = mutecsii[name_mutex]

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
					del mutecsii[name_mutex]

			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif msg[0] == 'L':	#Lock
			if address_client in my_mutex.process:
				if my_mutex.actual_name == None:
					send_message(socket, address_client, b'Ai dat Lock')
				else:
					my_mutex.coada.append(addres_client)
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif msg[0] == 'U':	#Unlock
			if address_client in mutecsii[name_mutex].process:
				if my_mutex.actual_name == address_client:
					send_message(socket, address_client, b'Ai dat Unlock')

					if my_mutex.coada:
						next_guy = my_mutex.coada.pop(0)
						my_mutex.actual_name = next_guy
						send_message(socket, address_client, b'Ai dat Lock')
					else:
						my_mutex.actual_name = None
				else:
					send_message(socket, address_client, b'Nume client != nume actual')
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		else:
			print("Ce vrei de la viata mea!!!?!!?")
			send_message(socket, address_client, b'Nu ai ales bine. Mai incearca')


if __name__ == '__main__':
	main()