import sys
import select
import time
import socket

server_socket = socket.socket()
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
port = 8000

sockets_list = [server_socket]
clients = {}

server_socket.bind((server_ip,port))
print("Binding done successfully.")

server_socket.listen()

def receive_message(client_socket):
    try:
        message = (client_socket.recv(1024)).decode()
        if not len(message):
            return False
        else:
            return {"message" : message}


    except:
        return False


def add_new_client(client_socket):
    #add client to sockets list
    pass


while True: 
    # if and else to see if the sockets list is a new connection or just a message from a client
    print("Listening for any new connections or messages from users")

    read_sockets, _, _, = select.select(sockets_list, [], []) # Reading all sockets in sockets_list and checking if there's any message / new client wants to join   
    for x in read_sockets:
        if x==server_socket:
            newclient_socket, newclient_ip = server_socket.accept()
            newclient_username = input("Username : ")
            sockets_list.append(x)
            message = receive_message(newclient_socket)
            clients[newclient_ip] = {'username' : newclient_username}.update(message)
            newclient_socket.send(newclient_username.encode())


        else:
            message = receive_message(x)
            if not message:
                print("No message from user")
            else:
                print(f"{clients[newclient_ip]} > {message['data']}")
                for client in clients:
                    if clients[]!= 


                
                
