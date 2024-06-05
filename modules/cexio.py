import requests
from .base import basetap

DEFAULT_HEADER = {
    "authority": "cexp.cex.io",
    "method": "POST",
    "path": "/api/claimTaps",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "dnt": "1",
    "origin": "https://cexp.cex.io",
    "priority": "u=1, i",
    "referer": "https://cexp.cex.io/",
    "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}

class cexio(basetap):
    def __init__(self, proxy = None, headers = DEFAULT_HEADER):
        super().__init__()
        self.proxy = proxy
        self.headers = headers
        self.stopped = False
        self.wait_time = 20
        self.name = self.__class__.__name__

    def get_balance_and_remain(self):
        url = "https://cexp.cex.io/api/getUserInfo"
        data = {
            "devAuthData": self.init_data["user"]["id"],
            "authData": self.init_data_raw,
            "platform": "android",
            "data": {}
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            data = response.json()
            self.print_balance(float(data["data"]["balance"]))
            return data["data"]["availableTaps"]
        except Exception as e:
            self.bprint(e)
            return 0


    def try_claim(self, tapnum = 1):
        url = "https://cexp.cex.io/api/claimTaps"

        data = {
            "devAuthData": self.init_data["user"]["id"],
            "authData": self.init_data_raw,
            "data": {"taps": tapnum}
        }

        response = requests.post(url, headers=self.headers, json=data)

    
    def claim(self):
        if not self.is_init_data_ready():
            self.bprint("Init data is required, please check config.json")
        else:
            tapnum = self.get_balance_and_remain()
            if int(tapnum) > 0:
                self.try_claim(tapnum)
            else:
                self.bprint(f"No tap available, waiting {self.wait_time} seconds")