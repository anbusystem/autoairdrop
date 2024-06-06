from .base import basetap
import requests
import time

# Define the URL and the headers
url = "https://api-gw-tg.memefi.club/graphql"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "authority": "api-gw-tg.memefi.club",
    "method": "POST",
    "path": "/graphql",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY2MWI5ODYwYjU0MjNlYWI0MmEwZjNkNSIsInVzZXJuYW1lIjoicm9rYm90c3h5eiJ9LCJzZXNzaW9uSWQiOiI2NjYxYWY5OTNjNmVkNDc3Y2JkZTM5ZTgiLCJzdWIiOiI2NjFiOTg2MGI1NDIzZWFiNDJhMGYzZDUiLCJpYXQiOjE3MTc2Nzc5NzcsImV4cCI6MTcxODI4Mjc3N30.mJIL-UBGylUMfhcoKB-12cAk_M3wCgj2m7VanQIdYpc",
    "dnt": "1",
    "origin": "https://tg-app.memefi.club",
    "priority": "u=1, i",
    "referer": "https://tg-app.memefi.club/",
    "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Content-Type": "application/json"
}
DEFAULT_AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY2MWI5ODYwYjU0MjNlYWI0MmEwZjNkNSIsInVzZXJuYW1lIjoicm9rYm90c3h5eiJ9LCJzZXNzaW9uSWQiOiI2NjQ4NTVhNTQyYWRmOTQ4ZGNlODA3N2QiLCJzdWIiOiI2NjFiOTg2MGI1NDIzZWFiNDJhMGYzZDUiLCJpYXQiOjE3MTYwMTY1NDksImV4cCI6MTcxNjYyMTM0OX0.E7FkUdCtK1NuyJgoxs4BdShlMtucv_nZBuWCRoBiGLs"
# Define the JSON body



class memefi(basetap):
    def __init__(self, auth = DEFAULT_AUTH, proxy = None, headers = DEFAULT_HEADERS):
        super().__init__()
        self.auth = auth
        self.proxy = proxy
        self.headers = headers
        self.headers["authorization"] = auth
        self.stopped = False
        self.wait_time = 10
        self.name = self.__class__.__name__
        self.body = {
            "operationName": "MutationGameProcessTapsBatch",
            "variables": {
                "payload": {
                    "nonce": "cb467f0785fa0e8e62a55c1614b7d1c8084036d74f014422bfe799b8ead7ae67",
                    "tapsCount": 20
                }
            },
            "query": """
                mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {
                    telegramGameProcessTapsBatch(payload: $payload) {
                        ...FragmentBossFightConfig
                        __typename
                    }
                }
                fragment FragmentBossFightConfig on TelegramGameConfigOutput {
                    _id
                    coinsAmount
                    currentEnergy
                    maxEnergy
                    weaponLevel
                    energyLimitLevel
                    energyRechargeLevel
                    tapBotLevel
                    currentBoss {
                        _id
                        level
                        currentHealth
                        maxHealth
                        __typename
                    }
                    freeBoosts {
                        _id
                        currentTurboAmount
                        maxTurboAmount
                        turboLastActivatedAt
                        turboAmountLastRechargeDate
                        currentRefillEnergyAmount
                        maxRefillEnergyAmount
                        refillEnergyLastActivatedAt
                        refillEnergyAmountLastRechargeDate
                        __typename
                    }
                    bonusLeaderDamageEndAt
                    bonusLeaderDamageStartAt
                    bonusLeaderDamageMultiplier
                    nonce
                    __typename
                }
            """
        }
        

    def get_nonce(self):
        postdata = {
            "operationName": "QUERY_GAME_CONFIG",
            "variables": {},
            "query": """query QUERY_GAME_CONFIG {
                telegramGameGetConfig {
                    ...FragmentBossFightConfig
                    __typename
                }
            }

            fragment FragmentBossFightConfig on TelegramGameConfigOutput {
            _id
            coinsAmount
            currentEnergy
            maxEnergy
            weaponLevel
            energyLimitLevel
            energyRechargeLevel
            tapBotLevel
            currentBoss {
                _id
                level
                currentHealth
                maxHealth
                __typename
            }
            freeBoosts {
                _id
                currentTurboAmount
                maxTurboAmount
                turboLastActivatedAt
                turboAmountLastRechargeDate
                currentRefillEnergyAmount
                maxRefillEnergyAmount
                refillEnergyLastActivatedAt
                refillEnergyAmountLastRechargeDate
                __typename
            }
            bonusLeaderDamageEndAt
            bonusLeaderDamageStartAt
            bonusLeaderDamageMultiplier
            nonce
            __typename
            }"""
        }
        url = ""
        try:
            response = requests.post(url, headers=self.headers, json=postdata)
            data = response.json()
            print(response.json())
            if "data" in data and "telegramGameGetConfig" in data["data"]:
                nounce = data["data"]["telegramGameGetConfig"]["nonce"]
                self.body["variables"]["payload"]["nonce"] = nounce
        except Exception as e:
            self.bprint("Failed to get nounce")

    def claim(self):
        requests.get("https://api-gw-tg.memefi.club/graphql")
        time.sleep(10)
        self.get_nonce()
        try:
            response = requests.post(url, headers=self.headers, json=self.body, proxies=self.proxy)
            data = response.json()
            print(data)
            self.print_balance(data['data']['telegramGameProcessTapsBatch']['coinsAmount'])
        except Exception as e:
            self.bprint(e)
    
    def parse_config(self, cline):
        self.update_header("authorization", cline["authorization"])