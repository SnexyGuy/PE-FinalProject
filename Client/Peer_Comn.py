import socket
import threading
import pickle
import time
import lzma
import socketMassages
from PIL import ImageGrab


class Controlling:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_to=None
        self.send_to=None
        self.connected_to=None

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


            threading.Thread(target=self.handle_client, args=(self.listen_to, address), daemon=True).start()

    def send_data(self):
        while True:
            data = input('send: ')
            try:
                self.send_to.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data - Error: {e}")
                self.send_to.close()
                break
        return
    def handle_client(self,connection,address):
        while True:
            try:
                data=connection.recv(1000000)
                if not data:
                    break
                print(f"Received data from {address} : {data.decode()}")
            except socket.error:
                break
        print(f"Connection from {address} closed")
        self.listen_to.close()
    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()


class Controlled:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_to=None
        self.send_to=None
        self.connected_to=None

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


            threading.Thread(target=self.handle_client, args=(self.listen_to, address), daemon=True).start()

    def send_data(self):
        while True:
            data = input('send: ')
            try:
                self.send_to.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data - Error: {e}")
                self.send_to.close()
                break
        return
    def handle_client(self,connection,address):
        while True:
            try:
                data=connection.recv(1024)
                if not data:
                    break
                print(f"Received data from {address} : {data.decode()}")
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
        c=Controlling('10.0.0.10',9999)
        c.start()
    elif ans == 'cd':
        cd=Controlled('10.0.0.10',9998)
        cd.start()
        time.sleep(1)
        cd.connect('10.0.0.10',9999)
