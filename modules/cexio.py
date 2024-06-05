import requests
from .base import basetap
from datetime import datetime, timedelta, timezone

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

WAITING_FARM_HOUR = 4

class cexio(basetap):
    def __init__(self, proxy = None, headers = DEFAULT_HEADER):
        super().__init__()
        self.proxy = proxy
        self.headers = headers
        self.stopped = False
        self.wait_time = 20
        self.wait_time_farm = 4 * 60 * 60
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
            self.get_next_farm_waiting_time(data["data"]["farmStartedAt"])
            return data["data"]["availableTaps"]
        except Exception as e:
            self.bprint(e)
            return 0

    def get_next_farm_waiting_time(self, last_claim):
        last_claimed_dt = datetime.strptime(last_claim, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        next_claimed_dt = last_claimed_dt + timedelta(hours=WAITING_FARM_HOUR)
        current_time = datetime.now(timezone.utc)
        # Calculate the waiting time in seconds
        waiting_time_seconds = (next_claimed_dt - current_time).total_seconds()
        # Ensure the waiting time is not negative
        self.wait_time_farm = max(0, waiting_time_seconds)

    def try_claim(self, tapnum = 1):
        url = "https://cexp.cex.io/api/claimTaps"

        data = {
            "devAuthData": self.init_data["user"]["id"],
            "authData": self.init_data_raw,
            "data": {"taps": tapnum}
        }

        response = requests.post(url, headers=self.headers, json=data)


    def try_claim_farm(self):
        url = "https://cexp.cex.io/api/claimFarm"

        payload = {
            "devAuthData": self.init_data["user"]["id"],
            "authData": self.init_data_raw,
            "data": {}
        }

        response = requests.post(url, headers=self.headers, json=payload)
        data = response.json()
        if data["status"] == "ok":
            self.print_balance(float(data["data"]["balance"]))
            self.try_start_farm()

    def try_start_farm(self):
        url = "https://cexp.cex.io/api/startFarm"

        payload = {
            "devAuthData": self.init_data["user"]["id"],
            "authData": self.init_data_raw,
            "data": {}
        }

        response = requests.post(url, headers=self.headers, json=payload)
        data = response.json()
        if data["status"] == "ok":
            self.bprint("Start farm success")
            self.get_next_farm_waiting_time(data["data"]["farmStartedAt"])

    def tap(self):
        tapnum = self.get_balance_and_remain()
        if int(tapnum) > 0:
            self.try_claim(tapnum)
        else:
            self.bprint(f"No tap available, waiting {self.wait_time} seconds")

    def run(self):
        if not self.is_init_data_ready():
            self.bprint("Init data is required, please check config.json")
            return
        else:
            while self.stopped == False:
                self.tap()
                self.wait()
                if self.wait_time_farm <= 0:
                    self.try_claim_farm()

