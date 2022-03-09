from tkinter import *
import hashlib
import threading
import chime
from socket import *
from datetime import datetime
from interface import *
chime.theme('big-sur')


bg = "#203239"
system_text = "#C1666B"
user_text = "#E0DDAA"
font = "Helvetica 16 bold"
font_bold = "Helvertica 14 bold"

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

    def print_to_Screen(self, message):
        self.message_view.insert(END, message)
        chime.success()
        self.message_view.insert(END, "\n")

    # def login_on_enter(self, event):
    #     login_username = self.login_box.get("1.0", 'end-1c')
    #     log_in(login_username, self.is_logged_in)
    #     self.login_box.delete("1.0", END)
    #     return "break"

    def on_enter_press(self, event):
        message = self.text_widget.get("1.0", 'end-1c')
        while ("\n" not in message and message != ""):
            send_message(message, self.is_logged_in)
            self.text_widget.delete("1.0", END)
            return "break"

    def get_instructions():
        help = "/help : to view these instructions again"
        logout = "/exit"
        directed_message = "@target : to send a directed message - can be multiple targets, e.g. @target 1 @target 2 message"
        broadcast_message = "to send a message to everyone on the server, simply type the message and press enter"

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

    input_message = message_processing_out(message, logged_in, sender)
    client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

def recieve_messages(client_socket):
    while True:
        message, server_address = client_socket.recvfrom(2048)
        x = message_processing_in(message)
        try: 
            gui.print_to_Screen(x)
        except:
            continue
        #print(message.decode())

# def log_in(username, login_status):
#     sender = gui.username
#     input_message = message_processing_out(gui.username, login_status, sender)
#     client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

#seperates the message content from the header
def decode_message(message):
    message = message.decode()
    split_message = str(message).split(" <-HEADER||MESSAGE-> ")
    return split_message

#processes message (adds a header and other information)
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
        chime.error()
        gui.username=""
        gui.is_logged_in = False

    if (check_hashing(hashed_message, message_content)):
        return sender + ": " + message_content

def check_hashing(hashed_string, unhashed_string):
    x =  hashlib.sha256(unhashed_string.encode('utf-8')).hexdigest()  
    return (hashed_string == x)

#creates a header, given ceratain information
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

    #Message input/output handling
    input_message = ""
    logged_in = False
    sent = []
    outbox = []
    inbox = []       

    for i in range(1):
        rec = threading.Thread(target=recieve_messages, args=(client_socket, ))
        rec.start()

    gui = gui()
    gui.run()
