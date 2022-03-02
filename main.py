from socket import *

if __name__ == '__main__':

    name = input("Enter your name: ")
    server_ip = '127.0.0.1'             #maybe allow for input in future
    server_port = 12000
    
    client_socket=socket(AF_INET, SOCK_DGRAM)
    client_socket.sendto(name.encode('utf-8'), (server_ip, server_port))
    


    