import pickle
import lzma
from PIL import ImageGrab, ImageTk



def send_screen():
    screen=ImageGrab.grab()
    pickled_screen=pickle.dumps(screen)
    compressed_screen=lzma.compress(pickled_screen)
    return compressed_screen



def receive_screen(compressed_screen):
    uncompressed_screen=pickle.loads(compressed_screen)
    unpickled_screen=pickle.loads(uncompressed_screen)
    screen=ImageTk.PhotoImage(unpickled_screen)
    return screen


