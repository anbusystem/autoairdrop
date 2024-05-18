from .base import basetap
import requests


import requests

# Define the URL
url = "https://api0.herewallet.app/api/v1/user/hot/claim"

# Define the headers
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjQyMjIxMjYsImRpZCI6MjY4NDQ1NTIsImRldmljZSI6bnVsbCwiYWNjb3VudF9pZCI6InJva2JvdHN4eXoudGciLCJkZXZpY2VfaWQiOiIwNWIxNWIyNS03NDliLTRkNDEtOGU4Ny1hNTM1MWRmZjU1MWMiLCJwbGF0Zm9ybSI6InRlbGVncmFtIiwidGltZXN0YW1wIjoxNzEzNDIzOTk0LjAsInZpZXdfb25seSI6ZmFsc2V9.b1CIy0P8XELdqznWOhEGyfxShomq_SvS6IWrG_2exY4",
    "DNT": "1",
    "DeviceId": "05b15b25-749b-4d41-8e87-a5351dff551c",
    "Network": "mainnet",
    "Origin": "https://tgapp.herewallet.app",
    "Platform": "telegram",
    "Referer": "https://tgapp.herewallet.app/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Telegram-Data": "user=%7B%22id%22%3A5624258194%2C%22first_name%22%3A%22Evis%22%2C%22last_name%22%3A%22The%20Cat%22%2C%22username%22%3A%22rokbotsxyz%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=-1620440846169792460&chat_type=sender&auth_date=1716039450&hash=1d229b537447e27e27b6bf800377cc1021e5262fcccc7ff8c6bbeccd8e0f3ee4",
    "is-sbt": "false",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}

DEFAULT_AUTH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjQyMjIxMjYsImRpZCI6MjY4NDQ1NTIsImRldmljZSI6bnVsbCwiYWNjb3VudF9pZCI6InJva2JvdHN4eXoudGciLCJkZXZpY2VfaWQiOiIwNWIxNWIyNS03NDliLTRkNDEtOGU4Ny1hNTM1MWRmZjU1MWMiLCJwbGF0Zm9ybSI6InRlbGVncmFtIiwidGltZXN0YW1wIjoxNzEzNDIzOTk0LjAsInZpZXdfb25seSI6ZmFsc2V9.b1CIy0P8XELdqznWOhEGyfxShomq_SvS6IWrG_2exY4"

# Define the JSON body
body = {
    "game_state": {
        "refferals": 2,
        "inviter": "anhtuan8792.tg",
        "village": "14592.village.hot.tg",
        "last_claim": 1716020448235627800,
        "firespace": 3,
        "boost": 14,
        "storage": 21,
        "balance": 3875578
    }
}


class hotclaim(basetap):
    def __init__(self, auth = DEFAULT_AUTH, proxy = None, headers = DEFAULT_HEADERS):
        super().__init__()
        self.auth = auth
        self.proxy = proxy
        self.headers = headers
        self.headers["Authorization"] = auth
        self.stopped = False
        self.wait_time = 60*60*3
        self.name = self.__class__.__name__

    def tap(self):
        try:
            response = requests.post(url, headers=self.headers, json=body, proxies=self.proxy)
            data = response.json()
            self.print_balance(data['hot_in_storage'])
        except Exception as e:
            print(e)

    def run(self):
        while self.stopped == False:
            self.tap()
            self.wait()
        return