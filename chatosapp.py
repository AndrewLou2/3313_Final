from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.constants import CENTER, E, W


# create a receive function that must be threaded
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            msg_list.see(tkinter.END)
        except OSError:
            break
def send(event=None):  
    msg = my_msg.get()
    my_msg.set("")    

    global current_room
    #if message equals quit, client socket will close
    if msg == "{quit}":
        client_socket.send(bytes(my_username.get() + " has closed Chat App!", "utf8"))
        client_socket.close()
        top.quit()
        return
    client_socket.send(bytes(my_username.get() + ": " + msg, "utf8"))


# when window is closed, the fucntion will send a quit message to the server.
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

# a function to change the room of the client
def change_room():
    global current_room
    current_room = ((chatRoomSelected.get()).split(' '))[2]
    client_socket.send(bytes("/" + current_room, "utf8"))
    msg_list.delete(0, tkinter.END)
    msg_list.insert(tkinter.END, "Room " + str(current_room))
    msg_list.see(tkinter.END)


# setting global variables
number_of_rooms = 0
current_room = 0

#create a GUI app using tkinter
top = tkinter.Tk()

#setting the window size
top.geometry("660x700")

#add a title to the app
top.title("Chat Messenger App")

#adding a frame to the top
messages_frame = tkinter.Frame(top)

#messages to be sent
my_msg = tkinter.StringVar()  

#setting default "" for messages
my_msg.set("")

#username to be set
my_username = tkinter.StringVar()

#setting default "" for username
my_username.set("")

# creating a label for the title of the app
title_label = tkinter.Label(top, text='Welcome to Chat App!', font=('calibre',20,'bold'),justify=CENTER)
title_label.config(bg='#BACC81',fg='#FFFCF7')
title_label.grid(row=0,column=0,pady=15)

# creating a label for username using widget Label
username_label = tkinter.Label(top, text = 'Username', font=('calibre',10, 'bold'))
username_label.config(bg="#D2BF55", fg= "#FFF")
username_label.grid(row=1,column=0,pady=10,padx= 250,ipadx=30,sticky=E)

  
# creating a entry for input username using widget Entry
username_entry = tkinter.Entry(top,textvariable = my_username, font=('calibre',10,'normal'),width=23)
username_entry.config(bg='#FFFCF7')
username_entry.grid(row=1,column=0,pady=10,padx=20,ipadx=30,sticky=E)

# creating a scrollbar frame for the messages to be viewed
scrollbar = tkinter.Scrollbar(messages_frame) 
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.grid(row=2,column=0,padx=20)


# creating an entry field for user to input their message
entry_field = tkinter.Entry(top, textvariable=my_msg, width=87)
entry_field.bind("<Return>", send)
entry_field.config(bg='#FFFCF7')
entry_field.grid(row=3,column=0,pady=20,padx=20,sticky=W)

# creating a send button #uncomment somehting here
send_button = tkinter.Button(top, text="Send", width=10, height=1, font=('calibre',10,'bold'), command=send)
send_button.config(bg="#013A20", fg= "#FFFCF7",activeforeground= "#FFF", activebackground="#D2BF55")
send_button.grid(row=3,column=0,pady=20,padx=20,sticky=E)

# using a protocol to handle window close event
top.protocol("WM_DELETE_WINDOW", on_closing)

# Creating a socket with given AWS parameters
HOST = "35.162.177.130"
PORT = 3005
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

# creating the client socket
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# getting the number of rooms available on the server, and a drop-down menu is generated
first_msg = client_socket.recv(BUFFER_SIZE).decode("utf8")

#setting num of rooms according the server response
number_of_rooms = int(first_msg)

#setting the name for each chat room
chatRoomSelected = tkinter.StringVar(top)
chatRoomSelected.set("Chat Rooms")
rooms_list = []
for i in range(number_of_rooms):
    rooms_list.append("Chat Room " + str(i + 1))

# creating an option menu for the number of rooms that are available
chat_rooms = tkinter.OptionMenu(top, chatRoomSelected, *rooms_list)
chat_rooms.config(bg="#D2BF55", fg= "#FFF",activeforeground= "#FFFCF7", activebackground="#013A20",font=('calibre',10,'bold'))
chat_rooms.grid(row=1,column=0,pady=20, padx=20,sticky=W)

# creating a button to change the room
change_button = tkinter.Button(top, text="Change Room",font=('calibre',10,'bold'),bg="#D2BF55", fg= "#FFF",activeforeground= "#FFFCF7", activebackground="#013A20", command=change_room)
change_button.grid(row=1,column=0,pady=20, padx=150, sticky=W)

#threading
receive_thread = Thread(target=receive)
receive_thread.start()
#set resizale to false so user will not be able to resize the window
top.resizable(width=False, height=False)   
#configuring the background colour
top.config(bg='#BACC81')
tkinter.mainloop()
