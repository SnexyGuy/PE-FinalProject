import numpy as np
from PIL import ImageGrab,Image
import lzma
import struct


img=ImageGrab.grab()
s=img.size
bimg=img.tobytes()


sb=bimg.__len__()
sb2=bimg.__sizeof__()
#print(f'{sb}  {sb2}')


pack=struct.pack(f'i{sb}s',sb,bimg)
#print(pack)

unpack=struct.unpack(f'i{pack.__len__()-4}s',pack)




print(unpack[0])

cimg=Image.frombytes('RGB',(1920,1080),unpack[1])
cimg.show()
