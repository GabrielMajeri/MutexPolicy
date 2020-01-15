import zmq

from collections import defaultdict

class Mutex:
	def __init__(self):
		self.actual_name = None
		self.process = set()
		self.coada = []

mutecsii = defaultdict(Mutex)

def send_message(socket, addres_client, message):
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

		name_mutex = msg[1:]

		my_mutex = mutecsii[name_mutex]

		if msg[0] == 'O': #Open
			if address_client in my_mutex.procese:
				send_message(socket, address_client, b'Nu este Ok')
			else:
				my_mutex.procese.append(nume_client)
				send_message(socket, address_client, b'Ok')

		elif msg[0] == 'C':	#Close
			if address_client in my_mutex.process:
				mutecsii.process.delete(address_client)
				send_message(socket, address_client, b'S-a sters')
				if not my_mutex.process:
					del mutecsii[name_mutex]

			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif msg[0] == 'L':	#Lock
			if address_client in my_mutex.procese:
				if my_mutex.actual_name == None:
					send_message(socket, address_client, b'Ai dat Lock')
				else:
					my_mutex.coada.append(nume_client)
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		elif msg[0] == 'U':	#Unlock
			if addres_client in mutecsii[nume_mutex].procese:
				if my_mutex.actual_name == nume_client:
					send_message(socket, address_client, b'Ai dat Unlock')
					next_guy = my_mutex.coada.pop(0)
					my_mutex.actual_name = next_guy
					send_message(socket, address_client, b'Ai dat Lock')
				else:
					send_message(socket, address_client, b'Nume client != nume actual')
			else:
				send_message(socket, address_client, b'Nu exista adresa specificata')

		else:
			print("Ce vrei de la viata mea!!!?!!?")
			send_message(socket, address_client, b'Nu ai ales bine. Mai incearca')


if __name__ == '__main__':
	main()