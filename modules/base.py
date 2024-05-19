import threading
import time

TIME_WAIT = 10

def print_green_line(line):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{GREEN}{line}{RESET}")

class basetap(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = False
        self.wait_time = TIME_WAIT
        self.name = self.__class__.__name__
        self.oldbalance = 0
        self.headers = {}

    def update_header(self, k, v):
        self.headers[k] = v

    def stop(self):
        self.stopped = True
        print(f"{self.name}: stopped" )

    def print_balance(self, bl):
        if int(bl) > self.oldbalance:
            print_green_line(f"{self.name}: Account balance {bl} ^")
            self.oldbalance = int(bl)
        else:
            print(f"{self.name}: Account balance {bl}")

    def bprint(self, msg):
        print(f"{self.name}: {msg}")

    def wait(self):
        print(f"{self.name}: wait {self.wait_time}s" )
        sleeped = 0
        while sleeped < self.wait_time and self.stopped == False:
            time.sleep(1)
            sleeped = sleeped + 1
    
    def tap(self):
        print("You should implement this function")

    def set_proxy(self, proxy):
        self.proxy = proxy


    def run(self):
        while self.stopped == False:
            self.tap()
            self.wait()
        return