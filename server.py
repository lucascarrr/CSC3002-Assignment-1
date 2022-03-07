import hashlib
from http import client
from ipaddress import ip_address
from posixpath import split
from socket import *
from User import *
#header = [0=hashed message, 1=message_time, 2=targets, 3=message_type]

def print_all_users():
    print ("Current users: ")
    for users in user_database:
        users.printDetails()
    print()

def process_full_message(message, details, user_list):
    decoded_message = decode_message(message)

    #clean this up maybe
    header = str(decoded_message[0])
    header = header.replace("'", "")
    header = header.replace(" ", "")
    header = header[1:(len(header)-1)]
    header = header.split(",")
    message_content = str(decoded_message[1])
    
    #assigning variables
    message_type = header[3]
    #print (header[3]) - shows type of request (for debugging)
    hashed_confirmation = check_hashing(header[0][:(len(header[0]))], message_content)
    targets = header[2]
    time = header[1]
    sender = header[4]
    # print (header[4])
    
    #handling message types
    if (message_type == "JOIN"):
        user_created = create_user(message_content, details, user_list)

        if not user_created:
            out_message = create_out_message("Username in use. Try again", "[Server]", "REJECTION")
            serverSocket.sendto(bytes(out_message.encode('utf-8')), (details[0], int(details[1])))
        else:
            temp = sender + " has joined the server"
            out_message = create_out_message(temp, "[server]", "CONFIRMATION")
            for user in user_list:
                serverSocket.sendto(bytes(out_message.encode('utf-8')), (user.ip_address, int(user.port_no)))
            
        #insert outmessage here
    elif (message_type == "CHAT"):
        out_message = create_out_message(message_content, sender, "CHAT")
        for user in user_list:
            if (user.name in targets):
                serverSocket.sendto(bytes(out_message.encode('utf-8')), (user.ip_address, int(user.port_no)))
                #  serverSocket.sendto(bytes((sender + ": " + message_content).encode('utf-8')), (user.ip_address, int(user.port_no)))

    elif (message_type == "BROADCAST"):
        out_message = create_out_message(message_content, (sender + "( broadcast )"), "BROADCAST")
        for user in user_list:
            if (user.name != sender):
            #  serverSocket.sendto(bytes((sender + ": " + message_content).encode('utf-8')), (user.ip_address, int(user.port_no)))
                serverSocket.sendto(bytes(out_message.encode('utf-8')), (user.ip_address, int(user.port_no)))

def create_out_message(message, sender, type):
    message_header = create_out_header(sender, message, type)
    created_message = str(message_header) + " <-HEADER||MESSAGE-> " + message
    return (created_message)

def create_out_header(sender, content, type):
    hashed_message = hashlib.sha256(content.encode('utf-8')).hexdigest()  
    sender = sender
    return [hashed_message, sender, type]

#seperates the message content from the header
def decode_message(message):
    message = message.decode()
    split_message = str(message).split(" <-HEADER||MESSAGE-> ")
    return split_message

#confirms that correct message was delivered to the server (check again on receiving message*)
def check_hashing(hashed_string, unhashed_string):
    x =  hashlib.sha256(unhashed_string.encode('utf-8')).hexdigest()  
    return (hashed_string == x)

#creates a user and adds to the database
def create_user(name, details, user_list):
    temp_user = User(str(details[0]), str(details[1]), name)
    print(len(user_list))
    if len(user_list) == 0:
        user_list.append(temp_user)
        return True
    else:
        for user in user_list:
            if (temp_user.name == user.name):
                return False
  
    user_list.append(temp_user)
    print (temp_user.name + " user added")
    return True


if __name__ == '__main__':
    user_database = []
    message_database = []
    connections_counter = 0 

    server_ip = '127.0.0.1'
    server_port = 12000
    serverSocket=socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((server_ip, server_port))
    print("Server Running")

    while True:
        message,client_address = serverSocket.recvfrom(2048)
        print (message)
        process_full_message(message, client_address, user_database)

