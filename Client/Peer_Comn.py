import socket
import threading
import pickle
import time
import tkinter as tk
from tkinter import messagebox
import os
from PIL import ImageGrab,Image,ImageTk
import client_gui
import sys
import win32api
import pyautogui
import lz4.frame

pyautogui.FAILSAFE=False

#gui part

class gui:
    def __init__(self):
        self.root=tk.Tk()
        #------------------------------------------------------------
        self.connect_frame=tk.Frame(self.root)
        self.connect_frame.pack()

        self.connect_label=tk.Label(self.connect_frame,text='Connected To: None')
        self.connect_label.pack()

        self.connect_button = tk.Button(self.connect_frame, text="Connect", command=self.connect_to_welcome)
        self.connect_button.pack()
        #-------------------------------------------------------------
        self.welcome_frame=tk.Frame(self.root)
        self.welcome_frame.forget()

        self.choice_reg_button = tk.Button(self.welcome_frame, text="register", command=self.welcome_to_register_frame)
        self.choice_reg_button.pack()

        self.choice_login_button = tk.Button(self.welcome_frame, text="Login", command=self.welcome_to_login_frame)
        self.choice_login_button.pack()
        #-------------------------------------------------------------------
        self.register_frame=tk.Frame(self.root)
        self.register_frame.forget()

        self.register_username_label = tk.Label(self.register_frame, text="Userid:")
        self.register_username_label.pack()

        self.register_username_entry = tk.Entry(self.register_frame)
        self.register_username_entry.pack()

        self.register_password_label = tk.Label(self.register_frame, text="Password:")
        self.register_password_label.pack()

        self.register_password_entry = tk.Entry(self.register_frame, show="*")  # Show asterisks for password
        self.register_password_entry.pack()

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.pack()

        self.register_to_login_button = tk.Button(self.register_frame, text="ToLogin", command=self.register_to_login_frame)
        self.register_to_login_button.pack()
        #----------------------------------------------------------------------
        self.login_frame=tk.Frame(self.root)
        self.login_frame.forget()

        self.login_username_label = tk.Label(self.login_frame, text="Userid:")
        self.login_username_label.pack()

        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.pack()

        self.login_password_label = tk.Label(self.login_frame, text="Password:")
        self.login_password_label.pack()

        self.login_password_entry = tk.Entry(self.login_frame, show="*")  # Show asterisks for password
        self.login_password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.get_login_information)
        self.login_button.pack()

        self.login_to_register_button = tk.Button(self.login_frame, text="ToRegister", command=self.login_to_register_frame)
        self.login_to_register_button.pack()
        #-----------------------------------------------------------
        self.rooms_frame=tk.Frame(self.root)
        self.rooms_frame.forget()

        self.enter_room_label = tk.Label(self.rooms_frame, text="enter room password:")
        self.enter_room_label.pack()

        self.enter_room_entry = tk.Entry(self.rooms_frame)
        self.enter_room_entry.pack()

        #self.enter_room_button = tk.Button(self.rooms_frame, text="enter room", command=self.enter_room)
        #self.enter_room_button.pack()

        #self.create_room_button = tk.Button(self.rooms_frame, text="create room", command=self.create_room)
        #self.create_room_button.pack()

        #-----------------------------------------------------------
        self.screen_frame=tk.Frame(self.root)
        self.screen_canvas=tk.Canvas(self.screen_frame, bg='green')
        self.screen_image=self.screen_canvas.create_image(self.screen_canvas.winfo_reqwidth() / 2, self.screen_canvas.winfo_reqheight() / 2, image=None, anchor='center')
        self.screen_frame.pack(fill='both', expand=True)
        self.screen_frame.forget()

        self.screen_canvas.pack(fill='both', expand=True)
        self.screen_canvas.bind('<Configure>', self.screen_frame_resize)
        self.received_screen : Image.Image = ImageGrab.grab()


    def welcome_to_register_frame(self):
        self.register_frame.pack()
        self.welcome_frame.forget()

    def welcome_to_login_frame(self):
        self.login_frame.pack()
        self.welcome_frame.forget()

    def register_to_login_frame(self):
        self.login_frame.pack()
        self.register_frame.forget()

    def login_to_register_frame(self):
        self.register_frame.pack()
        self.login_frame.forget()

    def login_to_screen_share(self):
        self.screen_frame.pack(fill='both', expand=True)
        self.login_frame.forget()

    def connect_to_welcome(self):
        self.welcome_frame.pack()
        self.connect_frame.forget()

    def login_to_rooms_frame(self):
        self.rooms_frame.pack()
        self.login_frame.forget()




    #register/login handling------------------------------------





    #screen share handling------------------------------------------
    def screen_frame_resize(self, event : tk.Event):
        display= self.received_screen

        display.thumbnail((event.width, event.height))

        display_img = ImageTk.PhotoImage(display)

        self.actual_screenShare_size=(display_img.width(),display_img.height())

        new_width = event.width - display_img.width()
        new_height = event.height - display_img.height()

        event.widget.itemconfigure(self.screen_image, image=display_img)
        event.widget.moveto(self.screen_image, new_width / 2, new_height / 2)

        event.widget.image = display_img
        self.root.update()
    def update_screen(self,img):

        if img is None:
            display= self.received_screen
        else:
            display=img
            self.received_screen=img

        display.thumbnail((self.screen_canvas.winfo_width(), self.screen_canvas.winfo_height()))

        display_img = ImageTk.PhotoImage(display)

        new_width = self.screen_canvas.winfo_width() - display_img.width()
        new_height = self.screen_canvas.winfo_height() - display_img.height()

        self.screen_canvas.itemconfigure(self.screen_image, image=display_img)
        self.screen_canvas.moveto(self.screen_image, new_width / 2, new_height / 2)

        self.screen_canvas.image = display_img
        self.root.update()
    def receive_screen(self,screen):
        self.update_screen(screen)
    def start(self):
        self.root.mainloop()


