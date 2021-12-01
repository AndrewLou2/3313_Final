import tkinter

#create a GUI app using tkinter
top = tkinter.Tk()

#add a title to the app
top.title("Chat Messenger App")

#adding a frame to the top
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
my_username = tkinter.StringVar()
my_username.set("")

scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
# Messages container.
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
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
#entry_field.bind("<Return>", send)
entry_field.pack()
#send_button = tkinter.Button(top, text="Send", command=send)
#send_button.pack()

#top.resizable(width=False, height=False)    # The client can't resize the window.
top.config(bg='#738290')
tkinter.mainloop()
