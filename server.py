from socket import*

serverName='127.0.0.1'
serverPort=12000
serverSocket=socket(AF_INET, SOCK_DGRAM)

serverSocket.bind((serverName, serverPort))

print("The server is ready to receive")


while True:

    message,clientAddress=serverSocket.recvfrom(2048)
    print ("client says: " + str(message))
    returnMessage=input("server says: ")
    serverSocket.sendto(returnMessage.encode('utf-8'), (clientAddress))