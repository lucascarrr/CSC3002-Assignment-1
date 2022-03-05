from http import client
from posixpath import split
from socket import *
from User import *

def print_all_users():
    print ("Current users: ")
    for users in user_database:
        users.printDetails()
    print()

def process_full_message(message, details, user_list):
    decoded_message = decode_message(message)
    message_type = decoded_message[0]
    message_content = decoded_message[1]
    manage_type(decoded_message, details, user_list)


def decode_message(message):
    message = message.decode()
    split_message = str(message).split("||")
    return split_message

def manage_type(decoded_message, details, user_list):
    if (decoded_message[0] == "login_request"):
        create_user(decoded_message[1], details, user_list)
    elif (decoded_message[0] == "direct_message"):
        direct_message(decoded_message[1], user_list)

def direct_message(message, user_list):
    split_to_target = message.split("|@")
    target_name = split_to_target[1]
    if (target_name == ""):
        for user in user_list:
            serverSocket.sendto(bytes(split_to_target[0].encode('utf-8')), (user.ip_address, int(user.port_no)))
    else:
        for user in user_list:
            if (user.name in target_name):
                serverSocket.sendto(bytes(split_to_target[0].encode('utf-8')), (user.ip_address, int(user.port_no)))
            

def create_user(name, details, user_list):
    temp_user = User(str(details[0]), str(details[1]), name)
    user_list.append(temp_user)
    print ("user added")

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
        try:
            message,client_address = serverSocket.recvfrom(2048)
            received=True
            process_full_message(message, client_address, user_database)
        except:
            print ("Error receiving message")       

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




