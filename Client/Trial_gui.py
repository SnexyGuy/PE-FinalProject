import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageGrab, ImageTk, Image
import time
import clipboard


class gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Share Application")
        self.root.geometry("800x600")

        # Define styles
        self.style = {
            "font": tkfont.Font(family="Helvetica", size=12),
            "bg": "#f0f0f0",
            "padx": 10,
            "pady": 10
        }

        # Main frames
        self.connect_frame = self.create_frame(self.root)
        self.welcome_frame = self.create_frame(self.root)
        self.register_frame = self.create_frame(self.root)
        self.login_frame = self.create_frame(self.root)
        self.connect_room_frame = self.create_frame(self.root)
        self.create_room_frame = self.create_frame(self.root)
        self.waiting_frame = self.create_frame(self.root)
        self.screen_frame = self.create_frame(self.root)

        # Connect Frame
        self.connect_label = self.create_label(self.connect_frame, text='Connected To: None')
        self.connect_button = self.create_button(self.connect_frame, text="Connect", command=self.connect_to_welcome)

        # Welcome Frame
        self.choice_reg_button = self.create_button(self.welcome_frame, text="Register",
                                                    command=self.welcome_to_register_frame)
        self.choice_login_button = self.create_button(self.welcome_frame, text="Login",
                                                      command=self.welcome_to_login_frame)

        # Register Frame
        self.create_label(self.register_frame, text="Userid:")
        self.register_username_entry = self.create_entry(self.register_frame)
        self.create_label(self.register_frame, text="Password:")
        self.register_password_entry = self.create_entry(self.register_frame, show="*")
        self.create_button(self.register_frame, text="Register")
        self.create_button(self.register_frame, text="To Login", command=self.register_to_login_frame)

        # Login Frame
        self.create_label(self.login_frame, text="Userid:")
        self.login_username_entry = self.create_entry(self.login_frame)
        self.create_label(self.login_frame, text="Password:")
        self.login_password_entry = self.create_entry(self.login_frame, show="*")
        self.create_button(self.login_frame, text="Login")
        self.create_button(self.login_frame, text="To Register", command=self.login_to_register_frame)

        # Connect Room Frame
        self.create_label(self.connect_room_frame, text="Enter Room Code:")
        self.enter_room_entry = self.create_entry(self.connect_room_frame)
        self.create_button(self.connect_room_frame, text="Enter Room")
        self.create_button(self.connect_room_frame, text="To Room Creation", command=self.roomConn_to_roomCreate)

        # Create Room Frame
        self.create_label(self.create_room_frame, text="Create a New Room")
        self.create_button(self.create_room_frame, text="Create Room")
        self.create_button(self.create_room_frame, text="To Room Connection", command=self.roomCreate_to_roomConn)

        # Waiting Frame
        self.create_label(self.waiting_frame, text="Waiting for your friend to enter")
        self.code_text = tk.Text(self.waiting_frame, height=2, borderwidth=0, bg=self.style["bg"])
        self.code_text.pack(padx=self.style["padx"], pady=self.style["pady"])
        self.create_button(self.waiting_frame, text='Copy Code', command=self.copy_room_code_to_clipboard)

        # Screen Frame
        self.screen_canvas = tk.Canvas(self.screen_frame, bg='green')
        self.screen_image = self.screen_canvas.create_image(self.screen_canvas.winfo_reqwidth() / 2,
                                                            self.screen_canvas.winfo_reqheight() / 2, image=None,
                                                            anchor='center')
        self.screen_frame.pack(fill='both', expand=True)
        self.screen_frame.pack_forget()
        self.screen_canvas.pack(fill='both', expand=True)
        self.screen_canvas.bind('<Configure>', self.screen_frame_resize)
        self.received_screen = ImageGrab.grab()

    def create_frame(self, parent):
        frame = tk.Frame(parent, bg=self.style["bg"])
        frame.pack(padx=self.style["padx"], pady=self.style["pady"])
        frame.pack_forget()
        return frame

    def create_label(self, parent, text):
        label = tk.Label(parent, text=text, font=self.style["font"], bg=self.style["bg"])
        label.pack(padx=self.style["padx"], pady=self.style["pady"])
        return label

    def create_button(self, parent, text, command=None):
        button = tk.Button(parent, text=text, font=self.style["font"], command=command)
        button.pack(padx=self.style["padx"], pady=self.style["pady"])
        return button

    def create_entry(self, parent, show=None):
        entry = tk.Entry(parent, font=self.style["font"], show=show)
        entry.pack(padx=self.style["padx"], pady=self.style["pady"])
        return entry

    def welcome_to_register_frame(self):
        self.register_frame.pack()
        self.welcome_frame.pack_forget()

    def welcome_to_login_frame(self):
        self.login_frame.pack()
        self.welcome_frame.pack_forget()

    def register_to_login_frame(self):
        self.login_frame.pack()
        self.register_frame.pack_forget()

    def login_to_register_frame(self):
        self.register_frame.pack()
        self.login_frame.pack_forget()

    def login_to_screen_share(self):
        self.screen_frame.pack(fill='both', expand=True)
        self.login_frame.pack_forget()

    def connect_to_welcome(self):
        self.welcome_frame.pack()
        self.connect_frame.pack_forget()

    def login_to_rooms_frame(self):
        self.connect_room_frame.pack()
        self.login_frame.pack_forget()

    def create_to_waiting(self):
        self.waiting_frame.pack()
        self.create_room_frame.pack_forget()

    def roomCreate_to_roomConn(self):
        self.connect_room_frame.pack()
        self.create_room_frame.pack_forget()

    def roomConn_to_roomCreate(self):
        self.create_room_frame.pack()
        self.connect_room_frame.pack_forget()

    def show_room_code(self, code):
        self.code_text.insert(1.0, f'Room Code:\n')
        self.code_text.insert(2.0, f'{code}')
        self.code_text.configure(state='disabled')

    def waiting_to_screen_share(self):
        time.sleep(1.5)
        self.screen_frame.pack(fill='both', expand=True)
        self.waiting_frame.pack_forget()

    def connect_to_screen_share(self):
        self.screen_frame.pack(fill='both', expand=True)
        self.connect_room_frame.pack_forget()

    def copy_room_code_to_clipboard(self):
        txt = self.retrieve_code_text_input()
        clipboard.copy(txt)

    def retrieve_code_text_input(self):
        input = self.code_text.get('2.0', 'end-1c')
        return input

    def screen_frame_resize(self, event):
        display = self.received_screen
        display.thumbnail((event.width, event.height))
        display_img = ImageTk.PhotoImage(display)
        self.actual_screenShare_size = (display_img.width(), display_img.height())
        new_width = event.width - display_img.width()
        new_height = event.height - display_img.height()
        event.widget.itemconfigure(self.screen_image, image=display_img)
        event.widget.moveto(self.screen_image, new_width / 2, new_height / 2)
        event.widget.image = display_img
        self.root.update()

    def update_screen(self, img):
        if img is None:
            display = self.received_screen
        else:
            display = img
            self.received_screen = img
        display.thumbnail((self.screen_canvas.winfo_width(), self.screen_canvas.winfo_height()))
        display_img = ImageTk.PhotoImage(display)
        new_width = self.screen_canvas.winfo_width() - display_img.width()
        new_height = self.screen_canvas.winfo_height() - display_img.height()
        self.screen_canvas.itemconfigure(self.screen_image, image=display_img)
        self.screen_canvas.moveto(self.screen_image, new_width / 2, new_height / 2)
        self.screen_canvas.image = display_img
        self.root.update()

    def receive_screen(self, screen):
        self.update_screen(screen)

    def start(self):
        self.root.mainloop()

