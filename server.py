from http import client
from socket import *
from User import *

server_ip = '127.0.0.1'
server_port = 12000
serverSocket=socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((server_ip, server_port))

user_database = []

print("Server Running")

message,client_address = serverSocket.recvfrom(2048)

x = User(str(client_address[0]), str(client_address[1]), message)
user_database.append(x)

user_database[0].printDetails()

# outputname = x.name
# output_ip = x.ip_address
# output_port = x.port_no

# print (outputname.decode())
# print (output_ip)
# print (output_port)



#print (x.name.decode() + " " + x.ip_address.decode())

# print (message.decode())
# print (str(client_address[0]))


