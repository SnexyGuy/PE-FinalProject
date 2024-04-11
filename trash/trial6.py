from tkinter import *
from PIL import ImageTk, Image,ImageGrab
import cv2
from mss import mss
import numpy as np


root = Tk()
# Create a frame
app = Frame(root, bg="white",width=100,height=100)
app.grid()
# Create a label in the frame
lmain = Label(app)
lmain.grid()

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct = mss()



# Capture from camera
#cap = cv2.VideoCapture(0)


# function for video streaming
def video_stream():
    while True:
        sct_img = ImageGrab.grab()
        #sct.grab(bounding_box)
        #scsh = np.array(sct_img)


        #_, frame = cap.read()
        #cv2image = cv2.cvtColor(scsh, cv2.COLOR_BGR2RGBA)

        #img = Image.fromarray(cv2image)

        sct_img.thumbnail((1000, 1000))

        imgtk = ImageTk.PhotoImage(image=sct_img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.update()

video_stream()
root.mainloop()