from py_near.account import Account
import sys
import json
from py_near.dapps.core import NEAR

class hotclaimnear():
    def __init__(self):
        self.wait_time = 2*60*60
        self.acclist = []
        self.inputvalid = False
        self.name = self.__class__.__name__
        self.rpc = "https://rpc.mainnet.near.org"
    
    def set_input_file(self, input):
        try:
            with open(input) as f:
                data = f.read()
                self.acclist = json.loads(data)
                self.inputvalid = True
        except Exception as e:
            print("Data input is wrong")

    def set_input_data(self, acclist):
        self.acclist = acclist
        self.inputvalid = True

    async def claim(self, accid, privkey):
        nearaccount = Account(
            accid,
            privkey,
            rpc_addr=self.rpc
        )
        await nearaccount.startup()
        txn = await nearaccount.function_call(
            'game.hot.tg',
            'claim',
            {},
            gas=30000000000000
        )
        print(txn.transaction_outcome.__dict__)
        acc_balance = await nearaccount.get_balance()
        print(f"Balance: {acc_balance / NEAR}")

    async def claim_all(self):
        if not self.inputvalid:
            print("Input file is required, check hotnear.json")
            sys.exit(1)
        for k,v in self.acclist.items():
            await self.claim(k, v)