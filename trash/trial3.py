import cv2
import socket
import pickle
import os
import numpy as np
from PIL import ImageGrab,ImageTk

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)

server_ip='10.0.0.9'
server_port=9999
s.bind((server_ip,server_port))
s.listen(5)
conn,addr=s.accept()

#cap=cv2.VideoCapture(0)
#cap.set(3,640)
#cap.set(4,480)
while True: #cap.isOpened():
    #ret,img=cap.read()
    grb=ImageGrab.grab()
    grb.thumbnail((800,400))
    #img=ImageTk.PhotoImage(grb)
    img=np.asarray(grb)
    #cv2.imshow('img client',img)
    ret1,buffer=cv2.imencode('.png',img)

    x_as_bytes=pickle.dumps(buffer)
    conn.send(x_as_bytes)
    #if cv2.waitKey(5) & 0xFF == 27:
        #break


#cv2.destroyAllWindows()
#cap.release()
