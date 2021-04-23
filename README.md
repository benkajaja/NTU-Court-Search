# NTU-Court-Search

This project contains 4 parts
* Django web(with semantic-ui)
* Telegram Bot
* Telegram Channel(with AWS Lambda)
* cdk-ncs-reminder (with AWS CDK)

For more information please check README file in each subfolder

## Features a.k.a 挖坑區
* django :white_check_mark:
* semantic ui :white_check_mark:
* AWS Lambda :white_check_mark:
* Telegram API :white_check_mark:
* Deploy ncs_djangoweb image with Github Action :white_check_mark:
* Deploy AWS resources(dynamoDB, lambda) using AWS CDK :white_check_mark:

## Usage
You can simply get information of courts in current month by running 
```
$ python3 NTU-Court-Search/main.py
```

Try djangoWeb using docker image
```
$ docker run --name ncs_djangoweb -p 8000:8000 -d docker.pkg.github.com/benkajaja/ntu-court-search/ncs_djangoweb:latest
```

## Take a look
* Web layout

![](https://i.imgur.com/zQjB0xZ.png)

* TG channel

![](https://i.imgur.com/iiDiJPH.png)

## Thanks to
- [Daniel Tsai](https://github.com/daniel0076)
