import win32api
import pickle
import lz4.frame
from client_gui import *

from general_important_functions import *


class Controlling:
    def __init__(self, host,port, gui_obj : gui):
        self.host=host
        self.port=port

        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_to=None
        self.send_to=None
        self.window=gui_obj
        self.window.screen_canvas.focus_set()
        self.window.screen_canvas.bind('<Key>', self.send_keyboard)
        self.window.screen_canvas.bind('<Button>',self.send_mouse)
        self.window.screen_canvas.bind('<ButtonRelease>',self.send_mouse)
        self.window.root.protocol('WM_DELETE_WINDOW',self.tk_close)


    def connect(self,peer_host, peer_port):
        try:
            connection=socket.create_connection((peer_host,peer_port))
            self.send_to=connection
            print(f"Connected to {peer_host} : {peer_port}")

            if self.listen_to is None:
                msg = (self.host,self.port)

                send_all(self.send_to,msg)

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

            if self.send_to is None:
                peer_address, peer_port = recv_all(self.listen_to)
                self.connect(peer_address,peer_port)

            print(f"Accepted connection from {address}")

            receive_thread=threading.Thread(target=self.receive_data, args=(self.listen_to, address))
            receive_thread.start()
            thread_event_setter(receive_thread.ident)
            break
        #self.connect('10.0.0.9',9998)

    def send_keyboard(self, event):
        keyboard_keycode = event.keycode
        keyboard_scancode = win32api.MapVirtualKey(keyboard_keycode, 4)

        data = ['k',keyboard_keycode,keyboard_scancode]
        try:
            send_all(self.send_to,data)
        except socket.error as e:
            print(f"Failed to send data - Error: {e}")
            self.send_to.close()

    def send_mouse(self,event):
        data=''
        match int(event.type):
            case 4:  #mouse-down
                data=['m','d',event.num,event.x,event.y,self.window.actual_screenShare_size[0],self.window.actual_screenShare_size[1]]

            case 5: #mouse-up
                data=['m','u',event.num,event.x,event.y,self.window.actual_screenShare_size[0],self.window.actual_screenShare_size[1]]
        try:
            send_all(self.send_to,data)
        except socket.error as e:
            print(f"Failed to send data - Error: {e}")
            self.send_to.close()

    def receive_data(self, connection, address):
        while True:
            if check_thread_flag(threading.get_ident()):
                connection.close()
                thread_event_remove(threading.get_ident())
                break

            try:
                img=recv_all(connection)

                self.window.receive_screen(img)


            except socket.error as err:
                print(err)
                connection.close()
                break
        print(f"Connection from {address} closed")
        self.listen_to.close()

    def __del__(self):
        end_all_threads()
        self.end_sockets()
        self.window.root.destroy()

    # function for handling tkinter window closing
    def tk_close(self):
        self.__del__()
        print('tk close')

    def end_sockets(self):
        self.socket.close()
        if self.listen_to is not None:
            self.listen_to.close()
        if self.send_to is not None:
            self.send_to.close()


    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()
        thread_event_setter(listen_thread.ident)