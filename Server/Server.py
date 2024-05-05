import socket
import sys
import threading
import sqlite3
import pickle
import hashlib
import secrets



#function that generates new room passwords

def generate_room_code(db : sqlite3.Connection):
    while True:
        generated_code=secrets.token_hex(32)
        code_response = db.execute("SELECT EXISTS(SELECT * FROM open_rooms WHERE password = ? )", (generated_code,))
        code_fetched = code_response.fetchone()[0]
        if code_fetched == 1:
            continue
        elif code_fetched == 0:
            return generated_code





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


#data base handler class

class DataBaseHandler():
    def __init__(self):
        self.connection=sqlite3.connect('rdp_db.sql')
        self.connection.executescript("""
        \
            CREATE TABLE IF NOT EXISTS usersdata (
                id INTEGER PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
            \
            CREATE TABLE IF NOT EXISTS open_rooms (
                id INTEGER PRIMARY KEY,
                creator_address VARCHAR(255) NOT NULL,
                creator_port INTEGER NOT NULL,
                creator_type VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
            """)
        self.connection.commit()

    def login_check(self,username,password):
        try:
            result=self.connection.execute("SELECT * FROM usersdata WHERE username = ? AND password = ?",(username,password))
            fetched=result.fetchall()
            if fetched:
                return 'w'
            else:
                return 'noexist'
        except sqlite3.Error as err:
            return 'f'

        pass
    def register(self,username,hashed_password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM usersdata WHERE username=?)", (username,))
            fetched = response.fetchone()[0]
            if fetched == 1:
                return 'exist'
            else:
                self.connection.execute("INSERT INTO usersdata (username,password) VALUES (?,?)",(username,hashed_password))
                self.connection.commit()
                return 'w'
        except sqlite3.Error as err:
            return 'f'

    def delete_user(self,username):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM usersdata WHERE username=?)", (username,))
            fetched = response.fetchone()[0]
            if fetched == 1: #exists
                self.connection.execute("DELETE from usersdata where username = ?;",(username,))
                self.connection.commit()
                return 'w'
            else:
                return 'noexist'
        except sqlite3.Error as err:
            return 'f'


    def create_room(self,address,port,type,code):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM open_rooms WHERE creator_address = ? AND creator_port = ? AND creator_type = ?)", (address, port, type))
            fetched = response.fetchone()[0]
            if fetched == 1:
                return 'exist'
            else:
                self.connection.execute("INSERT INTO open_rooms (creator_address,creator_port,creator_type,password) VALUES (?,?,?,?)",(address, port,type,code))
                self.connection.commit()
                return 'w'
        except sqlite3.Error as err:
            return 'f'
    def end_room(self,address,port,type,password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM open_rooms WHERE creator_address = ? AND creator_port = ? AND creator_type = ? AND password = ? )", (address, port, type, password))
            fetched = response.fetchone()[0]
            if fetched == 1: #exists
                self.connection.execute("DELETE from open_rooms WHERE creator_address = ? AND creator_port = ? AND creator_type = ? AND password = ?;", (address, port, type, password))
                self.connection.commit()
                return 'w'
            else:
                return 'noexist'
        except sqlite3.Error as err:
            return 'f'

    def enter_room(self,type,password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM open_rooms WHERE password = ? )", (password,))
            fetched = response.fetchone()[0]
            if fetched == 1: #exists
                room_data=self.connection.execute("SELECT * FROM open_rooms WHERE password = ?;", (password,))
                fetched_data=room_data.fetchall()
                address=fetched_data[0][1]
                port=fetched_data[0][2]
                peer_type=fetched_data[0][3]
                if peer_type == type:
                    return 'err-same-type'
                elif peer_type != type:
                    status=self.end_room(address,port,peer_type,password)
                    if status == 'w':
                        return (address,port,peer_type)
                    elif status == 'noexist' or status == 'f':
                        return 'noendroom'
            else:
                return 'noexist'
        except sqlite3.Error as err:
            return 'f'

    def close_db(self):
        try:
            self.connection.close()
            return 'w'
        except sqlite3.Error:
            return 'f'








class Server:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections=[]
        self.db=DataBaseHandler()
    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host} : {self.port}")

        while True:
            connection, address = self.socket.accept()

            conn_confirm='continue'.encode()
            msg_size=len(conn_confirm)

            connection.sendall(msg_size.to_bytes(8,sys.byteorder)+conn_confirm)

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
    def handle_client(self,connection : socket.socket,address):
        while True:
            try:
                recv_data=recv_all(connection)
                data=pickle.loads(recv_data)
                if data[0] == 'r' or data[0] == 'l':
                    if data[0] == 'r':
                        hashed_pwd=hashlib.sha256(data[2]).hexdigest()
                        ans=self.db.register(data[1],hashed_pwd)
                        if ans == 'w':
                            msg='registration-w'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg = 'registration-f'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'exist':
                            msg = 'registration-to-login'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)

                    elif data[0] == 'l':
                        hashed_pwd=hashlib.sha256(data[2]).hexdigest()
                        ans=self.db.login_check(data[1],hashed_pwd)
                        if ans == 'w':
                            msg='login-w'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg='login-f'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'noexist':
                            msg='login-to-register'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                elif data[0] == 'rooms':
                    if data[1] == 'create-room':
                        address,port = connection.getpeername()
                        code=generate_room_code(self.db.connection)
                        ans=self.db.create_room(address,port,data[2],code)
                        if ans == 'exist':
                            msg='room-exists'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'w':
                            msg='room-created'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg='room-creation-failed'.encode()
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)



            except socket.error:
                break
        print(f"Connection from {address} closed")
        self.connections.remove(connection)
        connection.close()
    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()