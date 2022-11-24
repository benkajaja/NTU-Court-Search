import json
import os
from datetime import datetime, timedelta, timezone
import calendar
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']
WEBURL = os.environ['WEBURL']

requestyearUserUnitName = ['資訊工程學系', '資訊工程學研究所', '資訊網路與多媒體研究所']
requestvenueId = [44, 45, 46, 47] # court 4,5,6,7
venuesSNToName = {
    44: "排球場 (4)",
    45: "排球場 (5)",
    46: "排球場 (6)",
    47: "排球場 (7)"
}
weekday = ['一', '二', '三', '四', '五', '六', '日']

def lambda_handler(event, context):
    url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage'
    time = datetime.now() + timedelta(days=12)
    text = f'{time.month}月份場單：）\n'
    text += getCrawlResult(time)
    text += getInfo(time)
    response = requests.get(url, json = {"chat_id": CHANNEL, "text": text})

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def getInfo(time):
    text = f"\nFor more information, please check\n{WEBURL}/?year={time.year}&month={time.month}"
    return text

def getCrawlResult(time):

    text = ""
    requestTime = time
    requestDateS =  datetime(requestTime.year,requestTime.month,1,tzinfo=timezone(timedelta(hours=8))).timestamp() ## epoch time
    requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1],tzinfo=timezone(timedelta(hours=8))).timestamp() ## epoch time
    res = []
    isDrawn = True

    ## crawler
    for court in requestvenueId:
        key = {
            "VenuesSN": court,
            "SDMK": requestDateS,
            "EDMK": requestDateE
        }
        r = requests.get('https://rent.pe.ntu.edu.tw/__/f/Schedule.php', params = key)
        
        if r.status_code != 200:
            return f"Request failed with status: {r.status_code}\n"

        data = r.json()
        soup = BeautifulSoup(data['ScheduleList'], "html.parser")
        matchPattern = "(" + "|".join(requestyearUserUnitName) + ")"
        result = soup.find_all("div", {"title": re.compile(matchPattern)})
        for i in result:
            duration = int(re.findall('[0-9]+', result[0].parent.get_attribute_list('style')[0])[1])
            start = int(re.findall('[0-9]+', i.parent.previous_sibling.contents[0])[0])
            rentTimePeriod = f"{start}:00~{start+duration}:00"
            res.append({
                "rentDate": i.parent.parent.parent['d'],
                "venueName": venuesSNToName[key["VenuesSN"]],
                "rentTimePeriod": rentTimePeriod
            })

    if not isDrawn: return "還沒抽呢：）"

    ## post process
    for i in res:
        i['rentDate'] = i['rentDate'][:10]

        ## convert to "一二三四五六日"
        i['weekDay'] =  weekday[datetime.strptime(i['rentDate'], '%Y-%m-%d').weekday()]

        ## convert to "前" or "後"
        i['rentTimePeriodCh'] = i['rentTimePeriod']
        if i['rentTimePeriodCh'] == "18:00~20:00": i['rentTimePeriodCh'] = "前"
        elif i['rentTimePeriodCh'] == "20:00~22:00": i['rentTimePeriodCh'] = "後"

    ## show
    res.sort(key = lambda s: (s['rentDate'], s['rentTimePeriod']))
    for i in res:
        text += f"{i['rentDate']}({i['weekDay']}){i['rentTimePeriodCh']} {i['venueName']}\n"

    return text
