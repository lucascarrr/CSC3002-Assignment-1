from socket import*
import threading
import time

quit=False

serverPort=12000
clientSocket=socket(AF_INET, SOCK_DGRAM)
serverName=gethostname()
server= (serverName, serverPort)

def receiving (name, socket):
    while not quit:
        while True:   
            data, address= socket.recvfrom(2048)
            print (str(data))


for i in range(5):
    threading.Thread(target=receiving, args=("RecvThread", clientSocket)).start()

name=input("Name: ")
message=input(name + ": ")

while message != 'Quit':
    if message != '':
        clientSocket.sendto(message.encode(), server)
    message= input(name + ": ")
    
    time.sleep(0.1)
    
quit=True
clientSocket.close()