import signal
import time
import sys
import importlib
import pkgutil
import modules
import inspect
import json
from moduleutils import *


threads = []
stopped = False

def signal_handler(sig, frame):
    global stopped
    stopped = True

def load_config():
    with open("config.json") as f:
        data = f.read()
        try:
            config = json.loads(data)
            return config
        except Exception as e:
            print("The config.json is wrong")
    return None

def initialized_app():
    global threads

    # Load config.json
    config = load_config()
    if config == None:
        print("Exit")
        sys.exit(1)

    cnt = 0
    # Create instances according to config
    for c in config:
        try:
            # Import module, make sure module is existed
            importedm = import_one_module(modules, c["coin"])
            if importedm != None:
                # Create instance from the module
                ins = create_instances(importedm)
                if ins is None:
                    print(f"Failed to create instance {c['coin']}")
                else:
                    # Update the auth for instances
                    ins.update_header(c["type"], c["auth"])
                    ins.set_name(f"{c['coin']}#{cnt}")
                    cnt = cnt + 1
                    # Save to global threads
                    threads.append(ins)
            else:
                print(f"Failed to import module {c['coin']}")
        except Exception as e:
            print(e)
            sys.exit(1)

    # Set up signal handler to catch Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
   

if __name__ == "__main__":
    # Init all the thread
    initialized_app()
    # Start all the thread
    for t in threads:
        t.start()
        time.sleep(1)
    # Wait until ctrl+C is press
    while stopped == False:
        time.sleep(1)
    # Close the main function
    for t in threads:
        t.stop()
        # t.join()