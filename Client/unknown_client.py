import time
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
        self.window.code_text.bind('<Control-c>',self.room_code_copy)
        self.window.copy_code_button.configure(command=self.waiting_frame_copy_code_button_command)

    def connect_to_server(self):
        try:
            connection = socket.create_connection((self.server_address,self.server_port))
            self.server = connection
            self.port=self.server.getsockname()[1]
            print(f"Connected to {self.server.getpeername()[0]} : {self.server.getpeername()[1]}")

            confirmation=recv_all(self.server).decode()

            if confirmation == 'continue':
                receive_from_server_thread=threading.Thread(target=self.receive_from_server)
                receive_from_server_thread.start()
                thread_event_setter(receive_from_server_thread.ident)
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
        data_list=['l',username,password.encode()]
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
        ans=messagebox.askquestion('your type of client','Controlling (YES) OR Controlled? (NO)')
        if ans == messagebox.YES:
            self.client_type='Controlling'
        elif ans == messagebox.NO:
            self.client_type='Controlled'

        try:
            msg_list=['rooms','create-room',self.client_type]
            msg=pickle.dumps(msg_list)
            msg_len=len(msg)
            self.server.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)
        except socket.error as error:
            self.server.close()
            messagebox.showerror('failed communication with server', f'{error}')

    def handling_connecting_to_room(self):
        code=self.window.enter_room_entry.get()
        ans=messagebox.askquestion('your type of client', 'Controlling (YES) OR Controlled? (NO)')
        if ans == messagebox.YES:
            self.client_type='Controlling'
        elif ans == messagebox.NO:
            self.client_type='Controlled'
        msg_list=['rooms','connect-to-room',self.client_type,code]
        msg=pickle.dumps(msg_list)
        msg_len=len(msg)
        self.server.sendall(msg_len.to_bytes(8,sys.byteorder)+msg)

    def receive_from_server(self):
        while True:
            if check_thread_flag(threading.get_ident()):
                self.server.close()
                thread_event_remove(threading.get_ident())
                delete_all_thread_flags()
                break
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

                elif answer[0] == 'login-w':
                    self.window.login_to_rooms_frame()
                elif answer[0] == 'login-f':
                    ans = messagebox.showerror('failed login', 'want to try again?',type=messagebox.RETRYCANCEL)
                    if ans == messagebox.CANCEL:
                        self.end()
                elif answer[0] == 'login-to-register':
                    ans=messagebox.showinfo('user doesnt exist','ok-register,cancel-stay in login',type=messagebox.OKCANCEL)
                    if ans == messagebox.OK:
                        self.window.login_to_register_frame()

                elif answer[0] == 'room-exists':
                    messagebox.showinfo('room already exists', 'you tried to create a room that already exists',type=messagebox.OK)
                elif answer[0] == 'room-created':
                    self.window.create_to_waiting()
                    self.window.show_room_code(answer[1])
                    messagebox.showinfo('room created successfuly', 'room created- send the code to your friend',type=messagebox.OK)

                    if self.client_type == 'Controlling':
                        self.controlling_peer = Controlling(self.host,self.port,self.window)
                        #self.controlling_peer.window.waiting_to_screen_share()
                        self.controlling_peer.start()
                        #self.end_all()

                    elif self.client_type == 'Controlled':
                        self.controlled_peer = Controlled(self.host,self.port)
                        self.controlled_peer.start()
                        #self.window.root.destroy()
                        #self.end_all()

                elif answer[0] == 'room-creation-failed':
                    ans=messagebox.showerror('failed room creation', 'want to try again?', type=messagebox.RETRYCANCEL)
                    if ans == messagebox.CANCEL:
                        self.end()

                elif answer[0] == 'same-type-error':
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
            controlled_peer=Controlled(self.host,self.port)
            controlled_peer.start()
            controlled_peer.connect(peer_address,peer_port)
            self.window.root.destroy()
            self.end_all()
        elif peer_type == 'Controlled':
            controlling_peer = Controlling(self.host,self.port,self.window)
            controlling_peer.window.connect_to_screen_share()
            controlling_peer.start()
            controlling_peer.connect(peer_address,peer_port)
            self.end_all()


    def room_code_copy(self, event : tk.Event):
        if self.client_type == 'Controlling':
            self.window.copy_room_code_to_clipboard()
            self.controlling_peer.window.waiting_to_screen_share()
            #self.controlling_peer.start()
            self.end_all()
        elif self.client_type == 'Controlled':
            self.window.copy_room_code_to_clipboard()
            #self.controlled_peer.start()
            time.sleep(1.5)
            self.end()

    def waiting_frame_copy_code_button_command(self):
        self.window.copy_room_code_to_clipboard()
        if self.client_type == 'Controlling':
            self.controlling_peer.window.waiting_to_screen_share()
            #self.controlling_peer.start()
            self.end_all()
        elif self.client_type == 'Controlled':
            #self.controlled_peer.start()
            time.sleep(1.5)
            self.end()


    def end(self):
        #self.server.close()
        self.window.root.destroy()
        self.__del__()

    def end_all(self):
        #self.server.close()
        #end_all_threads()
        self.__del__()

    def start(self):
        self.window.start()

    def __del__(self):
        end_all_threads()
        #self.server.close()
        time.sleep(1)