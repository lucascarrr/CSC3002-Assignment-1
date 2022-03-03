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
            print (data.decode())

for i in range(5):
    threading.Thread(target=receiving, args=("RecvThread", clientSocket)).start()

name= input("Name: ")
message=''

while message != 'Quit':
    message=input()
    if message != '':
        clientSocket.sendto((name+ ": " + message).encode(), server)    
    time.sleep(0.1)
    
quit=True
clientSocket.close()