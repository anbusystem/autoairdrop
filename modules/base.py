import threading
import time
import json
import random
import urllib.parse

TIME_WAIT = 10
MODULE_VER = "2.1"
def print_green_line(line):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{GREEN}{line}{RESET}")

class basetap:
    def __init__(self):
        self.stopped = False
        self.wait_time = TIME_WAIT
        self.name = self.__class__.__name__
        self.oldbalance = 0
        self.headers = {}
        self.init_data = {}
        self.init_data_raw = ""
        self.init_data_load = False
        self.modver = "v1.0"

    def set_ua(self, ua):
        uastr = ua
        if isinstance(ua, str):
            pass
        else:
            uastr = ua()
        self.update_header("User-Agent", uastr)
        self.update_header("user-agent", uastr)
            
    def parse_config(self, cline):
        self.bprint("You should implement the parse config function")

    def parse_init_data(self, initdata):
        initstr = ""
        data = initdata.split("&")
        for d in data:
            k,v = d.split("=")
            self.init_data[k] = v
            initstr += k + "=" + urllib.parse.quote(v, safe='') + "&"
        self.init_data_raw = initstr
        self.init_data_load = True
    
    def parse_init_data_raw(self, rawdata):
        data = rawdata.split("&")
        for d in data:
            try:
                k,v = d.split("=")
                if k == "user":
                    v = json.loads(urllib.parse.unquote(v))
                self.init_data[k] = v
            except Exception as e:
                pass
        self.init_data_raw = rawdata
        self.init_data_load = True

    def is_init_data_ready(self):
        return self.init_data_load

    def update_header(self, k, v):
        self.headers[k] = v

    def set_proxy(self, proxy):
        self.proxy = proxy

    def stop(self):
        self.stopped = True
        print(f"{self.name}: stopped" )

    def set_name(self, myname):
        self.name = myname

    def print_balance(self, bl):
        if int(bl) > self.oldbalance:
            print_green_line(f"{self.name}: Balance 💎: {bl} ^")
            self.oldbalance = int(bl)
        else:
            print(f"{self.name}: Balance 💎: {bl}")

    def bprint(self, msg):
        print(f"{self.name}: {msg}")

    def wait(self):
        print(f"{self.name}: wait {self.wait_time}s" )
        sleeped = 0
        while sleeped < self.wait_time and self.stopped == False:
            time.sleep(1)
            sleeped = sleeped + 1
    
    def claim(self):
        self.bprint("You should implement this function")

    def set_proxy(self, proxy):
        self.proxy = proxy

    
if __name__ == "__main__":
    obj = basetap()
    data_raw = "query_id=AAGSXjtPAgAAAJJeO0_2-sHt&user=%7B%22id%22%3A5624258194%2C%22first_name%22%3A%22Evis%22%2C%22last_name%22%3A%22The%20Cat%22%2C%22username%22%3A%22rokbotsxyz%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1716722443&hash=40fe84e8f626ff0fa74c3f0e7c51c677fac5da8b27a0fc8ddd0fb5cdc5ace2a3"
    data = data_raw.split("&")
    init_data = {}
    for d in data:
        k,v = d.split("=")
        
        if k == "user":
            v = json.loads(urllib.parse.unquote(v))
        
        init_data[k] = v
    print(init_data["user"]["id"])