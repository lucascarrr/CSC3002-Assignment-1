from tkinter import *
import hashlib
import threading
from socket import *
from datetime import datetime
from interface import *

bg = "#203239"
system_text = "#C1666B"
user_text = "#E0DDAA"
font = "Helvetica 16 bold"
font_bold = "Helvetica 14 bold"
welcome_font = "Helvetica 14 bold"
instructions_font = "Helvetica 14"

class gui:
    is_logged_in = False
    username = ""
   
    def __init__(self):
        self.window = Tk()
        self.setup_main_window()
        #self.setup_login_window()
    
    def run(self):
        self.window.mainloop()
    
    def setup_login_window(self):
        self.window.title("Login")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=300, height = 100, bg="#203239")
        self.window.eval('tk::PlaceWindow . center')

        #login field
        login_label = Label(self.window, fg="#E0DDAA", bg="203239", text = "USERNAME:", font=font)
        login_label.place(relheight=0.4, relwidth=0.4, rely=0.3, relx=0)
        self.login_box = Text(self.window, width=1, height= 1, highlightthickness = 0, borderwidth=0,
                                    bg="#8DA9C4", fg="#0B2545", font=font,
                                    padx=3, pady=5)
        self.login_box.place(relheight=0.3, relwidth=0.5, rely=0.35, relx=0.37)
        self.login_box.focus()
        self.login_box.bind("<Return>", self.login_on_enter)

    def setup_main_window(self):
        self.window.title("Chatroom")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=800, bg="#141E27")
        self.window.eval('tk::PlaceWindow . center')

        head_label = Label(self.window, bg="#203239", fg="#E0DDAA",
                                    text="Welcome to the chat",
                                    font=font_bold, pady=10)
        head_label.place(relwidth=1)

        #add label
        self.send_label = Label (self.window, text="Press [enter]\n to send", width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised", bg="#13315C", fg="#EEF4ED", font=font)
        self.send_label.place(relheight=0.825, relwidth=0.2, rely=0.9, relx=0.8)

        #text add widget
        self.text_widget = Text(self.window, width=30, height=2, highlightthickness = 0, borderwidth=0, 
                            relief="raised", bg="#141E27", fg=user_text, font=font, padx=5, pady=5)
        self.text_widget.place(relheight=0.825, relwidth=0.8, rely=0.9)
        self.text_widget.configure(cursor="xterm")
        self.text_widget.focus()
        self.text_widget.bind("<Return>", self.on_enter_press)
    
        #text read widget
        self.message_view = Text(self.window, width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised",
                                    bg=bg, fg=user_text, font=font,
                                    padx=5, pady=5)
        self.message_view.place(relheight=0.9, relwidth=1, rely=0)
  

        self.message_view.tag_config('welcome', foreground="#94d2bd", font=welcome_font)
        self.message_view.tag_config('received', foreground="#48cae4", font=welcome_font)
        self.message_view.tag_config('broadcast', foreground="#e9d8a6", font=welcome_font)
        self.message_view.tag_config('self', foreground="#fec5bb", font=welcome_font)
        self.message_view.tag_config('instruction', foreground="#fae1dd", font=instructions_font)

        self.message_view.insert(END, self.welcome_message(), 'welcome')
        self.print_to_Screen(self.get_instructions(), 'instruction')


    def print_to_Screen(self, message, tag):
        self.message_view.insert(END, message, tag)
        self.message_view.insert(END, "\n")

    # def login_on_enter(self, event):
    #     login_username = self.login_box.get("1.0", 'end-1c')
    #     log_in(login_username, self.is_logged_in)
    #     self.login_box.delete("1.0", END)
    #     return "break"

    def on_enter_press(self, event):
        message = self.text_widget.get("1.0", 'end-1c')
        while ("\n" not in message and message != ""):
            if (message == "/help"):
                self.print_to_Screen(self.get_instructions(), 'instruction')
                self.text_widget.delete("1.0", END)
                return "break"
            elif (message == "/exit"):
                exit()
            else:
                send_message(message, self.is_logged_in)
                self.text_widget.delete("1.0", END)
                return "break"

    def get_instructions(self):
        help = "-> /help : to view these instructions again\n"
        logout = "-> /exit to exit the program\n"
        directed_message = "-> @target <message> : to send a directed message, can be multiple targets, \n      e.g. @target1 @target2 <message>\n"
        broadcast_message = "-> to send a broadcast message, simply type the message and press enter\n"
        return (help + logout + directed_message + broadcast_message)

    
    def welcome_message(self):
        return ("Welcome to the chatroom.\nPlease type your username to log in.\n\n")

def send_message(message, logged_in):
    if (gui.username == ""):
        sender = message
    else:
        sender = gui.username
    if ("@" in message):
        a = message.split(" ")
        b = len(a[0])
        gui.print_to_Screen("You: " + message[b:], 'self')
    elif (gui.is_logged_in):
        gui.print_to_Screen("You (broadcast): " + message, 'broadcast')

    input_message = message_processing_out(message, logged_in, sender)
    client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

#This function is responsible for getting messages from the server; when the method is called, a continous loop listens for messages.
#The message is then put through the 'message_processing_in()' function, and then displayed on the gui. 
#
#Parameters: 
#       socket client_socket: this is the socket for the client, which receives messages from the server

def recieve_messages(client_socket):
    while True:
        message, server_address = client_socket.recvfrom(2048)
        x = message_processing_in(message)
        try: 
            gui.print_to_Screen(x, 'received')
        except:
            continue

#This function is used by the message_processing_in() function. It takes a String received by the server (which contains the message header & the body), and splits
#the string into the header and the message body. The function returns a list of the header and the body. 
#
#Parameters: 
#       String message: the string received by the server (containing a header & message body)

def decode_message(message):
    message = message.decode()
    split_message = str(message).split(" <-HEADER||MESSAGE-> ")
    return split_message

#This function is responsible for performing the necessary actions on a message the user would like to send. The function figures out if the message is a direct
#message, broadcast, login-request - and attaches the relevant information to the header. This is done by calling the create_message_header() function. 
#
#Parameters: 
#       String raw_message: this is the input received from the user, it might look like "@someone here is my message", or just simply be text e.g. "my message". 
#                           the function must work out what type of request it is by looking for keywords, or booleans (such as '@', or checking if the user has 
#                           logged on already).
#       boolean logged_in: a boolean which returns True if the client has already connected to the server, False otherwise. 
#       String sender: a string containing the username of the client - the server uses this information. 

def message_processing_out(raw_message, logged_in, sender):
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
        #gui.is_logged_in = True

    elif (message_start_position == 0):
        message_type = message_type_list[1]

    elif (message_start_position > 0):
        message_type = message_type_list[0]
        
    message_header = create_message_header(message_content, target_string, message_type, sender)
    created_message = (str(message_header) + " <-HEADER||MESSAGE-> " + message_content)
    return created_message

#This function is responsible for understanding/processing a message received from the server. The message from the server will have a header and a message body, 
#the function will split this up and perform the relevant actions to handle the message request. 
#
#Parameters: 
#       String raw_message: this is a string containing the message header and the message body. 

def message_processing_in(raw_message):
    decoded_message = decode_message(raw_message)
    
    header = str(decoded_message[0])
    header = header.replace("'", "")
    header = header.replace(" ", "")
    header = header[1:(len(header)-1)]
    header = header.split(",")

    message_content = str(decoded_message[1])
    hashed_message = header[0]
    sender = header[1]
    
    if (message_type_list[4] in header):
        gui.is_logged_in = True
        print ("done")
    elif (message_type_list[5] in header):
        gui.username=""
        gui.is_logged_in = False

    if (check_hashing(hashed_message, message_content)):
        return sender + ": " + message_content
    else:
    	input_message = message_processing_out("@"+sender + ": Packets were lost, try send message again", logged_in, sender, False) 
    	client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))
    	return ("Sender will resend message as packets were lost") 

