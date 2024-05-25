import socket
import sys
import threading
import sqlite3
import pickle
import hashlib
import secrets



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
    def __init__(self, host):
        self.host=host
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections : dict [tuple[str,int],socket.socket] = {}
        self.db=DataBaseHandler()
    def listen(self):
        self.socket.bind((self.host,9999))
        self.port=self.socket.getsockname()[1]
        self.socket.listen(10)
        print(f"Listening for connections on {self.host} : {self.port}")

        while True:
            connection, address = self.socket.accept()

            conn_confirm='continue'.encode()
            msg_size=len(conn_confirm)

            connection.sendall(msg_size.to_bytes(8,sys.byteorder)+conn_confirm)

            self.connections.update({address : connection})
            print(f"Accepted connection from {address}")
            client_thread=threading.Thread(target=self.handle_client, args=(connection, address))
            client_thread.start()
            thread_event_setter(client_thread.ident)
    def handle_client(self,connection : socket.socket,address):
        while True:
            if check_thread_flag(threading.get_ident()):
                connection.close()
                thread_event_remove(threading.get_ident())
                break

            try:
                recv_data=recv_all(connection)
                data=pickle.loads(recv_data)
                if data[0] == 'r' or data[0] == 'l':
                    if data[0] == 'r':
                        hashed_pwd=hashlib.sha256(data[2]).hexdigest()
                        ans=self.db.register(data[1],hashed_pwd)
                        if ans == 'w':
                            msg_list=['registration-w']
                            msg=pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg_list = ['registration-f']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'exist':
                            msg_list = ['registration-to-login']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)

                    elif data[0] == 'l':
                        hashed_pwd=hashlib.sha256(data[2]).hexdigest()
                        ans=self.db.login_check(data[1],hashed_pwd)
                        if ans == 'w':
                            msg_list=['login-w']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg_list=['login-f']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'noexist':
                            msg_list=['login-to-register']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                elif data[0] == 'rooms':
                    if data[1] == 'create-room':
                        address,port = connection.getpeername()
                        code=generate_room_code(self.db.connection)
                        ans=self.db.create_room(address,port,data[2],code)
                        if ans == 'exist':
                            msg_list=['room-exists']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'w':
                            msg_list=['room-created',code,data[2]]
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg_list=['room-creation-failed']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                    elif data[1] == 'connect-to-room':
                        ans=self.db.enter_room(data[2],data[3])
                        if ans == 'err-same-type':
                            msg_list=['same-type-error', data[2]]
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'noendroom':
                            msg_list=['room-closing-failed']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'noexist':
                            msg_list=['connect-to-nonexistent-room']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        elif ans == 'f':
                            msg_list=['connecting-to-room-failed']
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                        else:
                            msg_list=[ans[0],ans[1],ans[2]]
                            msg = pickle.dumps(msg_list)
                            msg_len=len(msg)
                            connection.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
                elif data[0] == 'peers':
                    if data[1] == 'ready-for-connection':
                        address = connection.getpeername()
                        peer_sock=self.find_connection(address)

                        msg_list=['ready-to-connect', data[2], address[0], address[1]]
                        msg=pickle.dumps(msg_list)
                        msg_len=len(msg)
                        peer_sock.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
            except socket.error:
                break
        print(f"Connection from {address} closed")
        self.connections.pop(address)
        connection.close()

    def find_connection(self, address : tuple[str,int]):
        for conn_addr in self.connections:
            if conn_addr == address:
                return self.connections[conn_addr]

    def start(self):
        listen_thread=threading.Thread(target=self.listen)
        listen_thread.start()







address=socket.gethostbyname(socket.gethostname())
server=Server(address)
server.start()