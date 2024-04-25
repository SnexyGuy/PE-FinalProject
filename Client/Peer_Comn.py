import pickletools
import socket
import threading
import pickle
import time
import lzma
import socketMassages
from PIL import ImageGrab,Image,ImageTk
import client_gui
import sys
import struct
import win32api
import pyautogui
import lz4.frame

pyautogui.FAILSAFE=False


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









class Controlling:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_to=None
        self.send_to=None
        self.window=client_gui.gui()
        self.window.screen_canvas.focus_set()
        self.window.screen_canvas.bind('<Key>', self.send_keyboard)
        self.window.screen_canvas.bind('<Button>',self.send_mouse)
        self.window.screen_canvas.bind('<ButtonRelease>',self.send_mouse)

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
            connection, address = self.socket.accept()
            self.listen_to=connection

            print(f"Accepted connection from {address}")



            threading.Thread(target=self.receive_data, args=(self.listen_to, address), daemon=True).start()
            break
        self.connect('10.0.0.9',9998)

    def send_keyboard(self, event):
        keyboard_keycode = event.keycode
        keyboard_scancode = win32api.MapVirtualKey(keyboard_keycode, 4)

        data = f'k~{keyboard_keycode}~{keyboard_scancode}'
        #data = input('send: ')
        try:
            self.send_to.sendall(data.encode())
        except socket.error as e:
            print(f"Failed to send data - Error: {e}")
            self.send_to.close()

    def send_mouse(self,event):
        data=''
        match int(event.type):
            case 4:  #mouse-down
                data=f'm~d~{event.num}~{event.x}~{event.y}~{self.window.actual_screenShare_size[0]}~{self.window.actual_screenShare_size[1]}'
            case 5: #mouse-up
                data=f'm~u~{event.num}~{event.x}~{event.y}~{self.window.actual_screenShare_size[0]}~{self.window.actual_screenShare_size[1]}'
        try:
            self.send_to.sendall(data.encode())
        except socket.error as e:
            print(f"Failed to send data - Error: {e}")
            self.send_to.close()

    def receive_data(self, connection, address):
        while True:
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
        self.window.start()



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

            sending_thread=threading.Thread(target=self.send_data, daemon=True)
            sending_thread.start()
            return
        except socket.error as e:
            print(f"Failed to connect to {peer_host} : {peer_port} - Error: {e}")
            return

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host} : {self.port}")

        while True:
            connection, address = self.socket.accept()
            self.listen_to=connection

            print(f"Accepted connection from {address}")




            threading.Thread(target=self.receive_data, args=(self.listen_to, address), daemon=True).start()

    def send_data(self):
        while True:
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
            try:
                recv_data=connection.recv(1024)
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

if __name__ == "__main__":
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