#This function is used to confirm that the body of a message received is the correct/full message. This is done by hashing the body of the message, and comparing it
#to the hash provided in the header. If they are the same, then the message was delivered correctly. Returns True if they are the same, and False if they are not. 
#
#Parameters: 
#       String hashed_string: this is the result of the message going through the hash function and then being passed through the hexidigest() function. 
#       String unhashed_string: this is the message body, which is yet to be passed through a hash function. 

def check_hashing(hashed_string, unhashed_string):
    x =  hashlib.sha256(unhashed_string.encode('utf-8')).hexdigest()  
    return (hashed_string == x)

#This function creates a header for a message. It returns a list of the items in the header, which is then cast to a String by the create_out_message() function. 
#
#Parameters: 
#       String sender: the name of the client who sent the message. 
#       String content: the message body, which needs to be hashed and attached to the header. 
#       String type: the type of message (JOIN, CHAT, BROADCAST etc)

def create_message_header(message, targets, type, sender):
    hashed_message = hashlib.sha256(message.encode('utf-8')).hexdigest()           #hashes the message content only
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
 
    message_type_list = ["CHAT", "BROADCAST", "JOIN", "LEAVE", "CONFIRMATION", "REJECTION"]      

    for i in range(1):
        rec = threading.Thread(target=recieve_messages, args=(client_socket, ))
        rec.start()

    gui = gui()
    gui.run()
