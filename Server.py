import socket
import threading

HEADER = 1024
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
QUIT = 'QUIT'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(ADDR)
	
clients = []			#create a list of clients

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            client.send(msg)

def handle_client(c, addr):
	print(f"New connection: {addr} connected")
	connected = True
	while connected:
		msg_length = c.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = c.recv(msg_length).decode(FORMAT)
			
			if msg == QUIT:
				c.send("Disconnecting from server...\n".encode(FORMAT))		#if I don't have this line then sometime the server won't disconnect
				c.send("Goodbye".encode(FORMAT))
				print(f"{addr} disconnected")
				clients.remove(c)			#remove client from list	
				connected = False
			else:
				print(f"{addr}: {msg}")
				c.send("Message received from server\n".encode(FORMAT))
			for client in clients:
				if client != c and msg != QUIT:						#dont send QUIT and dont let sender recieve their own message
					client.send(f"{addr}: {msg}".encode(FORMAT))
					client.send("\n".encode(FORMAT))				#add a new line otherwise all messages are linked together
	#print("the client has exited the loop from the server side")	#this was just for testing, ignore it
	c.close

def start():
	s.listen()
	print(f"Server is listening on {SERVER}")
	while True:
		c, addr = s.accept()
		clients.append(c)
		thread = threading.Thread(target = handle_client, args=(c, addr))
		thread.start()
		print(f"Active connections: {threading.active_count() - 1}")

print("Server is starting up...")
start()