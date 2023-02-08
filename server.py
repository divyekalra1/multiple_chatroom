import time,sys,socket,select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
port = 407

server_socket.bind((server_ip,port))
print("Binding done successfully.")

server_username = input("Enter Server Name : ")
print("Server IP is :", server_ip)
server_socket.listen()
print("Listening for any new connections or messages from users")

socket_list = [server_socket]
clients = {}
HEADER_LEN = 90 # Constant defining the length of the headers

def receivemessage(client_socket):
    try:
        info_header = client_socket.recv(HEADER_LEN)
        if not len(info_header):
            return False
        return {'header' : info_header, 'info': client_socket.recv(int(info_header.decode().strip()))}
    except:
        return False

while True:

    read_sockets , _, exception_sockets, = select.select(socket_list,[],socket_list)
    for s in read_sockets:

        if s == server_socket:
            client_socket, client_ip = server_socket.accept()
            user = receivemessage(client_socket)
            if user is False:
                print("User Disconnected")
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user
            print(f"Connection received from {user['info'].decode()}")

        else:

            bundle = receivemessage(s)
            if bundle is False:
                print(f"No message received from {clients[s]['info'].decode()}")
                print(f"Terminating connection with {clients[s]['info'].decode()}")
                socket_list.remove(s)
                del clients[s]
                continue
            name = clients[s]
            print(f"Message received from {name['info'].decode()}")

            for client_socket in clients:
                if client_socket!=s:
                    client_socket.send(name['header'] + name['info'] + bundle['header'] + bundle['info'])

    for s in exception_sockets:
            socket_list.remove(s)
            del clients[s]
