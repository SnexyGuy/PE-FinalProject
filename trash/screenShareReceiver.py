# Import socket module
import socket
from PIL import Image
import pickle
import lzma

# Create a socket object
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Define the port on which you want to connect


# connect to the server on local computer
s.connect(('10.0.0.9', 9999))

# receive data from the server and decoding to get the string.
imag =b''
while True:
    data=s.recv(4096)
    if not data:
        break
    imag=imag+data

#image=Image.open(image)
image=pickle.loads(imag)
image.show()
# close the connection
s.close()