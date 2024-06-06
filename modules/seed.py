import requests
from .base import basetap
from datetime import datetime, timedelta, timezone

DEFAULT_HEADER = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'cache-control': 'no-cache',
    'origin': 'https://cf.seeddao.org',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

class seed(basetap):
    def __init__(self, proxy = None, headers = DEFAULT_HEADER):
        super().__init__()
        self.proxy = proxy
        self.headers = headers
        self.stopped = False
        self.wait_time = 20
        self.name = self.__class__.__name__

    def get_mine_time(self, storage_level):
        x = int(storage_level)
        return {
            0 : 2,
            1 : 3,
            2 : 4,
            3: 6,
            4: 12,
            5 : 24
        }[x]

    def get_next_waiting_time(self, last_claim, storage_level):
        mining_time = self.get_mine_time(storage_level)
        last_claimed_dt = datetime.strptime(last_claim, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        next_claimed_dt = last_claimed_dt + timedelta(hours=mining_time)
        current_time = datetime.now(timezone.utc)
        # Calculate the waiting time in seconds
        waiting_time_seconds = (next_claimed_dt - current_time).total_seconds()
        # Ensure the waiting time is not negative
        self.wait_time = max(0, waiting_time_seconds)

    def print_waiting_time(self):
        # Convert seconds to hours and minutes
        hours, remainder = divmod(self.wait_time, 3600)
        minutes, _ = divmod(remainder, 60)
        self.bprint(f"Waiting time: {int(hours)} hours and {int(minutes)} minutes")

    def get_profile(self):
        url = "https://elb.seeddao.org/api/v1/profile"

        try:
            response = requests.get(url, headers=self.headers)
            data = response.json()

            # Extract upgrades from the data source
            upgrades = data.get("data", {}).get("upgrades", [])

            # Filter storage-size upgrades and find the highest upgrade level
            highest_storage_level = max(
                (upgrade['upgrade_level'] for upgrade in upgrades if upgrade.get('upgrade_type') == 'storage-size'),
                default=0
            )

            self.get_next_waiting_time(data["data"]["last_claim"], highest_storage_level)
            if self.wait_time > 0:
                self.print_waiting_time()
        except Exception as e:
            self.bprint(e)

    def try_claim(self):
        url = "https://elb.seeddao.org/api/v1/seed/claim"
        try:
            response = requests.post(url, headers=self.headers)
            data = response.json()
            if int(data["data"]["amount"]) > 0:
                self.bprint("Claim success")
            self.print_balance(float(data["data"]["amount"]))
            self.get_profile()
        except Exception as e:
            self.bprint(e)

    def run(self):
        if not self.is_init_data_ready():
            self.bprint("Init data is required, please check config.json")
            return
        else:
            self.headers["telegram-data"] = self.init_data_raw
            while self.stopped == False:
                self.get_profile()
                self.wait()
                if self.wait_time <= 0:
                    self.try_claim()
