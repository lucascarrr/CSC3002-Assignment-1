import threading
from socket import *
import random

def send_message(message):      #send message to the server
    client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

def send_messages():
    if (len(outbox) != 0 ):
        pass

def recieve_messages(client_socket):
    while True:
        message, server_address = client_socket.recvfrom(2048)
        print(message.decode())


if __name__ == '__main__':
    #Server details
    server_ip = '127.0.0.1'            
    server_port = 12000
    client_socket=socket(AF_INET, SOCK_DGRAM)

    #encryption
    g_variable = 3
    n_variable = 1234567891011
    private_variable = random.randrage(1,2000)
    first_sum = (g_variable ** private_variable ) % n_variable

    #Message input/output handling
    input_message = ""
    sent = []
    sent_counter = 0
    outbox = []
    inbox = []
    
    #Starting send and receive threads
    # start_receiving = Thread(target=recieve_messages, args=())
    # start_sending = Thread(target=send_messages, args=())
    # start_receiving.start()
    # start_sending.start()

    logged_in = False

    for i in range(1):
        rec = threading.Thread(target=recieve_messages, args=(client_socket,))
        rec.start()

    while True:
        
        if not logged_in:
            name = input("Enter your username: \n")
            input_message = 'login_request||' + name + '||' + sent_counter
            logged_in = True
        else:
            input_message = input("Direct Message: ")
            target = input("Target: ")                                                      #if you want to send to everyone, leave blank, for james type 'james, for james and tom type 'james tom'
            input_message = 'direct_message||' + input_message + "|@" + target + '||' + sent_counter                     

        if input_message != "":
            sent.append(input_message)
            sent_counter += 1
            client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))
            


    


    
    


    