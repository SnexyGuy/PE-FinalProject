import pickle
import lzma
from PIL import ImageGrab, ImageTk
import sys
import numpy as np



def send_screen():
    screen=ImageGrab.grab()
    pickled_screen=pickle.dumps(screen)
    compressed_screen=lzma.compress(pickled_screen)
    return compressed_screen



def receive_screen(compressed_screen):
    uncompressed_screen=lzma.decompress(compressed_screen)
    unpickled_screen=pickle.loads(uncompressed_screen)
    return unpickled_screen



