import zmq

from collections import defaultdict

class Mutex:
	def __init__(self):
		self.nume_actual = None
		self.procese = set()
		self.coada = []

mutecsii = defaultdict(Mutex)

def send_message(socket, adresa_client, message):
	socket.send_multipart([
		adresa_client,
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
		adresa_client, empty, msg = socket.recv_multipart() #nume client, empty, mesaj

		nume_mutex = msg[1:]

		if msg[0] == 'O': #Open
			if adresa_client in mutecsii[nume_mutex].procese:
				send_message(socket, adresa_client, "b'Nu este Ok'")
			else:
				mutecsii[mutex].procese.append(nume_client)
				send_message(socket, adresa_client, "b'Ok'")

		if msg[0] == 'C':	#Close
			if adresa_client in mutecsii[nume_mutex].procese:
				mutecsii.procese.delete(adresa_client)
				send_message(socket, adresa_client, "b'S-a sters'")
			else:
				send_message(socket, adresa_client, "b'Nu exista adresa specificata'")

		if msg[0] == 'L':	#Lock
			if adresa_client in mutecsii[nume_mutex].procese:
				if mutecsii[nume_mutex].nume_actual == None:
					send_message(socket, adresa_client, "b'Ai dat Lock'")
				else:
					mutecsii[nume_mutex].coada.append(nume_client)
			else:
				send_message(socket, adresa_client, "b'Nu exista adresa specificata'")

		if msg[0] == 'U':	#Unlock
			if adresa_client in mutecsii[nume_mutex].procese:
				if mutecsii[nume_mutex].nume_actual == nume_client:
					send_message(socket, adresa_client, "b'Ai dat Unlock'")
					next_guy = mutecsii[nume_mutex].coada.pop(0)
					mutecsii[nume_mutex].nume_actual = next_guy
					send_message(socket, adresa_client, "b'Ai dat Lock'")
				else:
					send_message(socket, adresa_client, "b'Nume client != nume actual'")
			else:
				send_message(socket, adresa_client, "b'Nu exista adresa specificata'")


if __name__ == '__main__':
	main()