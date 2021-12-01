import tkinter
from tkinter.constants import CENTER, LEFT, RIGHT


#create a GUI app using tkinter
top = tkinter.Tk()
top.geometry("1000x700")
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

# creating a label for
# name using widget Label
#ameena makeeeee it to the centerrrrrr
name_label = tkinter.Label(top, text = 'Username', font=('calibre',10, 'bold'))
name_label.grid(row=0,column=0)
#name_label.place(x=25, y=25, anchor="center")
  
# creating a entry for input
# name using widget Entry
name_entry = tkinter.Entry(top,textvariable = my_username, font=('calibre',10,'normal'))
name_entry.grid(row=0,column=1)




# username_label = tkinter.Label(top,text="Enter username: ", )
# username_label.pack(side=LEFT)
# username_field = tkinter.Entry(top,bd=5,textvariable=my_username)
# username_field.pack()#side= RIGHT)

# #adding a scroll bar to the chat frame, to view messages
# scrollbar = tkinter.Scrollbar(messages_frame)  

# #text message conatiner
# msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
# scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
# msg_list.pack()
# messages_frame.pack()


# message_label = tkinter.Label(top, text="Enter message: ")
# message_label.pack()
# entry_field = tkinter.Entry(top, textvariable=my_msg, width=50)
# #entry_field.bind("<Return>", send)
# entry_field.pack()
#send_button = tkinter.Button(top, text="Send", command=send)
#send_button.pack()

#top.resizable(width=False, height=False)    # The client can't resize the window.
top.config(bg='#738290')
tkinter.mainloop()
