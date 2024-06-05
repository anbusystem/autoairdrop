import threading
import time
import json
import modules
from utils import *
import urllib.parse
import sys
import queue


class worker(threading.Thread):
	# inqueue: give me a queue, I will get the config line
	def __init__(self, inqueue, registercb, request_locking = None):
		threading.Thread.__init__(self)
		self.q = inqueue
		self.cb = registercb
		if self.validate_cb() == False:
			print("The callback much be a function with 2 arguments")
			sys.exit(1)
		self.running = True
		self.coin = None
		self.lock_request = request_locking
	
	def stop(self):
		self.running = False

	def validate_cb(self):
		if not callable(self.cb):
			return False

		# Check if the object is a function or a method with two parameters
		sig = inspect.signature(self.cb)
		return len(sig.parameters) == 2

	def validate_cline(self, cline):
		try:
			self.coin = cline['coin']
			self.params = cline
			return True
		except Exception as e:
			return False
	 
	def acquire_lock(self):
		if self.lock_request:
			self.lock_request.acquire()
		
	def release_lock(self):
		if self.lock_request and self.lock_request.locked():
			self.lock_request.release()

	def run(self):
		while self.running:
			try:
				cline = self.q.get_nowait()
			except queue.Empty:
				time.sleep(1)
				continue
			try:
				if self.validate_cline(cline):
					self.acquire_lock()
					ins = create_instances(import_one_module(modules, self.coin))
					ins.parse_config(self.params)
					ins.claim()
					if self.cb:
						print(f"Waing {ins.wait_time} seconds for next run")
						self.cb(ins.wait_time, self.params)
					self.release_lock()
			except Exception as e:
				ins.bprint(e)
				print("Exception happen, please check the code")
				self.release_lock()
			finally:
				self.release_lock()
			self.q.task_done()

			

	