import json
import requests
import os
from datetime import datetime, timedelta
import calendar

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']
WEBURL = os.environ['WEBURL']

requestyearUserUnitName = ['資訊工程學系', '資訊工程學研究所', '資訊網路與多媒體研究所']
requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
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
    requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
    requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
    res = []
    isDrawn = True

    ## crawler
    for court in requestvenueId:

        key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
        r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)

        if r.status_code != 200:
            return f"Request failed with status: {r.status_code}\n"

        j1 = r.json()
        isDrawn = isDrawn and (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and r.json() != []
        j2 = [x for x in j1 if x['statusDraw'] == 1] # 1: winner 2: loser
        j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
        res += j3

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