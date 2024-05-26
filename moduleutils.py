import signal
import time
import sys
import importlib
import pkgutil
import inspect

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