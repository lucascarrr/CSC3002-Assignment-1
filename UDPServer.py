from socket import*
import threading
import time

serverPort=12000
serverSocket=socket(AF_INET, SOCK_DGRAM)

a=serverSocket.bind(('', serverPort))

clients=[]

print("The server is ready to receive")

end= False

while not end:
    data, clientAddress=serverSocket.recvfrom(2048)
    if "Quit" in str(data):
        end= True
    if clientAddress not in clients:
        clients.append(clientAddress)
    for client in clients:
        if client!=clientAddress:
               serverSocket.sendto(data, clientAddress)
    print (time.ctime(time.time()) + str(clientAddress) + " : " + str(data))
    
serverSocket.close() 