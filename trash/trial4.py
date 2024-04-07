import cv2
import socket
import pickle
import os
import numpy as np

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_ip='10.0.0.10'
server_port=9999
s.bind((server_ip,server_port))


while True:
    x=s.recvfrom(1000000)
    clientip=x[1][0]
    data=x[0]
    data=pickle.loads(data)
    img=cv2.imdecode(data,cv2.IMREAD_COLOR)
    cv2.imshow('img server',img)

    if cv2.waitKey(5) & 0xFF == 27:
        break


cv2.destroyAllWindows()
