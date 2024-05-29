import modules
from utils import *
import asyncio
import datetime
import random

stopped = False

def signal_handler(sig, frame):
    global stopped
    stopped = True

def initialized_app(nearaccountfile):
    importedm = import_one_module(modules, "hotclaimnear")
    ins = None
    if importedm != None:
        # Create instance from the module
        ins = create_instances(importedm)
        if ins is None:
            print(f"Failed to create instance hotclaimnear")
        else:
            # Update the auth for instances
            ins.set_input_file(nearaccountfile)
    else:
        print(f"Failed to import module hotclaimnear")

    # Set up signal handler to catch Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    return ins

async def main(nearaccountfile):
    ins = initialized_app(nearaccountfile)
    while not stopped:
        await ins.claim_all()
        delay = ins.wait_time + random.randint(10, 60)
        sleeped_time = 0
        print(f'\nWait for {str(datetime.timedelta(seconds=delay))}. Press Ctrl+C to stop \n')
        while not stopped and sleeped_time < delay:
            time.sleep(1)
            sleeped_time = sleeped_time + 1

if __name__ == '__main__':
    asyncio.run(main("hotnear.json"))