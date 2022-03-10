
#  CSC3002-Assignment-1

**Group Members**

 - Lucas Carr || CRRLUC003 
 - Jenna Jones || JNSJEN017
 - Holly Judge || JDGHOL001

***To Run the Program***

- open a terminal and cd into the project directory 
- run the 'server.py' file
- for each user you would like to add to the chat: open another terminal and run the 'interface.py' file
- 
Doing the above will run the server on your localhost IP_address ('127.0.0.1'). If you wish to run the program using your own IP_address:

- open a terminal and cd into the project directory
- run the 'server.py' file with the desired IP_address as an argument, e.g. **_python3 server.py 192.168.0.17_**
- for each user you would like to add to the chat: open another terminal and run the 'interface.py' file with the same argument as you ran the server,
   e.g. **_python3 interface.py 192.168.0.17_**
   
_please be careful about the IP_address you pass as an argument_

***Guide***

Although there is information on how to navigate the chatroom displayed on the gui; it might be useful to have it here too. 
When the gui loads, the first thing you should do is to login. To login, simply enter your desired username and press <enter>. Make sure that this username is unique, as the server does not allow for duplicates!
 
Once you have logged in, you are able to chat. 
To send a direct message to another user, type their username preceeded by an '@' symbol - like this: **@lucas hey**
The direct message feature allows you to send a direct message to multiple targets; to do this you simply insert multiple usernames after one another - like this: **@lucas @jenna hey guys**
 
If you would like to send a broadcast message (this is a message that will go to everyone on the server - simply type your message and press <enter>. 
 


