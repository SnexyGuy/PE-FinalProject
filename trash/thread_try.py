import threading
import time
event=threading.Event()

def func():
    while True:
        count=1
        if event.is_set():
            print('end')
            return


t=threading.Thread(target=func)
t.start()
print(t)
print(t.ident)
time.sleep(5)
event.set()