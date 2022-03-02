from http import client
from socket import *
from User import *

def print_all_users():
    print ("Current users: ")
    for users in user_database:
        users.printDetails()
    print()

server_ip = '127.0.0.1'
server_port = 12000
serverSocket=socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((server_ip, server_port))

user_database = []
connections_counter = 0

print("Server Running")
while True:
    message,client_address = serverSocket.recvfrom(2048)

    x = User(str(client_address[0]), str(client_address[1]), message)
    user_database.append(x)

    user_database[connections_counter].printDetails()
    connections_counter += 1
    
    print_all_users()




