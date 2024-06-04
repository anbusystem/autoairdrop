import threading
import time
import json
import modules
from utils import *
import urllib.parse


class worker(threading.Thread):
    # inqueue: give me a queue, I will get the config line
    def __init__(self, inqueue, registercb):
        threading.Thread.__init__(self)
        self.q = inqueue
        self.cb = registercb
        self.running = True
        self.coin = None
    
    def stop(self):
        self.running = False

    def validate_cline(self, cline):
        try:
            self.coin = cline['coin']
            self.params = cline
            return True
        except Exception as e:
            return False            
    
    def run(self):
        while self.running:
            cline = self.q.get()
            if self.validate_cline(cline):
                ins = create_instances(import_one_module(modules, self.coin))
                ins.set_params(self.params)
                ins.claim()
            

    