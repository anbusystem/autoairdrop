import requests
from datetime import datetime
import time
import pytz
from .base import basetap

DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "authority": "game-domain.blum.codes",
    "method": "POST",
    "path": "/api/v1/game/play",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6ImZkMmVkOWIyLTQxYTAtNDBkZC05N2YyLTU3YjNjMzA5NjU1YSIsImV4cCI6MTcxNzY4MTUxMCwiaWF0IjoxNzE3Njc3OTEwfQ.T90sFimauS_Prg2uJUdLqyzbeYrsqIkSKuvAGiNfAQw",
    "dnt": "1",
    "origin": "https://telegram.blum.codes",
    "priority": "u=1, i",
    "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}

class blump(basetap):
    def __init__(self, proxy = None, headers = DEFAULT_HEADER):
        super().__init__()
        self.proxy = proxy
        self.headers = headers
        self.stopped = False
        self.wait_time = 20
        self.name = self.__class__.__name__
        self.remain_play_pass = 0

    
    def play_game(self):
        url = "https://game-domain.blum.codes/api/v1/game/play"
        try:
            res = requests.post(url, headers=self.headers)
            data = res.json()
            if "gameId" in data:
                gameid = data["gameId"]
                body = {
                    "gameId": gameid,
                    "points": 300000
                }
                url = "https://game-domain.blum.codes/api/v1/game/claim"
                time.sleep(31)
                res = requests.post(url, headers=self.headers, json=body)
        except Exception as e:
            self.bprint(e)
    
    def get_balance_info(self):
        url = "https://game-domain.blum.codes/api/v1/user/balance"
        try:
            res = requests.get(url, headers=self.headers, proxies=self.proxy)
            data = res.json()
            if "playPasses" in data:
                self.print_balance(float(data['availableBalance']))
                self.remain_play_pass = int(data['playPasses'])
                if self.remain_play_pass > 0:
                    self.bprint("Start hacking game")
                    self.play_game()
                    return self.get_balance_info()
                
                cur = int(time.time() * 1000)
                time_difference_s = (cur - int(data["farming"]["endTime"]))/1000
                if time_difference_s >= 0:
                    return True
                else:
                    self.wait_time = 0 - time_difference_s
                    return False
        except Exception as e:
            self.bprint(e)
            return True

    def claim_farm(self):
        pass

    def parse_config(self, cline):
        self.update_header("Authorization", cline["Authorization"])

    def claim(self):
        if self.get_balance_info():
            self.claim_farm()
        