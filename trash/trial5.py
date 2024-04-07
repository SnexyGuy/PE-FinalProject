import numpy as np
import cv2
from mss import mss
from PIL import Image
import socket



bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)
    cv2.imshow('screen', np.array(sct_img))


    if cv2.waitKey(5) & 0xFF == 27:
        cv2.destroyAllWindows()
        break