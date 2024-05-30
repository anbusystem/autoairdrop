from .base import basetap
import requests
from datetime import datetime
import time
import struct

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
def to_js_float64(value):
    """Convert a large integer to a float64 representation, simulating JavaScript precision issues."""
    return struct.unpack('d', struct.pack('d', float(value)))[0]

def js_modulo(a, b):
    """Simulate JavaScript modulo operation for large integers with precision issues."""
    a_js = to_js_float64(a)
    b_js = to_js_float64(b)
    result = (a_js * b_js) % a_js
    return result

url = "https://api.tapswap.ai/api/player/submit_taps"

class tapswap(basetap):
    def __init__(self, auth = DEFAULT_AUTH, proxy = None, headers = DEFAULT_HEADERS):
        super().__init__()
        self.auth = auth
        self.proxy = proxy
        self.headers = headers
        # self.headers["Authorization"] = auth
        self.stopped = False
        self.wait_time = 5*60
        self.name = self.__class__.__name__
        self.energy = 2000
        self.remain_boost = {"energy" : 0, "turbo" : 0}
        self.last_boost_time = {"energy" : 0, "turbo" : 0}

    def apply_boost(self, boosttype, curtime):
        url = "https://api.tapswap.ai/api/player/apply_boost"
        if self.remain_boost[boosttype] > 0:
            body = {
                "type" : boosttype
            }
            try:
                response = requests.post(url, headers=self.headers, json=body, proxies=self.proxy)
                data = response.json()
                if "statusCode" in data:
                    self.bprint(f"Try to claim boost {boosttype} but failed {data['message']}")
                    self.wait_time = 5*60
                    return False
                else:
                    self.last_boost_time[boosttype] = curtime
                    self.bprint(f"Claim boost {boosttype} success")
                    self.wait_time = 1
                return True
            except Exception as e:
                self.bprint(f"Some thing wrong {e}")
                self.wait_time = 5*60
                return False
        else:
            self.bprint("No more boost")
            self.wait_time = 5*60
            return False

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
                self.remain_boost["energy"] = int(data['player']['boost'][0]['cnt'])
                self.remain_boost["turbo"] = int(data['player']['boost'][1]['cnt'])
                self.tap(fromlogin=True)
                return True
            self.bprint("Login failed")
        except Exception as e:
            self.bprint(e)
        return False

    def update_content_id(self, now):
        myid = self.init_data["user"]["id"]
        contentid = int(js_modulo(myid, now))
        self.update_header("Content-Id", str(contentid))

    def tap(self, fromlogin = False):
        current_time_seconds = time.time()
        epoch_ms = int(current_time_seconds * 1000)
        self.update_content_id(epoch_ms)
        data = {
            "taps": self.energy,
            "time": epoch_ms 
        }
        try:
            self.apply_boost("energy")
            # self.apply_boost("turbo")
            response = requests.post(url, headers=self.headers, json=data, proxies=self.proxy)
            data = response.json()
            if "statusCode" in data:
                if fromlogin:
                    self.bprint(f"Error {data['message']}, stop looping since code is failed")
                    self.stopped = True
                else:
                    self.bprint(f"Error: {data['message']}, try re-login")
                    self.login()
            else:
                self.print_balance(data['player']['shares'])
                self.energy = 10
                self.remain_boost["energy"] = int(data['player']['boost'][0]['cnt'])
                self.remain_boost["turbo"] = int(data['player']['boost'][1]['cnt'])
        except Exception as e:
            self.bprint(e)

    def run(self):
        while self.stopped == False:
            self.tap()
            self.wait()
        return


if __name__ == "__main__":
    obj = tapswap()
    obj.init_data_raw = "query_id=AAGSXjtPAgAAAJJeO0_t0i5G&user=%7B%22id%22%3A5624258194%2C%22first_name%22%3A%22Evis%22%2C%22last_name%22%3A%22The%20Cat%22%2C%22username%22%3A%22rokbotsxyz%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1716909225&hash=109f0f7fbe349f2d9e6e563734735131a56bc9942955c5e162352d5a7bbad9fe"
    obj.init_data = {
        "user" : {
            "id" : 5624258194
        }
    }
    obj.tap()