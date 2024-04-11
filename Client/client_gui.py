import time
import tkinter as tk

import PIL.Image
from PIL import ImageGrab, ImageTk, ImageOps, Image, ImageChops, ImageDraw
import socket
import threading



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
        self.screen_frame=tk.Frame(self.root)
        self.screen_canvas=tk.Canvas(self.screen_frame, bg='green')
        self.screen_image=self.screen_canvas.create_image(self.screen_canvas.winfo_reqwidth() / 2, self.screen_canvas.winfo_reqheight() / 2, image=None, anchor='center')
        self.screen_canvas.pack(fill='both', expand=True)
        self.screen_frame.pack(fill='both', expand=True)
        self.screen_canvas.bind('<Configure>', self.resize)
        self.received_screen : PIL.Image.Image = ImageGrab.grab()

    def resize(self, event : tk.Event):
        display= self.received_screen

        display.thumbnail((event.width, event.height))

        display_img = ImageTk.PhotoImage(display)

        new_width = event.width - display_img.width()
        new_height = event.height - display_img.height()

        event.widget.itemconfigure(self.screen_image, image=display_img)
        event.widget.moveto(self.screen_image, new_width / 2, new_height / 2)

        event.widget.image = display_img
        print(f'{event.width}x{event.height}')
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