import win32api
from PIL import ImageGrab
import pickle
import lz4.frame
import pyautogui
from general_important_functions import *
pyautogui.FAILSAFE=False


class Controlled:
    def __init__(self, host,port):
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

            if self.listen_to is None:
                msg = (self.host,self.port)
                send_all(self.send_to,msg)

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
            if check_thread_flag(threading.get_ident()):
                self.socket.close()
                thread_event_remove(threading.get_ident())
                break

            connection, address = self.socket.accept()
            self.listen_to=connection

            if self.send_to is None:
                bytes = recv_all(self.listen_to)
                peer_address, peer_port = pickle.loads(bytes)
                self.connect(peer_address,peer_port)

            print(f"Accepted connection from {address}")


            receive_thread=threading.Thread(target=self.receive_data, args=(self.listen_to, address))
            receive_thread.start()
            thread_event_setter(receive_thread.ident)

    def send_data(self):
        while True:
            if check_thread_flag(threading.get_ident()):
                self.send_to.close()
                thread_event_remove(threading.get_ident())
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
            if check_thread_flag(threading.get_ident()):
                connection.close()
                thread_event_remove(threading.get_ident())
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