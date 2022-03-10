import hashlib
from http import client
from ipaddress import ip_address
from posixpath import split
from socket import *
from User import *

#server.py
#This is the server class for the chat application. Each client will connect to this server
def print_all_users():
    print ("Current users: ")
    for users in user_database:
        users.printDetails()
    print()

#This function receives a message from a client. The string the function receives contains a header, as well as message body. This
#function is responsible for decodig the message, differentiating between the header and the body, as well as performing the relevant
#actions to the message. 
#
#Parameters: 
#       String message: this is the full string the server receives from the client. 
#       List details: this is the details of the client who sent the message to the server. Details[0] gives the IP_addres; details[1] gives the port number.
#       List user_list: this is a list of users who are online on the client. The server cross checks the user_list with the target of the message, and finds
#           correct details to enable message forwarding. 

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

    if hashed_confirmation:
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
    else:
        error_message = create_out_message("Packets were lost, try send message again", "[Server]", "CORRUPTED")
        serverSocket.sendto(bytes(error_message.encode('utf-8')), (details[0], int(details[1])))
    
#This function is responsible for performing the necessary tasks on a message body, in order to send it to a client. This involves creating and attaching a
#message header - which is done by calling create_out_header(). The function returns a string which the server can send to a client. 
#
#Parameters: 
#       String message: this is the message body. 
#       String sender: this is the name of the sender of the message, details corresponding to the name can be found by 
#           searching through user_list and calling .name for each element in the list. 
#       String type: thhis is the type of message that is being sent - which tells the recipient what to do with the message. 

def create_out_message(message, sender, type):
    message_header = create_out_header(sender, message, type)
    created_message = str(message_header) + " <-HEADER||MESSAGE-> " + message
    return (created_message)

#This function creates a header for a message. It returns a list of the items in the header, which is then cast to a String by the create_out_message() function. 
#
#Parameters: 
#       String sender: the name of the client who sent the message. 
#       String content: the message body, which needs to be hashed and attached to the header. 
#       String type: the type of message (JOIN, CHAT, BROADCAST etc)

def create_out_header(sender, content, type):
    hashed_message = hashlib.sha256(content.encode('utf-8')).hexdigest()  
    sender = sender
    return [hashed_message, sender, type]

#This function is used by the process_full_message() function. It takes a String received by the server (which contains the message header & the body), and splits
#the string into the header and the message body. The function returns a list of the header and the body. 
#
#Parameters: 
#       String message: the string received by the server (containing a header & message body)

def decode_message(message):
    message = message.decode()
    split_message = str(message).split(" <-HEADER||MESSAGE-> ")
    return split_message

#This function is used to confirm that the body of a message received is the correct/full message. This is done by hashing the body of the message, and comparing it
#to the hash provided in the header. If they are the same, then the message was delivered correctly. Returns True if they are the same, and False if they are not. 
#
#Parameters: 
#       String hashed_string: this is the result of the message going through the hash function and then being passed through the hexidigest() function. 
#       String unhashed_string: this is the message body, which is yet to be passed through a hash function. 
def check_hashing(hashed_string, unhashed_string):
    x =  hashlib.sha256(unhashed_string.encode('utf-8')).hexdigest()  
    return (hashed_string == x)

#This function creates an object of User type and appends it to the user_list. The function checks to make sure that the username is unique, since duplicates
#are not allowed. The function returns True if the user has been succesfully created and added, and False if the request was unsuccesfull. 
#
#Parameters: 
#       String name: this is the name of the user. Must be unique. 
#       String details: these are the IP_address and port number of the user. 
#       List user_list: this is a list of current users connected to the server.

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

