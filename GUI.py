#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json

import pickle
import tkinter.messagebox as msgb
from encrypt_decrypt import *
from encode_decode import *
#==============================================================================
# Client_keys class for storing every client's public/private rsa key
# Secret_message class for storing every client's sended secret message
# Both can only be accessed from specific client side
#==============================================================================
class Client_keys:
    def __init__(self,public_key,private_key):
        self.public_rsa_key=public_key
        self.private_rsa_key=private_key
class Secret_message:
    def __init__(self,to_name,msg):
        self.to_name=to_name
        self.msg=msg
# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # Create login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        # create a username Label
        self.username = StringVar() 
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
        # Create password label
        self.password = StringVar() 
        self.labelPassword = Label(self.login,
                               text = "Password: ",
                               font = "Helvetica 12")
          
        self.labelPassword.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.4)
        # create entry boxes for name and password
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14",textvariable=self.username)
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
       
        self.entryPassword = Entry(self.login, 
                             font = "Helvetica 14",textvariable=self.password)
          
        self.entryPassword.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.4)

        # set the focus of the curser

        self.entryName.focus()
        
        #My code: create login button and sign
        self.login_button = Button(self.login,
                                   text="Log In",
                                   font="Helvetica 14",
                                   command=self.log_in)

        self.login_button.place(relwidth=0.2,
                                relheight=0.1,
                                relx=0.4,
                                rely=0.55)

        self.sign_button = Button(self.login,
                                  text="Sign Up",
                                  font="Helvetica 14",
                                  command=self.sign_up)

        self.sign_button.place(relwidth=0.2,
                               relheight=0.1,
                               relx=0.4,
                               rely=0.65)
        #End of my code
        self.Window.mainloop()
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.55)
        

        
    #我的代码
    def send_secure_message(self):
        def send_secret_message():
            to_name=self.to_username.get()
            msg=self.secret_msg.get()
            # Ask the server for the target receiver's public rsa key
            self.send(json.dumps({"action":"client_request_rsa_key","to_name":to_name}))
            # Record secret message in file(only accessible in client side)
            file=open("secure_messages.txt","rb")
            dict_secret_messages=pickle.load(file)
            file.close()
            temp=Secret_message(to_name,msg)
            if  not self.log_in_username in dict_secret_messages.keys():
                dict_secret_messages[self.log_in_username]=[temp]
            else:
                dict_secret_messages[self.log_in_username].append(temp)
            file=open("secure_messages.txt","wb")
            pickle.dump(dict_secret_messages,file)
            file.close()
            self.window_secure_message.destroy()

        self.window_secure_message= Toplevel()
        self.window_secure_message.title("Send secure message")
        self.window_secure_message.configure(width=400,
                                      height=300)
        
        self.to_username = StringVar()

        self.label_to_username = Label(self.window_secure_message,
                                        text="To Username ",
                                        font="Helvetica 12")

        self.label_to_username.place(relheight=0.15,
                                      relx=0.2,
                                      rely=0.1)

        self.entry_to_username = Entry(self.window_secure_message,
                                    font="Helvetica 12",
                                    textvariable=self.to_username)

        self.entry_to_username.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.45,
                                  rely=0.1)
        self.secret_msg = StringVar()
        self.label_secret_msg = Label(self.window_secure_message,
                                        text="Message",
                                        font="Helvetica 12")

        self.label_secret_msg.place(relheight=0.15,
                                      relx=0.2,
                                      rely=0.25)

        self.entry_secret_msg = Entry(self.window_secure_message,
                                        font="Helvetica 12",
                                        show="*",
                                        textvariable=self.secret_msg)

        self.entry_secret_msg.place(relwidth=0.4,
                                      relheight=0.1,
                                      relx=0.45,
                                      rely=0.25)
        
        self.send_secret_msg_button = Button(self.window_secure_message,
                                    text="Send secret message",
                                    font="Helvetica 12",
                                    command=send_secret_message)

        self.send_secret_msg_button.place(relx=0.35,
                                 rely=0.65)

        self.window_secure_message.bind('<Return>', lambda event: send_secret_message())

    def sign_up(self):
        def sign_up():
            new_user = self.new_username.get()
            new_pwd = self.new_password.get()
            again_pwd = self.confirm_password.get()

            with open("all_users.pickle", "rb") as users_file:
                all_user = pickle.load(users_file)
                if new_user in all_user:
                    msgb.showerror(message="Username already exists.")
                else:
                    if new_pwd == again_pwd:
                        msgb.showinfo(message="Signup succeeded!")
                        all_user[new_user] = new_pwd
                        with open("all_users.pickle", "wb") as users_file:
                            pickle.dump(all_user, users_file)
                        self.window_sign_up.destroy()
                        self.goAhead(new_user)
                    else:
                        msgb.showerror(message="Please confirm your password again.")

        self.window_sign_up = Toplevel(self.login)
        self.window_sign_up.title("Signup")
        self.window_sign_up.configure(width=400,
                                      height=300)
        
        # new username label and entry
        self.new_username = StringVar()

        self.label_new_username = Label(self.window_sign_up,
                                        text="Username ",
                                        font="Helvetica 12")

        self.label_new_username.place(relheight=0.15,
                                      relx=0.2,
                                      rely=0.1)

        self.entry_username = Entry(self.window_sign_up,
                                    font="Helvetica 12",
                                    textvariable=self.new_username)

        self.entry_username.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.45,
                                  rely=0.1)

        # new password label and entry
        self.new_password = StringVar()

        self.label_new_password = Label(self.window_sign_up,
                                        text="Password ",
                                        font="Helvetica 12")

        self.label_new_password.place(relheight=0.15,
                                      relx=0.2,
                                      rely=0.25)

        self.entry_new_password = Entry(self.window_sign_up,
                                        font="Helvetica 12",
                                        show="*",
                                        textvariable=self.new_password)

        self.entry_new_password.place(relwidth=0.4,
                                      relheight=0.1,
                                      relx=0.45,
                                      rely=0.25)
        # confirm password label and entry
        self.confirm_password = StringVar()

        self.label_confirm_password = Label(self.window_sign_up,
                                            text="Password Again ",
                                            font="Helvetica 12")

        self.label_confirm_password.place(relheight=0.15,
                                          relx=0.1,
                                          rely=0.4
                                          )

        self.entry_password = Entry(self.window_sign_up,
                                    font="Helvetica 12",
                                    show="*",
                                    textvariable=self.confirm_password)

        self.entry_password.place(relwidth=0.4,
                                  relheight=0.1,
                                  relx=0.45,
                                  rely=0.4)

        # create a signup button
        self.signup_button = Button(self.window_sign_up,
                                    text="Sign up",
                                    font="Helvetica 12",
                                    command=sign_up)

        self.signup_button.place(relx=0.35,
                                 rely=0.65)

        self.window_sign_up.bind('<Return>', lambda event: sign_up())
        
    def log_in(self):
        self.log_in_username = self.username.get()
        self.log_in_password = self.password.get()

        self.users_file = open("all_users.pickle", "rb")
        self.all_users = pickle.load(self.users_file)
        self.users_file.close()

        if self.log_in_username in self.all_users:
            if self.log_in_password == self.all_users[self.log_in_username]:
                msgb.showinfo(message="Welcome, " + self.log_in_username + "!")
                self.login.destroy()
                self.goAhead(self.log_in_username)
            else:
                msgb.showerror(message="Password isn't correct! Please try again.")
        else:
            msgb.showerror(message="Username doesn't exist. Please sign up first.")

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                #Generate client's public/private rsa keys 
                public_rsa_key,private_rsa_key=rsa.newkeys(2048)
                client=Client_keys(public_rsa_key,private_rsa_key)
                #Record client's pair of rsa keys in file
                file=open("client_rsa_keys.txt","rb")
                client_keys=pickle.load(file)
                file.close()
                client_keys[name]=client
                file=open("client_rsa_keys.txt","wb")
                pickle.dump(client_keys,file)
                file.close()
                #Send client's public rsa key to the server for storage
                self.send(json.dumps({"action":"client_send_rsa_key","client_rsa_key":encode_rsa_key(public_rsa_key)}))
                

                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
    
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 800,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.6,
                            relheight = 0.05,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.62,
                             rely = 0.008,
                             relheight = 0.03, 
                             relwidth = 0.10)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
        #create a send secure message button
        self.send_secure_message_button = Button(self.labelBottom,
                                    text="Send secure\n message",
                                    font = "Helvetica 8 bold", 
                                    width = 20,
                                    bg = "#ABB2B9",
                                    command=self.send_secure_message)

        self.send_secure_message_button.place(relx = 0.62,
                             rely = 0.038,
                             relheight = 0.03, 
                             relwidth = 0.10)
        #我的代码
        self.command_frame = Frame(self.Window, bg="#ABB2B9")
        self.command_frame.place(relwidth=0.3, relheight=1, relx=0.72)  # 右侧区域

        self.time_button = Button(self.command_frame, text="Get Time", font="Helvetica 12",command=self.get_time)
        self.time_button.pack(pady=5)

        self.who_button = Button(self.command_frame, text="See Who else is here", font="Helvetica 12",command=self.who_else)
        self.who_button.pack(pady=5)

        self.connect_label = Label(self.command_frame, text="Type in the peer to connect", bg="#ABB2B9", font="Helvetica 12")
        self.connect_label.pack(pady=5)
        self.connect_entry = Entry(self.command_frame, font="Helvetica 12")
        self.connect_entry.pack(pady=8)
        self.connect_button = Button(self.command_frame, text="Connect", font="Helvetica 12",command=self.connect)
        self.connect_button.pack(pady=5)

        self.search_label = Label(self.command_frame, text="Type in a term to search", bg="#ABB2B9", font="Helvetica 12")
        self.search_label.pack(pady=5)
        self.search_entry = Entry(self.command_frame, font="Helvetica 12")
        self.search_entry.pack(pady=8)
        self.search_button = Button(self.command_frame, text="Search", font="Helvetica 12",command=self.search_log)
        self.search_button.pack(pady=5)

        self.sonnet_label = Label(self.command_frame, text="Type in a number to get a poem", bg="#ABB2B9", font="Helvetica 12")
        self.sonnet_label.pack(pady=5)
        self.sonnet_entry = Entry(self.command_frame, font="Helvetica 12")
        self.sonnet_entry.pack(pady=8)
        self.sonnet_button = Button(self.command_frame, text="Get a sonnet poem", font="Helvetica 12",command=self.get_sonnet)
        self.sonnet_button.pack(pady=5)

        self.bye_button = Button(self.command_frame, text="Quit chatting", font="Helvetica 12",command=self.bye)
        self.bye_button.pack(pady=5)

        self.quit_button = Button(self.command_frame, text="Quit chat system", font="Helvetica 12",command=self.quit)
        self.quit_button.pack(pady=5)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
    def get_time(self):
        self.my_msg="time"
    def who_else(self):
        self.my_msg="who"
    def connect(self):
        peer=self.connect_entry.get()
        self.my_msg="c "+peer
        self.connect_entry.delete(0, END)
    def search_log(self):
        term = self.search_entry.get()
        self.my_msg="?"+term
        self.search_entry.delete(0, END)
    def get_sonnet(self):
        number = self.sonnet_entry.get()
        print(number)
        self.my_msg="p"+number
        self.sonnet_entry.delete(0, END)
    def quit(self):
        self.my_msg="q"
    def bye(self):
        self.my_msg="bye"   
    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()