#function that ensures all data received ---> returns all data

def recv_all(conn : socket.socket):
    data=b''
    pck_sz= conn.recv(8)
    size=int.from_bytes(pck_sz,sys.byteorder)
    while len(data)<size:
        data=data+conn.recv(size-len(data))
        if len(data)==size:
            break
    return data

#functions to handle closing and activating threads


thread_event_array : dict[threading.Thread.ident,threading.Event] = {}


def thread_event_setter(thread_id : threading.Thread.ident):
    thread_event_array.update({thread_id : threading.Event()})

def thread_event_remove(thread_id: threading.Thread.ident):
    thread_event_array.pop(thread_id)
def thread_closer(thread_id : threading.Thread.ident):
    thread_event_array[thread_id].set()
def end_all_threads():
    for thread in thread_event_array:
        thread_event_array[thread].set()

def delete_all_thread_flags():
    thread_event_array.clear()

def check_thread_flag(thread_id):
    if thread_id in thread_event_array and thread_event_array[thread_id].is_set():
        return True
    else:
        return False

#----------------------------------------------------------

class unknown_client:
    def __init__(self,host,port):
        self.host=host
        self.port=port

        self.window=gui()

    def connect_to_server(self, server_address, server_port):
        try:
            connection = socket.create_connection((server_address, server_port))
            self.server = connection
            print(f"Connected to {server_address} : {server_port}")

            receive_from_server_thread=threading.Thread(target=self.receive_from_server)
            receive_from_server_thread.start()

            return 'w'
        except socket.error as err:
            ans = messagebox.showerror('failed connection to server', f'{err}\n want to try again?',type=messagebox.RETRYCANCEL)
            if ans == messagebox.RETRY:
                self.connect_to_server(server_address, server_port)
            else:
                return 'f'

    def handling_login(self):
        username = self.window.login_username_entry.get()
        password = self.window.login_password_entry.get()
        data = f'l~{username}~{password}'
        try:
            self.server.sendall(data.encode())
        except socket.error as error:
            self.server.close()
            messagebox.showerror('failed communication with server', f'{error}')

    def handling_register(self):
        username = self.window.register_username_entry.get()
        password = self.window.register_password_entry.get()
        data = f'r~{username}~{password}'
        try:
            self.server.sendall(data.encode())
        except socket.error as error:
            self.server.close()
            messagebox.showerror('failed communication with server', f'{error}')

    def receive_from_server(self):
        while True:
            try:
                received=recv_all(self.server)

                answer=received.decode()

            except socket.error as error:
                self.server.close()
                messagebox.showerror('failed communication with server', f'{error}')
                break




