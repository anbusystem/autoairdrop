
# About this project

A simple application written in Python with requests library to achieve the smooth airdrop claim/click on telegram without needed of open telegram bot app (web app) on the phone or PC




## Features

- Auto claim for popular airdrop app like: yescoin, tapswap, cexio...
- With proxy support
- Auto claim hot coin using NEAR transaction API
- Cross platform, run anywhere 
- Very light weight and friendly framework


## Installation

For claiming of normal coins using requests, you need to have python install on the computer (or event a phone) and modify config.json with your actual data.

```bash
  cd autoairdrop
  pip install requests
  python main.py
```

For claiming of hot coin on near wallet, you need also the python and remember to edit hotnear.json to put your account id and privatekey

```bash
  cd autoairdrop
  pip install -r requirements
  python onlyhotcoin.py
```

In case you meet error when run the pip install, please raise an issue and put your telegram account so I can support
## Support

For support, join telegram  [Tele Airdrop Script](https://t.me/teleairdropscript)


## Project status

| Bot/Token name  | Script name  | Ref-link | Status |
| :------------ |:---------------:| -----:| -----: |
| Yes coin      | yescoin.py |  |  Working |
| Tapswap      | tapswap.py |  |  Working |
| Memefi      | memefi.py |  |  Working |
| Hamster Kombat      | hamster.py |  |  Working |
| CEX IO Tap      | cexio.py |  |  Working |
| Cell coin      | cellcoin.py |  |  Working |
| Blump coin      | blump.py |  |  Plan |
| Seed coin      | seed.py |  |  Plan |
| VivaFtn      | seed.py |  |  Not support |
| Hot coin      | hotclaimnear.py |  |  Working |



## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.
