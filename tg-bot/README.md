# NTU-Court-Search #tg-bot
比較少使用這個專案，它的實用性沒有比TG channel推播來得高，只用來學習如何串Telegram API

## To do list
- [ ] Use AWS Lambda + API Gateway
- [ ] 持續挖坑

## Development:
### Prerequisites
* python 3.6+
* requests
* flask
* python-telegram-bot

### Certificates(self-signed)
```
$ openssl req -newkey rsa:2048 -sha256 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
$ curl -F "url=https://[IP:PORT]/hook" -F "certificate=@/path/to/cert.pem" https://api.telegram.org/bot[BOT TOKEN]/setWebhook
{"ok":true,"result":true,"description":"Webhook was set"}
```
### Create config file
```ini
[TELEGRAM]
ACCESS_TOKEN = 
CERT = /path/to/cert.pem
KEY = /path/to/key.pem
```

### Run on your host
```
$ python3 NTU-Court-Search/tg-bot/main.py
```

## Ref
https://medium.com/@zaoldyeck/%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E6%80%8E%E9%BA%BC%E6%89%93%E9%80%A0-telegram-bot-a7b539c3402a
https://core.telegram.org/bots/api