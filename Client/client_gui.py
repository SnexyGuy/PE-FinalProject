import tkinter as tk
from PIL import ImageGrab, ImageTk, Image





class gui:
    def __init__(self):
        self.root=tk.Tk()
        #------------------------------------------------------------
        self.connect_frame=tk.Frame(self.root)
        self.connect_frame.pack()

        self.connect_label=tk.Label(self.connect_frame,text='Connected To: None')
        self.connect_label.pack()

        self.connect_button = tk.Button(self.connect_frame, text="Connect")
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

        self.register_button = tk.Button(self.register_frame, text="Register")
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

        self.login_button = tk.Button(self.login_frame, text="Login")
        self.login_button.pack()

        self.login_to_register_button = tk.Button(self.login_frame, text="ToRegister", command=self.login_to_register_frame)
        self.login_to_register_button.pack()
        #-----------------------------------------------------------
        self.connect_room_frame=tk.Frame(self.root)
        self.connect_room_frame.forget()

        self.enter_room_label = tk.Label(self.connect_room_frame, text="enter room code:")
        self.enter_room_label.pack()

        self.enter_room_entry = tk.Entry(self.connect_room_frame)
        self.enter_room_entry.pack()

        self.enter_room_button = tk.Button(self.connect_room_frame, text="enter room")
        self.enter_room_button.pack()

        self.connect_to_create_button=tk.Button(self.connect_room_frame,text='to room creation',command=self.roomConn_to_roomCreate)
        self.connect_to_create_button.pack()

        #-----------------------------------------------------------------------------------------
        self.create_room_frame=tk.Frame(self.root)
        self.create_room_frame.forget()

        self.create_room_label = tk.Label(self.create_room_frame, text="")
        self.create_room_label.pack()

        self.create_room_button = tk.Button(self.create_room_frame, text="create room")
        self.create_room_button.pack()

        self.create_to_connect_button=tk.Button(self.create_room_frame,text='to room connection',command=self.roomCreate_to_roomConn)
        self.create_to_connect_button.pack()

        #--------------------------------------------------------------------------------
        self.waiting_frame=tk.Frame(self.root)
        self.waiting_frame.forget()

        self.waiting_label = tk.Label(self.waiting_frame, text="waiting for your friend to enter")
        self.waiting_label.pack()

        self.code_text = tk.Text(self.waiting_frame,height=2,borderwidth=0)
        self.code_text.pack()

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
        self.connect_room_frame.pack()
        self.login_frame.forget()

    def create_to_waiting(self):
        self.waiting_frame.pack()
        self.create_room_frame.forget()

    def roomCreate_to_roomConn(self):
        self.connect_room_frame.pack()
        self.create_room_frame.forget()

    def roomConn_to_roomCreate(self):
        self.create_room_frame.pack()
        self.connect_room_frame.forget()

    def show_room_code(self,code):
        self.code_text.insert(1.0,f'room code:\n{code}')
        self.code_text.configure(state='disabled')

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