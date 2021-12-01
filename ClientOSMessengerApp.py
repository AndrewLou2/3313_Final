# SE 3313A Project - Ali Malik, Ali Chouman, Yazan Al-Lahham, Andrei Popescu
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


# This function must be threaded.
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            msg_list.see(tkinter.END)
        except OSError:
            break


def send(event=None):  # Binders pass the event.
    msg = my_msg.get()
    my_msg.set("")      # Clears text field.
    global current_room
    if msg == "{quit}":
        client_socket.send(
            bytes(my_username.get() + " has closed OS Messenger App!", "utf8"))
        client_socket.close()
        top.quit()
        return
    client_socket.send(bytes(my_username.get() + ": " + msg, "utf8"))


# Send quit message to the server.
def on_closing(event=None):
    # Send server quit message.
    my_msg.set("{quit}")
    send()


def change_room():
    global current_room
    current_room = ((chatRoomSelected.get()).split(' '))[2]
    client_socket.send(bytes("/" + current_room, "utf8"))
    msg_list.delete(0, tkinter.END)
    msg_list.insert(tkinter.END, "You are now in room " + str(current_room))
    msg_list.see(tkinter.END)


# Global variables.
number_of_rooms = 0
current_room = 0

top = tkinter.Tk()
top.title("OS Messenger App")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
my_username = tkinter.StringVar()
my_username.set("")

# To see through previous messages.
scrollbar = tkinter.Scrollbar(messages_frame)
# Messages container.
msg_list = tkinter.Listbox(messages_frame, height=30,
                           width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

username_label = tkinter.Label(top, text="Enter username: ")
username_label.pack()
username_field = tkinter.Entry(top, textvariable=my_username)
username_field.pack()

message_label = tkinter.Label(top, text="Enter message: ")
message_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg, width=50)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)

# Socket with given AWS parameters.
HOST = "127.0.0.1"
PORT = 1236
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Server response of number of rooms available and generate drop down list.
first_msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
number_of_rooms = int(first_msg)
chatRoomSelected = tkinter.StringVar(top)
chatRoomSelected.set("List Of Chat Rooms")
rooms_list = []
for i in range(number_of_rooms):
    rooms_list.append("Chat Room " + str(i + 1))

chat_rooms = tkinter.OptionMenu(top, chatRoomSelected, *rooms_list)
chat_rooms.pack()
change_button = tkinter.Button(top, text="Change Room", command=change_room)
change_button.pack()

receive_thread = Thread(target=receive)
receive_thread.start()
# The client can't resize the window.
top.resizable(width=False, height=False)
tkinter.mainloop()
