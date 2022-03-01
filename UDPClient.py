from socket import*

serverName='hollyCSC-VirtualBox'
serverPort=12000
clientSocket=socket(AF_INET, SOCK_DGRAM)

while True:
    message=input()
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    returnMessage, serverAddress= clientSocket.recvfrom(2048)
    print (returnMessage.decode())
    
clientSocket.close()