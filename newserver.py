import time,sys,socket,select

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)

port = 1234

server_socket.bind((server_ip,port))
print("Binding done successfully.")

server_username = input("Enter Server Name : ")

print("Server IP is :", server_ip)

server_socket.listen()
print("Listening for any new connections or messages from users")

socket_list = [server_socket]
clients = {}

header_len = 15

def receivemessage(client_socket):
    try:
        info_header = client_socket.recv(header_len)
        if not len(info_header):
            print("yo1")
            return False
        return {"header" : info_header, "info": client_socket.recv(int(info_header.decode().strip()))}
    except:
        print("yo2")
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
            print(f"1Message received from {user['info'].decode()}")
        else:
            bundle = receivemessage(s)
            if bundle is False:
                print(f"No message received from {clients[s]['info'].decode()}")
                print(f"Terminating connection with {clients[s]['info'].decode()}")
                socket_list.remove(s)
                del clients[s]
            name = clients[s]
            msg = bundle
            print(f"2Message received from {name['info'].decode()}")
            for client_socket in clients:
                if client_socket!=s:
                    client_socket.send(name['header'] + name['info'] + msg['header'] + msg['info'])
    for s in exception_sockets:
            socket_list.remove(s)
            del clients[s]
