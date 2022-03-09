from tkinter import *
import hashlib
import threading
from socket import *
from datetime import datetime
from turtle import end_fill
from venv import create
from interface import *
from account import *

# Constants used by GUI
bg = "#EEF4ED"
system_text = "#C1666B"
user_text = "#4357AD"
font = "Helvetica 16 bold"
font_bold = "Helvertica 14 bold"

# GUI class made with Tkinter. Sets up windows and their corresponding functionality.
class gui:
    is_logged_in = False
    username = ""
    accounts = [Account("nil", "nil")] # create dummy account
   
    def __init__(self):
        self.window = Tk()
        self.setup_login_window()
    
    # Fucntion to ensure gui main loop is always running. 
    def run(self):
        self.window.mainloop()
    
    # Function to set up login window. On enter, logs user in.
    def setup_login_window(self):
        self.window.title("Login")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=300, height = 100, bg="#EEF4ED")
        self.window.eval('tk::PlaceWindow . center')

        # Login field
        login_label = Label(self.window, fg="#13315C", bg="#EEF4ED", text = "USERNAME:", font=font)
        login_label.place(relheight=0.4, relwidth=0.4, rely=0.3, relx=0)
        self.login_box = Text(self.window, width=1, height= 1, highlightthickness = 0, borderwidth=0,
                                    bg="#8DA9C4", fg="#0B2545", font=font,
                                    padx=3, pady=5)
        self.login_box.place(relheight=0.3, relwidth=0.5, rely=0.35, relx=0.37)
        self.login_box.focus()
        self.login_box.bind("<Return>", self.login_on_enter) 

    # Function to set up login window. On enter, password is saved and then confirmed.
    def setup_password_window(self):
        print("trying to set up")
        self.window.destroy()
        self.window = Tk()
        
        self.window.title("Password")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=300, height = 100, bg="#EEF4ED")
        self.window.eval('tk::PlaceWindow . center')

        #login field
        login_label = Label(self.window, fg="#13315C", bg="#EEF4ED", text = "PASSWORD:", font=font)
        login_label.place(relheight=0.4, relwidth=0.4, rely=0.3, relx=0)
        self.login_box = Text(self.window, width=1, height= 1, highlightthickness = 0, borderwidth=0,
                                    bg="#8DA9C4", fg="#0B2545", font=font,
                                    padx=3, pady=5)
        self.login_box.place(relheight=0.3, relwidth=0.5, rely=0.35, relx=0.37)
        self.login_box.focus()
        self.login_box.bind("<Return>", self.password_on_enter) 
        

    # Function to set up password incorrect pop up message upon a user entering an incorrect password should the username entered already exist.    
    def setup_password_popup(self):
        self.window = Tk()
        self.window.title("Login")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=450, height = 150, bg="#EEF4ED")
        self.window.eval('tk::PlaceWindow . center')

        #login field
        message_label = Label(self.window, fg="#13315C", bg="#EEF4ED", text = "INCORRECT PASSWORD FOR USERNAME \n PRESS ENTER TO TRY AGAIN.", font=font)
        message_label.place(rely=0.3, relx=0.12)
        
        
        
        self.button = Button(self.window,
                         text = "Try Again",
                         font = font,
                         command = lambda: self.setup_password_window())
        self.button.place(relx = 0.35,
                      rely = 0.7)
        
        self.window.mainloop()
        #message_label.bind("<Return>", self.window.destroy()) #this self.login xyz calls func to save username and call password window
       #this is not working why :(((((((((
        

    # Function to set up main chat window.
    def setup_main_window(self):
        self.window.destroy()
       
        self.window = Tk()

        self.window.title("Chatroom")
        
        self.window.resizable(width=False, height=False)
        self.window.configure(width=800, height=1200, bg=bg)
        self.window.eval('tk::PlaceWindow . center')
        
        head_label = Label(self.window, bg=bg, fg=system_text,
                                    text="Welcome to the chat",
                                    font=font_bold, pady=10)
        head_label.place(relwidth=1)

        #add label
        self.send_label = Label (self.window, text="Press [enter]\n to send", width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised", bg="#13315C", fg="#EEF4ED", font=font)
        self.send_label.place(relheight=0.825, relwidth=0.2, rely=0.9, relx=0.8)

        #text add widget
        self.text_widget = Text(self.window, width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised", bg="#8DA9C4", fg="#EEF4ED", font=font, padx=5, pady=5)
        self.text_widget.place(relheight=0.825, relwidth=0.8, rely=0.9)
        self.text_widget.configure(cursor="xterm")
        self.text_widget.focus()
        self.text_widget.bind("<Return>", self.on_enter_press)

        
        #text read widget
        self.message_view = Text(self.window, width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised",
                                    bg="#EEF4ED", fg="#134074", font=font,
                                    padx=5, pady=5)
        self.message_view.place(relheight=0.9, relwidth=1, rely=0)

    # Function to print messages to main chat window.   
    def print_to_Screen(self, message):
        self.message_view.insert(END, message)
        self.message_view.insert(END, "\n")

    # Function that saves username entry, calls log_in function and sets up password window.
    def login_on_enter(self, event):
        login_username = self.login_box.get("1.0", 'end-1c')
        log_in(login_username, self.is_logged_in)
        self.login_box.delete("1.0", END)
        self.setup_password_window()
    
    # Function that saves password entry, calls save_password function and sets up main chat window.
    def password_on_enter(self, event):
        password = self.login_box.get("1.0", 'end-1c')
        save_password(self.username, password, self.is_logged_in)
        self.login_box.delete("1.0", END)
        self.setup_main_window() 

    # Function that sends message typed in main chat window once enter is pressed. Calls send_message which sends message to server.
    def on_enter_press(self, event):
        message = self.text_widget.get("1.0", 'end-1c')
        while ("\n" not in message and message != ""):
            send_message(message, self.is_logged_in)
            self.text_widget.delete("1.0", END)
            return "break"

# Function that checks if password matches username in accounts array.
def check_password(password, username):
    for i in range(len(gui.accounts)):
        if gui.accounts[i].name == username:
            if password != gui.accounts.password:
                gui.incorrect_password_popup()
            else:
                print("User authenticated successfully.")

# Function that creates account object for a user and writes it to file.            
def create_account(username, password):
    account = Account(username, password)
    gui.accounts.append(account)
    fileObj = open("accounts.txt", "a")
    fileObj.write(username + "," + password)
    fileObj.write("\n")
    fileObj.close()

# Function that reads in existing accounts upon initiating a chat session.   
def read_in_accounts():
    fileObj = open("accounts.txt", "r") #opens the file in read mode
    words = fileObj.read().splitlines()
    for line in words:
        account = line.split(",")
        name = account[0]
        password = account[1]
        gui.accounts.append(Account(name, password))    
        #puts the file into an array
    fileObj.close()

# Saves user password and sends it to server. Calls password incorrect password if password does not match existing username.
def save_password(username, password, login_status):
    sender = username
    account_exist = False
    sent = False
    for i in range(len(gui.accounts)):
        print(gui.accounts[i].name)
        if gui.accounts[i].name == username:
            print("user exists")
            account_exist = True
            if password == gui.accounts[i].password:
                input_message = message_processing_out(password, login_status, sender, True)
                client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))
                sent = True
            else:
                gui.setup_password_popup()
    if account_exist != True:
        create_account(username, password)
    
    if sent == False:
        input_message = message_processing_out(password, login_status, sender, True)
        client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))                     

 # Function to send either a direct message or broadcast to server. 
