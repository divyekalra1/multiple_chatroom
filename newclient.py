from email import header
import time,sys,socket,select
import errno
header_len = 15


client_socket = socket.socket()
client_name = socket.gethostname()
client_ip = socket.gethostbyname(client_name)
port = 1234

name = input("Username : ")

# connection_ip = input("Enter Chatroom IP : ")

client_socket.connect((client_ip,port))
client_socket.setblocking(False)
client_username = name.encode()
client_username_header = (f"{len(client_username):<{header_len}}").encode()
client_socket.send(client_username_header + client_username)

while True:
    message = input(f"{name} > ")
    message = message.encode()
    message_header = f"{len(message):<{header_len}}".encode()
    if len(message_header):
        client_socket.send(message_header + message)
        print("meow")

    try:
        while True :
            username_header = (client_socket.recv(header_len))
            username = client_socket.recv(int(username_header).decode().strip()).decode()
            message_header = client_socket.recv(header_len)
            message = client_socket.recv(int(message_header).decode().strip()).decode()
            print(f"{username} > {message}")
            print("2")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue
    except Exception as e:
        print('Reading error: '.format(str(e)))
        print("3")
        sys.exit()
