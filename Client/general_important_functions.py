import socket
import sys
import threading

# function that ensures all data received ---> returns all data


def recv_all(conn : socket.socket):
    data=b''
    pck_sz= conn.recv(8)
    size=int.from_bytes(pck_sz,sys.byteorder)
    while len(data)<size:
        data=data+conn.recv(size-len(data))
        if len(data)==size:
            break
    return data


# functions to handle closing and activating threads

thread_event_array : dict[threading.Thread.ident,threading.Event] = {}


def thread_event_setter(thread_id : threading.Thread.ident):
    thread_event_array.update({thread_id : threading.Event()})


def thread_event_remove(thread_id: threading.Thread.ident):
    thread_event_array.pop(thread_id)


def thread_closer(thread_id : threading.Thread.ident):
    thread_event_array[thread_id].set()


def end_all_threads():
    for thread in list(thread_event_array):
        thread_event_array[thread].set()


def delete_all_thread_flags():
    thread_event_array.clear()


def check_thread_flag(thread_id):
    if thread_id in thread_event_array and thread_event_array[thread_id].is_set():
        return True
    else:
        return False