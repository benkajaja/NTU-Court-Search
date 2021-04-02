# NTU-Court-Search #djangoWeb

[![Release](https://github.com/benkajaja/NTU-Court-Search/actions/workflows/ncs_djangoweb.yml/badge.svg?branch=master)](https://github.com/benkajaja/NTU-Court-Search/actions/workflows/ncs_djangoweb.yml)

## Environment:
* django
* Semantic UI

## Easy deployment:
* using docker
```
docker run --name ncs_djangoweb -p 8000:8000 -d docker.pkg.github.com/benkajaja/ntu-court-search/ncs_djangoweb:latest
```

## Development:
### Prerequisites
* python 3.6+
* requests
* django

### Run on your host
```
$ pip3 install -r requirements.txt
$ python3 NTU-Court-Search/djangoWeb/manage.py runserver
```

### Web layouts
* Request courts
![](https://i.imgur.com/zQjB0xZ.png)
* Count sticks
![](https://i.imgur.com/WX9RU37.png)

## Change Log

2020/8/25 
* Use multiple threads for crawling