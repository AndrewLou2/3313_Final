from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.constants import CENTER, E, W

#handling receiving a message and threading it 
def receive_msg():
    while True:  #as long as there's no operating system errors, keep receiving messages from the client, decoding, and threating it
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            msg_list.see(tkinter.END)
        except OSError:  #if there's an error, break from the loop and stop receiving messages from the client
            break

#handling sending the client's message 
def send_msg(event=None):  
    msg = client_msg.get()  # getting the client's message
    client_msg.set("")    
    global current_room
    #if client's message is "quit"
    if msg == "{quit}":
        client_socket.send(bytes(my_username.get() + " has left the chat!", "utf8")) #sending message with the client's username to notify the server that the client left the chat
        client_socket.close()  #closing client's socket
        top.quit()  #quitting the application
        return
    #otherwise, send the client's username followed by their message, separated by a semicolon
    client_socket.send(bytes(my_username.get() + ": " + msg, "utf8")) 

#handles client closing the window
def close_window(event=None):
    client_msg.set("{quit}")  #sending the quit message to notify the server 
    send_msg()

#handles the client switching chatrooms
def switch_room():
    global current_room
    current_room = ((selected_room.get()).split(' '))[2]
    client_socket.send(bytes("/" + current_room, "utf8"))
    msg_list.delete(0, tkinter.END)
    msg_list.insert(tkinter.END, "you've switched to room " + str(current_room))  #notify the client the room they've switched to
    msg_list.see(tkinter.END)

#setting global variables
num_rooms = 0 #storing the number of rooms
current_room = 0 #storing the client's current room's room number

#creating the GUI
top = tkinter.Tk()  #using tkinter
top.geometry("660x600")  #setting window size
top.title("chat room app")  #add a title to the app
messages_frame = tkinter.Frame(top)  #adding a frame to the top

#initializing default values
client_msg = tkinter.StringVar()  #messages to be sent
client_msg.set("")  #setting default message as "" 
my_username = tkinter.StringVar()  #username to be set
my_username.set("")  #setting the default username as "" 

#creating a label for the title of the app
title_label = tkinter.Label(top, text='welcome to the chat room app!', font=('calibre',20,'bold'),justify=CENTER)
title_label.config(bg='#BACC81',fg='#FFFCF7')
title_label.grid(row=0,column=0,pady=15)

#creating a label for username using widget Label
username_label = tkinter.Label(top, text = 'username', font=('calibre',10, 'bold'))
username_label.config(bg="#D2BF55", fg= "#FFF")
username_label.grid(row=1,column=0,pady=10,padx= 250,ipadx=30,sticky=E)

  
#creating an entry for client to input their username using widget Entry
username_entry = tkinter.Entry(top,textvariable = my_username, font=('calibre',10,'normal'),width=23)
username_entry.config(bg='#FFFCF7')
username_entry.grid(row=1,column=0,pady=10,padx=20,ipadx=30,sticky=E)

#creating a scrollbar frame for the messages to be viewed
scrollbar = tkinter.Scrollbar(messages_frame) 
msg_list = tkinter.Listbox(messages_frame, height=20, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.grid(row=2,column=0,padx=20)


#creating an entry field for user to input their message
entry_field = tkinter.Entry(top, textvariable=client_msg, width=87)
entry_field.bind("<Return>", send_msg)
entry_field.config(bg='#FFFCF7')
entry_field.grid(row=3,column=0,pady=20,padx=20,sticky=W)

#creating a send button #uncomment somehting here
send_button = tkinter.Button(top, text="send", width=10, height=1, font=('calibre',10,'bold'), command=send_msg)
send_button.config(bg="#013A20", fg= "#FFFCF7",activeforeground= "#FFF", activebackground="#D2BF55")
send_button.grid(row=3,column=0,pady=20,padx=20,sticky=E)

#using a protocol to handle window close event
top.protocol("WM_DELETE_WINDOW", close_window)

#creating socket with given AWS parameters
HOST = "127.0.0.1"
PORT = 1236
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

#creating the client socket
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#getting the number of rooms available on the server and generating a drop down menu
first_msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
#setting num of rooms to the server's response
num_rooms = int(first_msg)

#setting the name for each chat room
selected_room = tkinter.StringVar(top)
selected_room.set("chat rooms")
rooms_list = []  #array of the current chatrooms
for i in range(num_rooms):  #for loop to iterate over all the rooms in the array 
    rooms_list.append("chat room " + str(i + 1))

#creating an option menu listing the chat rooms that are currently available
chat_rooms = tkinter.OptionMenu(top, selected_room, *rooms_list)
chat_rooms.config(bg="#D2BF55", fg= "#FFF",activeforeground= "#FFFCF7", activebackground="#013A20",font=('calibre',10,'bold'))
chat_rooms.grid(row=1,column=0,pady=20, padx=20,sticky=W)
#creating a button to allow client to switch rooms
change_button = tkinter.Button(top, text="switch room",font=('calibre',10,'bold'),bg="#D2BF55", fg= "#FFF",activeforeground= "#FFFCF7", activebackground="#013A20", command=switch_room)
change_button.grid(row=1,column=0,pady=20, padx=150, sticky=W)

#threading
receive_thread = Thread(target=receive_msg)
receive_thread.start()
#set resizale to false so user will not be able to resize the window
top.resizable(width=False, height=False)   
#configuring the background colour
top.config(bg='#BACC81')
tkinter.mainloop()