class Controlling:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_to=None
        self.send_to=None
        self.window=gui()
        self.window.screen_canvas.focus_set()
        self.window.screen_canvas.bind('<Key>', self.send_keyboard)
        self.window.screen_canvas.bind('<Button>',self.send_mouse)
        self.window.screen_canvas.bind('<ButtonRelease>',self.send_mouse)
        self.window.root.protocol('WM_DELETE_WINDOW',self.tk_close)




    # function for handling tkinter window closing
    def tk_close(self):
        end_all_threads()
        print('tk close')
        self.window.root.destroy()


    def connect(self,peer_host, peer_port):
        try:
            connection=socket.create_connection((peer_host,peer_port))
            self.send_to=connection
            print(f"Connected to {peer_host} : {peer_port}")

            #sending_thread=threading.Thread(target=self.send_data, daemon=True)
            #sending_thread.start()
            return
        except socket.error as e:
            print(f"Failed to connect to {peer_host} : {peer_port} - Error: {e}")
            return

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host} : {self.port}")

        while True:

            if check_thread_flag(threading.get_ident()):
                self.socket.close()
                thread_event_remove(threading.get_ident())
                break

            connection, address = self.socket.accept()
            self.listen_to=connection

            print(f"Accepted connection from {address}")

            receive_thread=threading.Thread(target=self.receive_data, args=(self.listen_to, address))
            receive_thread.start()
            thread_event_setter(receive_thread.ident)
            break
        #self.connect('10.0.0.9',9998)

    def send_keyboard(self, event):
        keyboard_keycode = event.keycode
        keyboard_scancode = win32api.MapVirtualKey(keyboard_keycode, 4)

        data = f'k~{keyboard_keycode}~{keyboard_scancode}'
        msg_to_send=data.encode()
        msg_len=len(msg_to_send)
        #data = input('send: ')
        try:
            self.send_to.sendall(msg_len.to_bytes(8,sys.byteorder)+msg_to_send)
        except socket.error as e:
            print(f"Failed to send data - Error: {e}")
            self.send_to.close()

    def send_mouse(self,event):
        data=''
        msg_to_send=b''
        msg_len = 0
        match int(event.type):
            case 4:  #mouse-down
                data=f'm~d~{event.num}~{event.x}~{event.y}~{self.window.actual_screenShare_size[0]}~{self.window.actual_screenShare_size[1]}'
                msg_to_send=data.encode()
                msg_len=len(msg_to_send)
            case 5: #mouse-up
                data=f'm~u~{event.num}~{event.x}~{event.y}~{self.window.actual_screenShare_size[0]}~{self.window.actual_screenShare_size[1]}'
                msg_to_send = data.encode()
                msg_len = len(msg_to_send)
        try:
            self.send_to.sendall(msg_len.to_bytes(8,sys.byteorder)+msg_to_send)
        except socket.error as e:
            print(f"Failed to send data - Error: {e}")
            self.send_to.close()

    def receive_data(self, connection, address):
        while True:
            if check_thread_flag(threading.get_ident()):
                connection.close()
                break

            try:
                data=recv_all(connection)

                decompressed_data=lz4.frame.decompress(data)

                img=pickle.loads(decompressed_data)

                self.window.receive_screen(img)


            except socket.error as err:
                print(err)
                connection.close()
                break
        print(f"Connection from {address} closed")
        self.listen_to.close()
    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()
        thread_event_setter(listen_thread.ident)
        self.window.start()


