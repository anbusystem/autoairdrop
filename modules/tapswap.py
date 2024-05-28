from .base import basetap
import requests
from datetime import datetime
import time


DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjU2MjQyNTgxOTQsImlhdCI6MTcxNjkwOTI0NywiZXhwIjoxNzE2OTEyODQ3fQ.IO35nSuv6-R3zgR9UB7-j6X7sjGM9wJ8Nj6ujZT91-0",
    "Content-Id": "5623748576",
    "DNT": "1",
    "Origin": "https://app.tapswap.club",
    "Referer": "https://app.tapswap.club/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "x-app": "tapswap_server",
    "x-cv": "607",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Content-Type": "application/json"
}

DEFAULT_AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjU2MjQyNTgxOTQsImlhdCI6MTcxNjkwOTI0NywiZXhwIjoxNzE2OTEyODQ3fQ.IO35nSuv6-R3zgR9UB7-j6X7sjGM9wJ8Nj6ujZT91-0"
# DEFAULT_AUTH = ""

url = "https://api.tapswap.ai/api/player/submit_taps"

class tapswap(basetap):
    def __init__(self, auth = DEFAULT_AUTH, proxy = None, headers = DEFAULT_HEADERS):
        super().__init__()
        self.auth = auth
        self.proxy = proxy
        self.headers = headers
        # self.headers["Authorization"] = auth
        self.stopped = False
        self.wait_time = 5
        self.name = self.__class__.__name__
        self.energy = 2000

    def login(self):
        url = "https://api.tapswap.ai/api/account/login"
        body = {
            "init_data": self.init_data_raw,
            "referrer": "",
            "bot_key": "app_bot_1"
        }
        try:
            response = requests.post(url, headers=self.headers, json=body, proxies=self.proxy)
            data = response.json()
            
            if "access_token" in data:
                self.auth = f"Bearer {data['access_token']}"
                self.update_header("Authorization", self.auth)
                self.bprint("Login success")
                self.energy = int(data['player']['energy'])
                # self.tap()
                return True
            self.bprint("Login failed")
        except Exception as e:
            self.bprint(e)
        return False

    def update_content_id(self, now):
        from decimal import Decimal
        now = Decimal(now)
        myid = Decimal(self.init_data["user"]["id"])
        contentid = (now * myid) % myid
        print(now)
        self.update_header("Content-Id", str(contentid))
        print(contentid)

    def tap(self):
        current_time_seconds = time.time()
        epoch_ms = int(current_time_seconds * 1000)
        self.update_content_id(1716912946864)
        data = {
            "taps": self.energy,
            "time": epoch_ms 
        }
        print(data)
        try:
            response = requests.post(url, headers=self.headers, json=data, proxies=self.proxy)
            data = response.json()
            print(data)
            if "statusCode" in data:
                self.bprint(f"Error: {data['message']}, try re-login")
                # self.login()
            else:
                self.print_balance(data['player']['shares'])
                self.energy = 10
        except Exception as e:
            self.bprint(e)

    def run(self):
        self.wait_time = 10
        while not self.stopped:
            self.tap()
            self.wait()
            break