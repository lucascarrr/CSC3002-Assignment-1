import hashlib
from posixpath import split
import threading
from socket import *
from datetime import datetime
   
def send_message(message):      #send message to the server
    client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

def send_messages():
    if (len(outbox) != 0 ):
        pass

def recieve_messages(client_socket):
    while True:
        message, server_address = client_socket.recvfrom(2048)
        print(message.decode())

#processes message (adds a header and other information)
def message_processing(raw_message, logged_in):
    target_string = ""
    message_type = ""
    message_content = ""

    split_on_space = raw_message.split(" ")
    message_start_position = 0
   
    for current_word in split_on_space:
        if (current_word[0] != "@"):
            message_start_position = split_on_space.index(current_word)
            break

    content_list = split_on_space[message_start_position:]
    for x in content_list:
        message_content += x
        message_content += " "

    target_list = split_on_space[:message_start_position]
    for x in target_list:
        target_string += x[1:]
        target_string += " "

    if not logged_in:
        message_type = message_type_list[2]

    elif (message_start_position == 0):
        message_type = message_type_list[1]

    elif (message_start_position > 0):
        message_type = message_type_list[0]
        
    
    message_header = create_message_header(message_content, target_string, message_type)
    created_message = (str(message_header) + " <-HEADER||MESSAGE-> " + message_content)
    return created_message

#creates a header, given ceratain information
def create_message_header(message, targets, type):
    hashed_message = hashlib.sha256(message.encode('utf-8')).hexdigest()           #hashes the message content only
    print (hashed_message)
    message_time = datetime.now()
    message_time = message_time.strftime("%H:%M:%S")
    targets = targets
    message_type = type
    return [hashed_message, message_time, targets, message_type]


if __name__ == '__main__':
    #Server details
    server_ip = '127.0.0.1'            
    server_port = 12000
    client_socket=socket(AF_INET, SOCK_DGRAM)
    message_type_list = ["CHAT", "BROADCAST", "JOIN", "LEAVE"]

    #Message input/output handling
    input_message = ""
    sent = []
    outbox = []
    inbox = []          

    logged_in = False
    
    for i in range(1):
        rec = threading.Thread(target=recieve_messages, args=(client_socket,))
        rec.start()

    while True:                            
        if not logged_in:
            name = input("Enter your username: \n")
            input_message = message_processing(name, logged_in)
            logged_in = True
        
        else:
            x = input()
            input_message = message_processing(x, logged_in=True)
       
        if input_message != "":
            client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))


    


    
    


    