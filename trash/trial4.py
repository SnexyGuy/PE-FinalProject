import cv2
import socket
import pickle
import os
import numpy as np
from tkinter import *
from PIL import ImageTk,Image


root = Tk()
# Create a frame
app = Frame(root, bg="white",width=100,height=100)
app.grid()
# Create a label in the frame
lmain = Label(app)
lmain.grid()

root.mainloop()







s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_ip='10.0.0.9'
server_port=9999
s.connect((server_ip,server_port))

while True:
    x=s.recv(1000000) #recvfrom
    #clientip=x[1][0]
    data=x   #x[0]

    data=pickle.loads(data)

    img=cv2.imdecode(data,cv2.IMREAD_COLOR)

    imgtk=ImageTk.PhotoImage(img)
    #img=ImageTk.PhotoImage(data)
    #cv2.imshow('img server',img)


    #img=ImageTk.PhotoImage(image=Image.fromarray(data))


    lmain.configure(image=imgtk)

    lmain.update()

    #if cv2.waitKey(5) & 0xFF == 27:
        #break


#cv2.destroyAllWindows()