#need to apply thread closing handling to the Controled Class!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Controlled:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_to=None
        self.send_to=None
        self.connected_to=None
        self.controlled_screen_width=win32api.GetSystemMetrics(0)
        self.controlled_screen_height=win32api.GetSystemMetrics(1)
    def connect(self,peer_host, peer_port):
        try:
            connection=socket.create_connection((peer_host,peer_port))
            self.send_to=connection
            print(f"Connected to {peer_host} : {peer_port}")

            sending_thread=threading.Thread(target=self.send_data)
            sending_thread.start()
            thread_event_setter(sending_thread.ident)
            return
        except socket.error as e:
            print(f"Failed to connect to {peer_host} : {peer_port} - Error: {e}")
            return

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host} : {self.port}")

        while True:
            if thread_event_array[threading.get_ident()].is_set():
                break

            connection, address = self.socket.accept()
            self.listen_to=connection

            print(f"Accepted connection from {address}")




            receive_thread=threading.Thread(target=self.receive_data, args=(self.listen_to, address))
            receive_thread.start()
            thread_event_setter(receive_thread.ident)

    def send_data(self):
        while True:
            if thread_event_array[threading.get_ident()].is_set():
                break

            try:
                screen_grab=ImageGrab.grab()

                data=pickle.dumps(screen_grab)
                compressed_data=lz4.frame.compress(data)
                msg_length=len(compressed_data)

                self.send_to.sendall(msg_length.to_bytes(8,sys.byteorder)+compressed_data)

            except socket.error as err:
                print(err)
                self.send_to.close()
                break
        return
    def receive_data(self, connection, address):
        while True:
            if thread_event_array[threading.get_ident()].is_set():
                break
            try:
                recv_data=recv_all(connection)
                decoded_data=recv_data.decode()
                data=decoded_data.split('~')
                if data[0]=='k':
                    keycode=int(data[1])
                    scancode=int(data[2])
                    win32api.keybd_event(keycode,scancode)
                elif data[0]=='m':
                    recv_x=int(data[3])
                    recv_y=int(data[4])
                    retio_x=self.controlled_screen_width/int(data[5])
                    ratio_y=self.controlled_screen_height/int(data[6])

                    x=round(recv_x*retio_x)
                    y=round(recv_y*ratio_y)

                    if data[1]=='d':
                        match int(data[2]):
                            case 1:
                                pyautogui.mouseDown(button='left',x=x,y=y)#left
                            case 3:
                                pyautogui.mouseDown(button='right',x=x,y=y)#right
                    elif data[1]=='u':
                        match int(data[2]):
                            case 1:
                                pyautogui.mouseUp(button='left',x=x,y=y)#left
                            case 3:
                                pyautogui.mouseUp(button='right',x=x,y=y)#right

            except socket.error:
                break
        print(f"Connection from {address} closed")
        self.listen_to.close()
    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()
        thread_event_setter(listen_thread.ident)

#if __name__ == "__main__":
    '''host, port = input('enter host:port for new peer -> ').split(':')
    node = Peer(host, int(port))
    node.start()
    # Give some time for nodes to start listening
    import time
    time.sleep(2)
    con_host, con_port = input('enter host:port to connect to -> ').split(':')
    node.connect(con_host, int(con_port))'''

ans=input('peer mode: ')
if ans == 'cing':
    c=Controlling('10.0.0.9',9999)
    c.start()

elif ans == 'cd':
    cd=Controlled('10.0.0.9',9998)
    cd.start()
    time.sleep(1)
    cd.connect('10.0.0.9',9999)