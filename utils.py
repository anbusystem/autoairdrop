import signal
import time
import sys
import json
import importlib
import pkgutil
import inspect
from enum import Enum

def create_instances(module):
	for name, obj in inspect.getmembers(module):
		if inspect.isclass(obj) and obj.__module__ == module.__name__:
				return obj()
	return None

def import_one_module(package, mname):
	package_name = package.__name__
	for _, module_name, _ in pkgutil.iter_modules(package.__path__):
		if module_name == mname:
			full_module_name = f"{package_name}.{module_name}"
			importedm = importlib.import_module(full_module_name)
			return importedm
	return None

class CONFIG(Enum):
	ACCOUNT = "accounts"
	PROXY = "proxy"
	THREAD = "thread"

class SUBCONFIG(Enum):
	COIN = "coin"
	INITDATA = "initdata"
	HDRFIELD = "type"
	HDRTOKEN = "auth"
	PROXYFILE = "proxyfile"
	PROXYTYPE = "proxytype"
	PROXYMODE = "proxymode"
	PROXYDIEACTION = "proxydie"
	PROXYDIEACTIONSTOP = "STOP"
	PROXYDIEACTIONSKIP = "SKIP"
	PROXYROT = "ROT"
	THREADMODE = "threadmode"
	THREADMODESPAWNALL = "SPAWN_ALL"
	THREADMODEPOOL = "THREAD_POOL"
	THREADNUMBER = "thread_number"

class ConfigParser:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(ConfigParser, cls).__new__(cls)
		return cls._instance

	def __init__(self, cfile="config.json"):
		if not hasattr(self, '_initialized'):  # Check if already initialized
			self.cfg = {}
			self.cfile = cfile
			try:
				with open(cfile) as f:
					self.cfg = json.loads(f.read())
					self.cfgvalid = True
			except Exception as e:
				self.cfgvalid = False
			self._initialized = True

	def get(self, cname, scname=None):
		if cname in self.cfg:
			data = self.cfg[cname]
			if scname is not None and scname in data:
				return data[scname]
			else:
				return data
		else:
			return None

	def set(self, cname, data):
		self.cfg[cname] = data

	def __del__(self):
		with open(self.cfile, "w") as f:
			f.write(json.dumps(self.cfg))

class proxyhelper:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(ConfigParser, cls).__new__(cls)
		return cls._instance

	def __init__(self, cfile):
		if not hasattr(self, '_initialized'):  # Check if already initialized
			self.cfg = ConfigParser(cfile)
			self.proxymode = self.cfg.get(CONFIG.PROXY.value, SUBCONFIG.PROXYMODE.value)
			self.proxyfile = self.cfg.get(CONFIG.PROXY.value, SUBCONFIG.PROXYFILE.value)
			self.proxydieaction = self.cfg.get(CONFIG.PROXY.value, SUBCONFIG.PROXYDIEACTION.value)
			self.proxytype = self.cfg.get(CONFIG.PROXY.value, SUBCONFIG.PROXYTYPE.value)
			self._initialized = True
	
