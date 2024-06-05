import numpy as np
from PIL import ImageGrab
import io
import sys
import lz4.frame
import _compression


img=ImageGrab.grab()

img_b=img.tobytes()

img_arr=np.array(img)
img_arr_b=img_arr.tobytes()

compressed_img = io.BytesIO()
np.savez_compressed(compressed_img, img=img_b)

cmprs=compressed_img.getvalue()

compressed_img.seek(0)

decompressed_img = np.load(compressed_img)['img']

decompressed_img_b=bytes(decompressed_img)

img_lz4=lz4.frame.compress(img_b)

print(len(img_arr))
print(len(img_arr_b))
print(len(cmprs))
print(len(decompressed_img))
print(len(decompressed_img_b))
