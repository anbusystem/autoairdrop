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

DEFAULT_AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjU2MjQyNTgxOTQsImlhdCI6MTcxNjA4OTQ5MSwiZXhwIjoxNzE2MDkzMDkxfQ.XPDJNCjCdfKCYCG4qG2sbyZ3OxbVHhKu03Dk-m0zDNM"
# DEFAULT_AUTH = ""

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

    def login(self):
        url = "https://api.tapswap.ai/api/account/login"
        body = {
            "init_data": "query_id=AAGSXjtPAgAAAJJeO08e-d2Q&user=%7B%22id%22%3A5624258194%2C%22first_name%22%3A%22Evis%22%2C%22last_name%22%3A%22The%20Cat%22%2C%22username%22%3A%22rokbotsxyz%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1716089488&hash=ba05d58996c1e60ebbe10e126fc7bf0a3f1c7a70ba98c8d2a368d0e5bd97b251",
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
                self.tap()
                return True
            self.bprint("Login failed")
        except Exception as e:
            self.bprint(e)
        return False


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
            if "statusCode" in data:
                self.bprint(f"Error: {data['message']}, try re-login")
                self.login()
            else:
                self.print_balance(data['player']['shares'])
        except Exception as e:
            self.bprint(e)