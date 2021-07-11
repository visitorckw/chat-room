import socket
import threading
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL

IP = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
client.connect((IP, PORT))

name = 'visitor'

window1 = tk.Tk()
window1.title('聊天室 login')
window1.geometry('300x300')
window1.resizable(height = False, width = False)
text1 = tk.Label(window1, text='username')
text1.place(x=10, y=100, height=30, width=70)
entry = tk.Entry(window1)
entry.place(x=80, y=100, height=30, width=200)

def login(event):
    print(event)
    if event and event.char != '\r':
        return
    global name
    name = entry.get() + ': '
    window1.destroy()

entry.bind('<Key>', login)
entry.focus()
btn = tk.Button(window1, text = 'login', command = lambda: login(None))
btn.place(x=200, y=170, height = 40, width = 70)
window1.mainloop()

window2 = tk.Tk()
window2.title('聊天室 - ' + name)
window2.geometry('400x500')
window2.resizable(False, False)
box = tk.Text(window2, padx=5, pady=5)
box.place(relheight=0.78, relwidth=0.94, relx=0.03, rely=0.03)
box.configure(state=DISABLED)
scroll = tk.Scrollbar(box, command=box.yview)
scroll.pack(side="right", fill="y")
lbl = tk.Label(window2, padx=1, pady=1)
lbl.place(relheight=0.09, relwidth = 0.9,relx=0.05, rely=0.9)

def sendMsg(event):
    if event and event.char != '\r':
        return
    msg = entry.get()
    if len(msg) == 0:
        return
    msg = name + msg
    client.send(msg.encode())
    entry.delete(0, 'end')
def recvMsg():
    while True:
        try:
            global box
            msg = client.recv(1024).decode()
            box.config(state = NORMAL)
            box.insert('end', msg + '\n')
            box.config(state=DISABLED)
            box.see('end')
            print(msg)
        except:
            print('server error')
            client.close()
            return

entry = tk.Entry(lbl)
entry.place(relheight=1, relwidth=0.78, x=0.2, y=0.2)
entry.bind('<Key>', sendMsg)
entry.focus()
btn = tk.Button(lbl, text = 'send', command = lambda : sendMsg(None))
btn.place(relheight=1, relwidth=0.18, relx=0.8, y=0.2)

t = threading.Thread(target=recvMsg)
t.start()

window2.mainloop()
