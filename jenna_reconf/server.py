from http import client
from posixpath import split
from socket import *
from time import time
from User import *
from client import *

def print_all_users():
    print ("Current users: ")
    for users in user_database:
        users.printDetails()
    print()

# def process_full_message(message, details, user_list):
#     decoded_message = decode_message(message)
#     message_type = decoded_message[0]
#     message_content = decoded_message[1]
#     manage_type(decoded_message, details, user_list)

def process(message, client_address, user_database):
    message = message.decode()
    message_array = message.split(" ")
    print(message_array[0])
    message_dict = {'type': message_array[0], 
                    'time': message_array[1], 
                    'message_sender': message_array[2],
                    'hash_message': message_array[3], 
                    'client_address': client_address, 
                    'user_database': user_database,
                    'reciever': message_array[4]}
    return message_dict
    
def create_message(raw_message, sender, type):
    print("trying to create")
    message_time = datetime.now()
    message_time = message_time.strftime("%H:%M:%S")
    raw_message_array = raw_message.split(" ")
    reciever = raw_message_array[0]
    raw_message_array.remove(reciever)
    message = " ".join(raw_message_array)
    hashed_message = hashlib.sha256(message.encode('utf-8')).hexdigest()  
    return type + " " + message_time + " " + sender + " " + hashed_message + " " + reciever 

def interpret_type(message_dict):
    print("trying to interpret")
    message_type = message_dict['type']
    if message_type == "ACK":
        client_address = message_dict['client_address']
        message = create_message("Acknowledgement request", "Server", "ACK")
        serverSocket.sendto(message.encode('utf-8'), client_address)
        
        print("Connection successful.")
        print(message_dict['type'])

    elif type == "JOIN":
        create_user(message_dict['message_sender'], client_address, message_dict['user_database'])
    elif type == "CHAT":
        direct_message(message_dict.get['reciever'], message_dict['hash_message'], message_dict['user_database'])


# def decode_message(message):
#     message = message.decode()
#     split_message = str(message).split("||")
#     return split_message

# def manage_type(decoded_message, details, user_list):
#     if (decoded_message[0] == "login_request"):
#         create_user(decoded_message[1], details, user_list)
#     elif (decoded_message[0] == "direct_message"):
#         direct_message(decoded_message[1], user_list)


# ask what is going on here?? with encode split to target
def direct_message(reciever, message, user_list):
    #split_to_target = message.split("|@")
    #target_name = split_to_target[1]
    if (reciever == "everyone"):
        for user in user_list:
            serverSocket.sendto(bytes(split_to_target[0].encode('utf-8')), (user.ip_address, int(user.port_no)))
    else:
        for user in user_list:
            if (user.name == reciever):
                serverSocket.sendto(bytes(split_to_target[0].encode('utf-8')), (user.ip_address, int(user.port_no)))
            

def create_user(name, client_address, user_list):
    temp_user = User(str(client_address[0]), str(client_address[1]), name)
    user_list.append(temp_user)
    print ("User added")
    #textbox gui pop up

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
        message_dict = process(message, client_address, user_database)
        interpret_type(message_dict)

        
        
        
        
        # print (full_data)
        # decoded_message = decode_message(message)
        # message_type = decoded_message[0]
        # message_content = decoded_message[1]


        

        # x = User(str(client_address[0]), str(client_address[1]), message)
        # user_database.append(x)

        # user_database[connections_counter].printDetails()
        # connections_counter += 1





    # user_database[connections_counter].printDetails()
    # connections_counter += 1
    # print_all_users()


