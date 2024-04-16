from tkinter import *
import math
import win32api
from win32api import *
from win32con import *
from win32gui import *
import time
#for i in range(5):
    #keybd_event(175,57392)
#time.sleep(2)
#exit(0)

w_r=65535/500
h_r=65535/500
#hwnd = MonitorFromPoint((0,0), MONITOR_DEFAULTTOPRIMARY)
def click(event):
    print(f'{event}----{event.num}')

root=Tk()

frame=Frame(root)
canvas=Canvas(frame,width=500,height=500,bg='red')
frame.pack()
canvas.pack()
print(f'{GetSystemMetrics(0)}x{GetSystemMetrics(1)}')
canvas.focus_set()
canvas.bind('<Key>', lambda event: print(f'vc: {event.keycode} sc: {MapVirtualKey(event.keycode,4)}'))
canvas.bind('<Button>', click)
canvas.bind('<ButtonRelease>',click)

root.mainloop()
