import tkinter as tk
#from win32api import GetSystemMetrics
#from tkinter import ttk

#screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)

from PIL import ImageGrab, ImageTk


class Client_Window(tk.Tk):
    def __init__(self,title,size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])



        self.Controlling_client_frame=Controlling_client_frame(self)


        self.mainloop()


class Controlling_client_frame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent



        img = ImageGrab.grab()
        img2 = ImageTk.PhotoImage(img)


        self.screen = tk.Canvas(self,bg='green')



        self.screen.create_image(0,0,image=img2,anchor='nw')
        self.screen.image=img2

        self.screen.pack(fill='both', expand=True)
        self.pack(fill='both',expand=True)







Client_Window('hi',(500,500))



#i have to work on dynamic image sizing in relation to window size