def send_message(message, logged_in):

    if (gui.username == ""):
        sender = message
    else:
        sender = gui.username
    if ("@" in message):
        a = message.split(" ")
        b = len(a[0])
        gui.print_to_Screen("You: " + message[b:])
    elif (gui.is_logged_in):
        gui.print_to_Screen("You (broadcast): " + message)

    input_message = message_processing_out(message, logged_in, sender, False)
    client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

# Function to recieve messafes from server (broadcast/chat messages from other users) and prints to gui.
def recieve_messages(client_socket):
    while True:
        message, server_address = client_socket.recvfrom(2048)
        x = message_processing_in(message)
        try: 
            gui.print_to_Screen(x)
        except:
            continue
        #print(message.decode())

# Function to send username to server. 
def log_in(username, login_status):
    sender = username
    input_message = message_processing_out(username, login_status, sender, False)
    client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

# Function to seperate the message content from the header
def decode_message(message):
    message = message.decode()
    split_message = str(message).split(" <-HEADER||MESSAGE-> ")
    print("split is")
    print(split_message)
    return split_message

# Function to processes an outgoing message (add a header and other information)
def message_processing_out(raw_message, logged_in, sender, password):
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
        gui.username = message_content
        if password == True:
            message_type = message_type_list[6]
            gui.is_logged_in = True

    elif (message_start_position == 0):
        message_type = message_type_list[1]
    
    elif (message_start_position > 0):
        message_type = message_type_list[0]
    
    print("msg content:" + message_content)
    message_header = create_message_header(message_content, target_string, message_type, sender)
    created_message = (str(message_header) + " <-HEADER||MESSAGE-> " + message_content)
    print(created_message)
    return created_message

# Function to process an incoming message in order for it to be reaable by user. Takes away unnecessary info, header etc.
def message_processing_in(raw_message):
    decoded_message = decode_message(raw_message)
    #print(raw_message)
    print(decoded_message)
    header = str(decoded_message[0])
    print(header)
    header = header.replace("'", "")
    print(header)
    header = header.replace(" ", "")
    print(header)
    header = header[1:(len(header)-1)]
    print(header)
    header = header.split(",")
    #print(header)

    message_content = str(decoded_message[1])
    hashed_message = header[0]
    sender = header[1]
    
    if (message_type_list[4] in header):
        gui.is_logged_in = True
        print ("done")
    elif (message_type_list[5] in header):
        gui.username=""
        #gui.is_logged_in = False

    if (check_hashing(hashed_message, message_content)):
        return sender + ": " + message_content

# Function to check hashing of messages.
def check_hashing(hashed_string, unhashed_string):
    x =  hashlib.sha256(unhashed_string.encode('utf-8')).hexdigest()  
    return (hashed_string == x)

# Function to create a header
def create_message_header(message, targets, type, sender):
    hashed_message = hashlib.sha256(message.encode('utf-8')).hexdigest()
    message_time = datetime.now()
    message_time = message_time.strftime("%H:%M:%S")
    targets = targets
    message_type = type
    sender = sender
    return [hashed_message, message_time, targets, message_type, sender]  

if __name__=="__main__":
    #Server details
    server_ip = '127.0.0.1'            
    server_port = 12000
    client_socket=socket(AF_INET, SOCK_DGRAM)
   
 
    message_type_list = ["CHAT", "BROADCAST", "JOIN", "LEAVE", "CONFIRMATION", "REJECTION", "PASSWORD"]

    #Message input/output handling
    input_message = ""
    logged_in = False
    sent = []
    outbox = []
    inbox = []       



    # input_message = message_processing("lucas", logged_in, sender)
    # client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))
    # logged_in = True

    for i in range(1):
        rec = threading.Thread(target=recieve_messages, args=(client_socket, ))
        rec.start()

    gui = gui()
    read_in_accounts()
    gui.run()
