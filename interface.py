from tkinter import *
import hashlib
import threading
from socket import *
from datetime import datetime
from interface import *

bg = "#EEF4ED"
system_text = "#C1666B"
user_text = "#4357AD"
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
        self.window.configure(width=300, height = 100, bg="#EEF4ED")
        self.window.eval('tk::PlaceWindow . center')

        #login field
        login_label = Label(self.window, fg="#13315C", bg="#EEF4ED", text = "USERNAME:", font=font)
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
        self.window.configure(width=800, height=1200, bg=bg)
        self.window.eval('tk::PlaceWindow . center')

        head_label = Label(self.window, bg=bg, fg=system_text,
                                    text="Welcome to the chat",
                                    font=font_bold, pady=10)
        head_label.place(relwidth=1)

        #text add widget
        self.text_widget = Text(self.window, width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised",
                                    bg="#8DA9C4", fg="#EEF4ED", font=font,
                                    padx=5, pady=5)
        self.text_widget.place(relheight=0.825, relwidth=1, rely=0.9)
        self.text_widget.configure(cursor="xterm")
        self.text_widget.focus()
        self.text_widget.bind("<Return>", self.on_enter_press)
    
        #text read widget
        self.message_view = Text(self.window, width=30, height=2, highlightthickness = 0, borderwidth=0, relief="raised",
                                    bg="#EEF4ED", fg="#134074", font=font,
                                    padx=5, pady=5)
        self.message_view.place(relheight=0.9, relwidth=1, rely=0)

    def print_to_Screen(self, message):
        self.message_view.insert(END, message)
        self.message_view.insert(END, "\n")

    def login_on_enter(self, event):
        login_username = self.login_box.get("1.0", 'end-1c')
        log_in(login_username, self.is_logged_in)
        self.login_box.delete("1.0", END)
        return "break"

    def on_enter_press(self, event):
        message = self.text_widget.get("1.0", 'end-1c')
        send_message(message, self.is_logged_in)
        self.text_widget.delete("1.0", END)
        return "break"
  
def send_message(message, logged_in):
    sender = gui.username
    input_message = message_processing(message, logged_in, sender)
    client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

def recieve_messages(client_socket):
    while True:
        message, server_address = client_socket.recvfrom(2048)
        gui.print_to_Screen(message.decode())
        #print(message.decode())

def log_in(username, login_status):
    sender = username
    input_message = message_processing(username, login_status, sender)
    client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))

#processes message (adds a header and other information)
def message_processing(raw_message, logged_in, sender):
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
        gui.is_logged_in = True

    elif (message_start_position == 0):
        message_type = message_type_list[1]

    elif (message_start_position > 0):
        message_type = message_type_list[0]
        
    
    message_header = create_message_header(message_content, target_string, message_type, sender)
    created_message = (str(message_header) + " <-HEADER||MESSAGE-> " + message_content)
    return created_message

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
 
    message_type_list = ["CHAT", "BROADCAST", "JOIN", "LEAVE"]

    #Message input/output handling
    input_message = ""
    sent = []
    outbox = []
    inbox = []       
    logged_in = False


    # input_message = message_processing("lucas", logged_in, sender)
    # client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))
    # logged_in = True

    for i in range(1):
        rec = threading.Thread(target=recieve_messages, args=(client_socket, ))
        rec.start()

    gui = gui()
    gui.run()


    # message = input()
    # input_message = message_processing(message, logged_in, input_name)
    # client_socket.sendto(input_message.encode('utf-8'), (server_ip, server_port))