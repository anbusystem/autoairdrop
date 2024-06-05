import requests
import time
from .base import basetap

DEFAULT_HDRS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://www.yescoin.gold",
    "priority": "u=1, i",
    "referer": "https://www.yescoin.gold/",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1NjI0MjU4MTk0IiwiY2hhdElkIjoiNTYyNDI1ODE5NCIsImlhdCI6MTcxNjAxNDAyNiwiZXhwIjoxNzE4NjA2MDI2LCJyb2xlQXV0aG9yaXplcyI6W10sInVzZXJJZCI6MTc4MTYwMDE1NzY2NTUxMzQ3Mn0.lIzwptF434dMYW3x72AJQb7cfcKUCevn62K0RJKey4DJPeiXGItoaTr5T9Q88NJN0Y1AI7nIh5noJf8y2SIwgQ",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}
DEFAULT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1NjI0MjU4MTk0IiwiY2hhdElkIjoiNTYyNDI1ODE5NCIsImlhdCI6MTcxNjAxNDAyNiwiZXhwIjoxNzE4NjA2MDI2LCJyb2xlQXV0aG9yaXplcyI6W10sInVzZXJJZCI6MTc4MTYwMDE1NzY2NTUxMzQ3Mn0.lIzwptF434dMYW3x72AJQb7cfcKUCevn62K0RJKey4DJPeiXGItoaTr5T9Q88NJN0Y1AI7nIh5noJf8y2SIwgQ"

class yescoin(basetap):
    def __init__(self, token = DEFAULT_TOKEN, proxy = None, headers = DEFAULT_HDRS):
        super().__init__()
        self.token = token
        self.proxy = proxy
        self.headers = headers
        self.headers["token"] = self.token
        self.stopped = False
        self.name = self.__class__.__name__

    def get_remain_coin(self):
        url = "https://api.yescoin.gold/game/getGameInfo"
        try:
            res = requests.get(url, headers=self.headers, proxies=self.proxy)
            if res.status_code == 200:
                data = res.json()
                # print(f"{self.name}: {data}")
                return int(int(data["data"]["coinPoolLeftCount"]) / 10)
        except Exception as e:
            self.bprint(e)
        return 0
    
    
    def collect_coin(self, numcollect):
        url = "https://api.yescoin.gold/game/collectCoin"
        try:
            res = requests.post(url, headers=self.headers, data=str(numcollect), proxies=self.proxy)
            # print(f"{self.name}: {res.json()}")
        except Exception as e:
            self.bprint(e)

    def get_info(self):
        url = "https://api.yescoin.gold/account/getAccountInfo"
        try:
            res = requests.get(url, headers = self.headers, proxies=self.proxy)
            self.print_balance(res.json()['data']['currentAmount'])
            # print(f"{self.name}: Account balance {res.json()['data']['currentAmount']}")
        except Exception as e:
            self.bprint(e)

    def claim(self):
        remain_coin = self.get_remain_coin()
        self.collect_coin(remain_coin)
        self.get_info()

    def parse_config(self, cline):
        self.update_header("token", cline["token"])