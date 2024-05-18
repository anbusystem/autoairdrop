import signal
import time
import importlib
import pkgutil
import modules
import inspect


threads = []

stopped = False

def create_instances(module):
    global threads
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
                threads.append(obj())

def import_all_modules(package):
    global threads
    # Iterate through the package and import all modules
    package_name = package.__name__
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name != "base":
            full_module_name = f"{package_name}.{module_name}"
            importedm = importlib.import_module(full_module_name)
            create_instances(importedm)

def signal_handler(sig, frame):
    global stopped
    stopped = True

def main():
    global stop_threads

    import_all_modules(modules)

    # Set up signal handler to catch Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    for t in threads:
        t.start()

if __name__ == "__main__":
    main()
    while stopped == False:
        time.sleep(1)
    for t in threads:
        t.stop()
        t.join()