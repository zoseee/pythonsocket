import socket
import threading


HEADER = 1024
PORT = 5051
FORMAT = 'utf-8'
QUIT = "QUIT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

valid = input("Type CONNECT to connect to the server\n")
if valid == 'CONNECT':
	connected = True
	client.connect(ADDR)
else:
	connected = False
	print("Connection not established\nTry again")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
def receive(): # seperate function for recieving so it does not wait for input to dispaly recieved msg
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT).strip()
            print(message)
        except:
            # an error occurred, assume server closed the connection
            print("Lost connection to server")
            client.close()
            break
    
receive_thread = threading.Thread(target=receive)
receive_thread.start()
    
while connected:
	answer = input("Enter SEND to send a message or QUIT to disconnect\n")
	if answer == 'SEND':
		msg = input("Enter message:\n")
		send(msg)
	elif answer == 'QUIT':
		send(QUIT)
		connected = False
		#print("I have set connected to false")		#ignore this
		#break										#don't need this anymore
	else:
		print("Command not recognized\nTry Again\n")
#print("I have exited the while loop")
client.close