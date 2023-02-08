from email import header
import time,sys,socket,select
import errno


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
port = 407

client_name = input("Name : ")
# connection_ip = input("Enter Chatroom IP : ") # To be used if the IP of the server is different from that of the client
HEADER_LEN = 90

client_socket.connect((server_ip,port))
client_socket.setblocking(False)
client_username = client_name.encode()
client_username_header = (f"{len(client_username):<{HEADER_LEN}}").encode()
client_socket.send(client_username_header + client_username)

while True:

    message = input(f"{client_name} > ")   
    if len(message):
        message = message.encode()
        message_header = f"{len(message):<{HEADER_LEN}}".encode()
        client_socket.send(message_header + message)

    try:
        while True :
            username_header = (client_socket.recv(HEADER_LEN))
            username = client_socket.recv(int(username_header.decode().strip())).decode()
            message_header = client_socket.recv(HEADER_LEN)
            message = client_socket.recv(int(message_header.decode().strip())).decode()
            print(f"{username} > {message}")
            print("2")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
