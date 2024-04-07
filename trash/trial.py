import io
import time

from PIL import ImageGrab, Image
import socket
import threading
import pickle
import pickletools
import struct
import sys
import numpy as np
import cv2
import lzma
import time


class server:
    def __init__(self):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(('10.0.0.10',9999))
        self.buffer=io.BytesIO()
    def listen(self):
        self.server.listen(5)

        while True:
            conn,addr=self.server.accept()
            threading.Thread(target=self.send,args=(conn,)).start()
            self.send(conn)

    def send(self,conn : socket.socket):
        while True:
            try:
                img = ImageGrab.grab()
                s = img.size
                simg = img.tobytes()
                bimg=lzma.compress(simg)

                sb = bimg.__len__()
                sb2 = bimg.__sizeof__()
                #print(f'{sb}')

                pack = struct.pack(f'{sb}s', bimg)
                print(pack.__sizeof__())
                print(pack.__len__())
                sizeofpack=struct.calcsize(f'{sb}s')
                print(sizeofpack)

                conn.sendall(sizeofpack.to_bytes(4,sys.byteorder)+pack)
                time.sleep(10)
            except socket.error as err:
                print(err)
                conn.close()
                return




class client:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def connect(self):
        self.conn=socket.create_connection(('10.0.0.10',9999))
        threading.Thread(target=self.receive, args=(self.conn,)).start()

    def receive(self,conn : socket.socket):
        while True:
            pack_size_b = conn.recv(4)
            pack_size = int.from_bytes(pack_size_b, sys.byteorder)
            if not pack_size_b:
                continue

            pack=b''
            while len(pack)<pack_size:
                recvmsg=conn.recv(1024)
                pack = pack+recvmsg
                if not recvmsg:
                    break

            try:
                if len(pack)==pack_size:
                    unpack = struct.unpack(f'{len(pack)}s', pack)
                    limg=lzma.decompress(unpack[0])
                    cimg = Image.frombytes('RGB', (1920, 1080), limg)
                    #print(cimg.tobytes())
                    cimg.show()
                    pack = b''
                else:
                    pack=b''
                    pack_size_b=0
                    pack_size=0
                    continue

            except socket.error as err:
                print(err)
                conn.close()
                break
        return

if __name__=='__main__':
    ans=input('enter mode: ')
    if ans == 's':
        s=server()
        s.listen()
    elif ans=='c':
        c=client()
        c.connect()
