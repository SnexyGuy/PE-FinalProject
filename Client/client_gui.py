import time
import tkinter as tk
from tkinter import messagebox
import PIL.Image
from PIL import ImageGrab, ImageTk, ImageOps, Image, ImageChops, ImageDraw
import socket
import threading
import win32api


'''
def resize(event):

    display = ImageGrab.grab()

    display.thumbnail((event.width,event.height))

    display_img=ImageTk.PhotoImage(display)

    new_width=event.width-display_img.width()
    new_height=event.height-display_img.height()

    event.widget.itemconfigure(screen_image,image=display_img)
    event.widget.moveto(screen_image, new_width/2, new_height/2)

    event.widget.image=display_img
    print(f'{event.width}x{event.height}')




if __name__ == "__main__":


    root=tk.Tk()


    Controlling_client_frame=tk.Frame(root)
    
    global display
    display = ImageGrab.grab()
    global display_img
    display_img=ImageTk.PhotoImage(display)


    displayed_screen=tk.Canvas(Controlling_client_frame,bg='green')
    
    displayed_screen.update()
    
    screen_image=displayed_screen.create_image(displayed_screen.winfo_reqwidth()/2,displayed_screen.winfo_reqheight()/2,image=display_img, anchor='center')
    displayed_screen.image=display_img

    displayed_screen.pack(fill='both', expand=True)
    Controlling_client_frame.pack(fill='both',expand=True)


    displayed_screen.bind('<Configure>',resize)
    root.mainloop()
'''

'''------------------------------------------------------------------------'''
class gui:
    def __init__(self):
        self.root=tk.Tk()
        #------------------------------------------------------------
        self.connect_frame=tk.Frame(self.root)
        self.connect_frame.pack()

        self.connect_label=tk.Label(self.connect_frame,text='Connected To: None')
        self.connect_label.pack()

        self.connect_button = tk.Button(self.connect_frame, text="Connect", command=self.connect_to_welcome)
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

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register)
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

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        self.login_to_register_button = tk.Button(self.login_frame, text="ToRegister", command=self.login_to_register_frame)
        self.login_to_register_button.pack()
        #-----------------------------------------------------------
        self.rooms_frame=tk.Frame(self.root)
        self.rooms_frame.forget()

        self.enter_room_label = tk.Label(self.rooms_frame, text="enter room password:")
        self.enter_room_label.pack()

        self.enter_room_entry = tk.Entry(self.rooms_frame)
        self.enter_room_entry.pack()

        #self.enter_room_button = tk.Button(self.rooms_frame, text="enter room", command=self.enter_room)
        #self.enter_room_button.pack()

        #self.create_room_button = tk.Button(self.rooms_frame, text="create room", command=self.create_room)
        #self.create_room_button.pack()

        #-----------------------------------------------------------
        self.screen_frame=tk.Frame(self.root)
        self.screen_canvas=tk.Canvas(self.screen_frame, bg='green')
        self.screen_image=self.screen_canvas.create_image(self.screen_canvas.winfo_reqwidth() / 2, self.screen_canvas.winfo_reqheight() / 2, image=None, anchor='center')
        self.screen_frame.pack(fill='both', expand=True)
        self.screen_frame.forget()

        self.screen_canvas.pack(fill='both', expand=True)
        self.screen_canvas.bind('<Configure>', self.screen_frame_resize)
        self.received_screen : PIL.Image.Image = ImageGrab.grab()


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
        self.rooms_frame.pack()
        self.login_frame.forget()



    def register(self):
        pass

    def login(self):
        userid = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # You can add your own validation logic here
        if userid == "admin" and password == "password":
            answer=messagebox.askquestion('login success','login successful',type=messagebox.OK)
            if answer==messagebox.OK:
                self.login_to_rooms_frame()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")






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

g=gui()
g.start()

'''
if __name__ == "__main__":
    host, port = input('enter host:port for new peer -> ').split(':')
    node = Controlled(host, int(port))
    node.start()

    # Give some time for nodes to start listening
    import time
    time.sleep(2)

    con_host, con_port = input('enter host:port to connect to -> ').split(':')
    node.connect(con_host, int(con_port))
    time.sleep(1)  # Allow connection to establish
    node.send_data("Hello from node!")
'''