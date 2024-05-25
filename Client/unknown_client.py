from controlling_client import *
from controlled_client import *
from tkinter import messagebox
from general_important_functions import *


class unknown_client:
    def __init__(self,host):
        self.host=host
        self.server_address='192.168.56.1'
        self.server_port = 9999

        self.window=gui()
        self.window.register_button.configure(command=self.handling_register)
        self.window.login_button.configure(command=self.handling_login)
        self.window.enter_room_button.configure(command=self.handling_connecting_to_room)
        self.window.create_room_button.configure(command=self.handling_room_creation)
        self.window.connect_button.configure(command=self.connect_to_server)

    def connect_to_server(self):
        try:
            connection = socket.create_connection((self.server_address,self.server_port))
            self.server = connection
            print(f"Connected to {self.server.getsockname()[0]} : {self.server.getsockname()[1]}")

            confirmation=recv_all(self.server).decode()

            if confirmation == 'continue':
                receive_from_server_thread=threading.Thread(target=self.receive_from_server)
                receive_from_server_thread.start()
                self.window.connect_to_welcome()
                return 'w'
            else:
                self.server.close()
                return 'noconfirm'

        except socket.error as err:
            ans = messagebox.showerror('failed connection to server', f'{err}\n want to try again?',type=messagebox.RETRYCANCEL)
            if ans == messagebox.RETRY:
                self.connect_to_server()
            else:
                return 'f'

    def handling_login(self):
        username = self.window.login_username_entry.get()
        password = self.window.login_password_entry.get()
        data_list=['l',username,password]
        data = pickle.dumps(data_list)
        msg_size = len(data)
        try:
            self.server.sendall(msg_size.to_bytes(8,sys.byteorder)+data)
        except socket.error as error:
            self.server.close()
            messagebox.showerror('failed communication with server', f'{error}')

    def handling_register(self):
        username = self.window.register_username_entry.get()
        password = self.window.register_password_entry.get()
        data_list = ['r', username, password.encode()]
        data = pickle.dumps(data_list)
        msg_size = len(data)
        try:
            self.server.sendall(msg_size.to_bytes(8,sys.byteorder)+data)
        except socket.error as error:
            self.server.close()
            messagebox.showerror('failed communication with server', f'{error}')

    def handling_room_creation(self):
        client_type=''
        ans=messagebox.askquestion('your type of client','Controlling (YES) OR Controlled? (NO)')
        if ans == messagebox.YES:
            client_type='Controlling'
        elif ans == messagebox.NO:
            client_type='Controlled'

        try:
            msg_list=['rooms','create-room',client_type]
            msg=pickle.dumps(msg_list)
            msg_len=len(msg)
            self.server.sendall(msg_len.to_bytes(8,sys.byteorder))
        except socket.error as error:
            self.server.close()
            messagebox.showerror('failed communication with server', f'{error}')


    def handling_connecting_to_room(self):
        code=self.window.enter_room_entry.get()
        type=''
        ans=messagebox.askquestion('your type of client', 'Controlling (YES) OR Controlled? (NO)')
        if ans == messagebox.YES:
            type='Controlling'
        elif ans == messagebox.NO:
            type='Controlled'
        msg_list=['rooms','connect-to-room',type,code]
        msg=pickle.dumps(msg_list)
        msg_len=len(msg)
        self.server.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)

    def receive_from_server(self):
        while True:
            try:
                received=recv_all(self.server)
                answer=pickle.loads(received)

                if answer[0] == 'registration-w':
                    self.window.register_to_login_frame()
                elif answer[0] == 'registration-f':
                    ans = messagebox.showerror('failed registration', 'want to try again?',type=messagebox.RETRYCANCEL)
                    if ans == messagebox.CANCEL:
                        self.end()
                elif answer[0] == 'registration-to-login':
                    ans=messagebox.showinfo('user already exists','ok-login,cancel-stay in register',type=messagebox.OKCANCEL)
                    if ans == messagebox.OK:
                        self.window.register_to_login_frame()

                if answer[0] == 'login-w':
                    self.window.login_to_rooms_frame()
                elif answer[0] == 'login-f':
                    ans = messagebox.showerror('failed login', 'want to try again?',type=messagebox.RETRYCANCEL)
                    if ans == messagebox.CANCEL:
                        self.end()
                elif answer[0] == 'login-to-register':
                    ans=messagebox.showinfo('user doesnt exist','ok-register,cancel-stay in login',type=messagebox.OKCANCEL)
                    if ans == messagebox.OK:
                        self.window.login_to_register_frame()


                if answer[0] == 'room-exists':
                    messagebox.showinfo('room already exists', 'you tried to create a room that already exists',type=messagebox.OK)
                elif answer[0] == 'room-created':
                    self.window.create_to_waiting()
                    self.window.show_room_code(answer[1])
                    messagebox.showinfo('room created successfuly', 'room created- send the code to your friend',type=messagebox.OK)

                    if answer[2] == 'Controlling':
                        controlling_peer = Controlling(self.host,self.window)
                        controlling_peer.start()
                        cing_address,cing_port=self.lock_until_peer_ready_to_connect('Controlling')
                        controlling_peer.connect(cing_address,cing_port)
                        self.end_all()
                    elif answer[2] == 'Controlled':
                        controlled_peer = Controlled(self.host)
                        controlled_peer.start()
                        cod_address,cod_port=self.lock_until_peer_ready_to_connect('Controlled')
                        controlled_peer.connect(cod_address,cod_port)
                        self.end_all()


                elif answer[0] == 'room-creation-failed':
                    ans=messagebox.showerror('failed room creation', 'want to try again?', type=messagebox.RETRYCANCEL)
                    if ans == messagebox.CANCEL:
                        self.end()

                if answer[0] == 'same-type-error':
                    messagebox.showerror('same type as room creator', f'room creator type is: {answer[1]}, you need to connect as the opposite type')
                elif answer[0] == 'room-closing-failed':
                    messagebox.showerror('room closing failure', 'room closing after connection failed, check if room code is correct, if correct then there was an error, try again')
                elif answer[0] == 'connect-to-nonexistent-room':
                    messagebox.showerror('room doesnt exist', 'the room you tried to connect to does not exist')
                elif answer[0] == 'connecting-to-room-failed':
                    messagebox.showerror('room connection failed', 'an error occurred while connecting to the room, please try again ')
                else:
                    peer_address = answer[0]
                    peer_port = answer[1]
                    peer_type = answer[2]
                    self.connecting_peers(peer_address,peer_port,peer_type)

            except socket.error as error:
                self.server.close()
                messagebox.showerror('failed communication with server', f'{error}')
                break


    def connecting_peers(self,peer_address,peer_port,peer_type):
        if peer_type == 'Controlling':
            controlled_peer=Controlled(self.host)
            controlled_peer.start()
            signal_msg = ['peers', 'ready-for-connection', 'Controlled']
            pickled_msg = pickle.dumps(signal_msg)
            msg_len = len(pickled_msg)
            self.server.sendall(msg_len.to_bytes(8, sys.byteorder) + pickled_msg)
            controlled_peer.connect(peer_address,peer_port)
            self.end_all()
        elif peer_type == 'Controlled':
            controlling_peer = Controlling(self.host,self.window)
            controlling_peer.start()
            signal_msg = ['peers', 'ready-for-connection', 'Controlling']
            pickled_msg = pickle.dumps(signal_msg)
            msg_len = len(pickled_msg)
            self.server.sendall(msg_len.to_bytes(8, sys.byteorder) + pickled_msg)
            controlling_peer.connect(peer_address,peer_port)
            self.end_all()


    def lock_until_peer_ready_to_connect(self,peer_type):
        while True:
            message_bytes = recv_all(self.server)
            message = pickle.loads(message_bytes)
            if message[0] == 'ready-to-connect':
                if message[1] == peer_type:
                    continue
                else:
                    return (message[2],message[3])
            else:
                continue

    def end(self):
        self.server.close()
        self.window.root.destroy()
        del self

    def end_all(self):
        self.server.close()
        end_all_threads()
        delete_all_thread_flags()
        del self

    def start(self):
        self.window.start()
