# first of all import the socket library
import socket
from PIL import ImageGrab
import pickle
import sys
import lzma
import threading
# next create a socket object
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything


# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('10.0.0.10', 9999))
print('socket binded')

# put the socket into listening mode
s.listen(5)
print("socket is listening")


def send_d(conn):
    while True:
        im = ImageGrab.grab()

        img = pickle.dumps(im)

        img = lzma.compress(img)
        try:
            conn.send(img)
        except socket.error as err:
            print(f'ERROR: {err}')
            conn.close()
            break
    # Close the connection with the client
    # Breaking once connection closed
    return

# a forever loop until we interrupt it or
# an error occurs

while True:
    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)
    sender=threading.Thread(target=send_d, args=(c,))
    sender.start()
    break
    # send a thank you message to the client. encoding to send byte type.

