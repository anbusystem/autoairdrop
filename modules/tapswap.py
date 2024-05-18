from .base import basetap
import requests
import datetime


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjU2MjQyNTgxOTQsImlhdCI6MTcxNjA0MzA3MiwiZXhwIjoxNzE2MDQ2NjcyfQ.ergSCrUj6PI8jluA3d-j69otpNDq97iPvBZqOZ7G2nU",
    "Content-Id": "783954",
    "DNT": "1",
    "Origin": "https://app.tapswap.club",
    "Referer": "https://app.tapswap.club/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "x-app": "tapswap_server",
    "x-cv": "1"
}

DEFAULT_AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjU2MjQyNTgxOTQsImlhdCI6MTcxNjA0MzA3MiwiZXhwIjoxNzE2MDQ2NjcyfQ.ergSCrUj6PI8jluA3d-j69otpNDq97iPvBZqOZ7G2nU"


url = "https://api.tapswap.ai/api/player/submit_taps"

class tapswap(basetap):
    def __init__(self, auth = DEFAULT_AUTH, proxy = None, headers = DEFAULT_HEADERS):
        super().__init__()
        self.auth = auth
        self.proxy = proxy
        self.headers = headers
        self.headers["Authorization"] = auth
        self.stopped = False
        self.wait_time = 5
        self.name = self.__class__.__name__

    def tap(self):
        current_time = datetime.datetime.now()
        current_timestamp = int(current_time.timestamp())
        data = {
            "taps": 10,
            "time": current_timestamp
        }
        try:
            response = requests.post(url, headers=self.headers, json=data, proxies=self.proxy)
            data = response.json()
            self.print_balance(data['player']['shares'])
        except Exception as e:
            print(e)