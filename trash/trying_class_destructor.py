import threading
import time

class StringPrinter:
    def __init__(self, string_to_print):
        self.string_to_print = string_to_print
        self._running = threading.Event()
        self._thread = threading.Thread(target=self._print_string)
        self._thread.start()

    def _print_string(self):
        while True:
            if self._running.is_set():
                break
            print(self.string_to_print)
            time.sleep(1)  # Adding a sleep to avoid flooding the console


    def stop(self):
        self._running.set()
        self._thread.join()

    def __del__(self):
        self.stop()


# Example usage:
if __name__ == "__main__":
    sp = StringPrinter("Hello, World!")
    time.sleep(5)  # Let it print for 5 seconds
    sp.__del__() # Destructor will be called here, stopping the thread
