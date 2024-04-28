import tkinter as tk
from tkinter import messagebox



class window:
    def __init__(self):

        self.root=tk.Tk()

        #-------------------------------------------------------
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

        #---------------------------------------------------------

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

        #------------------------------------------------------------

        self.welcome_frame=tk.Frame(self.root)
        self.welcome_frame.pack(fill='both', expand=True)

        self.choice_reg_button = tk.Button(self.welcome_frame, text="register", command=self.welcome_to_register_frame)
        self.choice_reg_button.pack()

        self.choice_login_button = tk.Button(self.welcome_frame, text="Login", command=self.welcome_to_login_frame)
        self.choice_login_button.pack()

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


    def register(self):
        pass





    def login(self):
        userid = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # You can add your own validation logic here
        if userid == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    def start(self):
        self.root.mainloop()


window=window()
window.start()