import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections=[]
    def connect(self,peer_host, peer_port):
        try:
            connection=socket.create_connection((peer_host,peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_host} : {peer_port}")
        except socket.error as e:
            print(f"Failed to connect to {peer_host} : {peer_port} - Error: {e}")
    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host} : {self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
    def send_data(self,data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data - Error: {e}")
                self.connections.remove(connection)
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
        self.connections.remove(connection)
        connection.close()
    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()



if __name__ == "__main__":
    host, port = input('enter host:port for new peer -> ').split(':')
    node = Peer(host, int(port))
    node.start()

    # Give some time for nodes to start listening
    import time
    time.sleep(2)

    con_host, con_port = input('enter host:port to connect to -> ').split(':')
    node.connect(con_host, int(con_port))
    time.sleep(1)  # Allow connection to establish
    node.send_data("Hello from node!")
