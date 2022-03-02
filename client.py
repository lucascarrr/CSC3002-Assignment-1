
from socket import*

serverName='127.0.0.1'
serverPort=12000
clientSocket=socket(AF_INET, SOCK_DGRAM)

while True:
    message=input("client says: ")
    clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))
    returnMessage, serverAddress= clientSocket.recvfrom(2048)
    print ("server says: " + str(returnMessage))
    
clientSocket.close()