#!/usr/bin/python
# -*- coding: utf-8 -*-


from Tkinter import *

import threading
from threading import Timer
from imbox import Imbox
from account import *

imbox = None
message_list = []
acc = account()
main = None

class MainWindow:
  
    def __init__(self, parent):
        self.parent = parent        
        self.init_view()

    def init_view(self):
        self.back_container = Frame(self.parent)
        self.back_container.pack(expand=1, fill=BOTH)

        self.top_frame = Frame(self.back_container,borderwidth=5, height=50)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.left_frame = Frame(self.back_container,
                borderwidth=5, height=900, width=200)
        self.left_frame.pack(side=LEFT, fill=BOTH,expand=YES)

        self.right_frame = Frame(self.back_container,
                borderwidth=5, width=500)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        '''top frame'''
        Label(self.top_frame, text='email address:').pack(side=LEFT)
        self.addr_edit = Entry(self.top_frame)
        self.addr_edit.pack(side=LEFT)
        Label(self.top_frame, text='password:').pack(side=LEFT)
        self.passwd_edit = Entry(self.top_frame, show="*")
        self.passwd_edit.pack(side=LEFT)
        Label(self.top_frame, text='server host:').pack(side=LEFT)
        self.server_edit = Entry(self.top_frame)
        self.server_edit.pack(side=LEFT)

        self.ssl_var = IntVar()
        self.ssl_button = Checkbutton(self.top_frame, text='ssl', variable=self.ssl_var)
        self.ssl_button.pack(side=LEFT)

        '''for test'''
        self.recv_button = Button(self.top_frame, text='recv', command=self.onClick)
        self.recv_button.pack(side=RIGHT)

        """left frame"""
        self.maillist = Listbox(self.left_frame)
        self.maillist.pack(fill=BOTH, expand=1)
        self.maillist.bind("<<ListboxSelect>>", self.onSelect)    
        
        """right frame"""
        self.mailview = Text(self.right_frame)
        self.mailview.pack(fill=BOTH, expand=1)

    def onClick(self):
        acc.username = self.addr_edit.get()
        acc.password = self.passwd_edit.get()
        acc.server = self.server_edit.get()
        acc.ssl = self.ssl_var.get()
        recv_thread = threading.Thread(target=fetch, args=(self, 0))
        recv_thread.start()

        
    def onSelect(self, val):
        index = int(self.maillist.curselection()[0])
        self.mailview.delete(1.0, END)
        display = message_list[index]
        self.mailview.insert(END, display, "normal")
      
    def append_message(self, message):
        message_list.append(message)
        self.maillist.insert(END, message.subject)

def fetch(mainwindow, i):
#    imbox = Imbox('mail.eyou.net', username='im@eyou.net', password='Zhanghua528625', ssl=True)
    imbox = Imbox(acc.server, username=acc.username, password=acc.password, ssl=acc.ssl)
    imbox.set_fetch_callback(mainwindow.append_message)
    messages = imbox.messages(sent_from='oypp999@gmail.com')
    for uid, message in messages:
        pass

def main():
    root = Tk()
    main = MainWindow(root)

    #recv_thread = threading.Thread(target=fetch, args=(main, 0))
    #recv_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
