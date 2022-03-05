# import all the required  modules
import socket
import threading
from tkinter import *

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
       
        self.Window = Tk()
        self.Window.withdraw()
         
        # login window
        self.login = Toplevel()
        # set the title
        self.login.configure(bg="white")
        self.login.title("Login")
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 194)
        # create a Label
        self.pls = Label(self.login,
                       text = "Enter your name:",
                       bg="white",
                       anchor="e",
                       justify = LEFT,
                       font = "Roboto 14")
         
        self.pls.place(relheight = 0.1,
                       relx = 0.05,
                       rely = 0.2)

         
        # create a entry box for typing the messafe. this entry box input needs to link to 
        self.entryName = Entry(self.login,
                             font = "Roboto 14", bg="#7C7AFE")
         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.05,
                             rely = 0.35)
         
        # set the focus of the cursor
        self.entryName.focus()
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE",
                         font = "Helvetica 14 bold",
                         command = lambda: self.choose_to_chat(self.entryName.get()))
         
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
 
    # The main layout of the chat
    # switch to layout, once thread starts and thread starts in gui when button after login is pressed
    # happens in lucas+holly code once logged in = true
    # so if logged in = true, create this layout window...
    # and when button press is sent, put message into socket etc...
    def sendButton(self,name):
        message = self.entryMsg
        target = self.entryFriend
        input_message = 'direct_message||' + message + "|@" + target 
    

    def new_chat(self,name):
        self.name = name
        menu = Menu(self.name)

        self.name.config(menu=menu)

    def choose_to_chat(self,name):
        self.login.destroy()
        self.name = name
        self.choose = Toplevel()

        self.choose.configure(bg = "white",
            width = 400,

                              height = 194,
                              )
        
        self.choose.title("Pick a friend")

        self.label = Label(self.choose,
                            text="Enter your friends screen name:",
                            font = "Roboto 14",                   
                            anchor="e",
                            justify = LEFT,
                            
        )

        self.label.place(relheight = 0.1,
                       relx = 0.05,
                       rely = 0.2)

        self.entryName = Entry(self.choose,
                             font = "Roboto 14", bg="#7C7AFE")
         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.05,
                             rely = 0.35)
         
        # set the focus of the cursor
        self.entryName.focus()

        self.go = Button(self.choose,
                         text = "CHAT",
                         font = "Helvetica 14 bold",
                         command = lambda: layout(self, name))
         
        self.go.place(relx = 0.4,
                      rely = 0.55)


        # self.pls = Label(self.login,
        #                text = "Who do you want to chat to?",
        #                bg="white",
        #                anchor="e",
        #                justify = LEFT,
        #                font = "Roboto 14")
         
def layout(self,name):
        self.choose.destroy()
       
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "white")
        self.labelHead = Label(self.Window,
                             bg = "#8DA9C4",
                              fg = "#EAECEE",
                              text = "Chat" ,
                               font = "Roboto 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "white")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
         
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#134074",
                             fg = "#8DA9C4",
                             bd=0,
                             font = "Roboto 14")
         
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
         
        self.labelBottom = Label(self.Window,
                                 bg = "#13315C",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
         
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#EBF0EA",
                              fg = "black",
                              font = "Roboto 13")
         
        # # place the given widget
        # # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
         
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#8DA9C4",
                                command = lambda : self.sendButton(self.entryMsg.get()))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)
 
