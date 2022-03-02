from socket import*
import User

serverName='127.0.0.1'
serverPort=12000
serverSocket=socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

user_database = []


print("Server Running")

message,clientAddress=serverSocket.recvfrom(2048)


serverSocket.sendto("Please enter your name: ".encode('utf-8'), (clientAddress))

message,clientAddress=serverSocket.recvfrom(2048)
print (message.decode())