from socket import*

serverName='127.0.0.1'
serverPort=12000
clientSocket=socket(AF_INET, SOCK_DGRAM)

clientSocket.sendto(''.encode('utf-8'), (serverName, serverPort))

returnMessage, serverAddress= clientSocket.recvfrom(2048)
print ("[Server] " + returnMessage.decode())

message=input()
clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
    
clientSocket.close()