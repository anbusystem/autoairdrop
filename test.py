import signal
import time
import importlib
import pkgutil
import modules
import inspect

threads = []

def create_instances(module):
	global threads
	for name, obj in inspect.getmembers(module):
		if inspect.isclass(obj) and obj.__module__ == module.__name__:
				threads.append(obj())

def import_all_modules(package, mname):
	global threads
	# Iterate through the package and import all modules
	package_name = package.__name__
	for _, module_name, _ in pkgutil.iter_modules(package.__path__):
		if module_name != "base" and module_name == mname:
			full_module_name = f"{package_name}.{module_name}"
			importedm = importlib.import_module(full_module_name)
			create_instances(importedm)



if __name__ == "__main__":
	mname = "yescoin"
	import_all_modules(modules, mname)
	for t in threads:
		t.tap()