import requests
from datetime import datetime
import calendar
import json
import math

requestyearUserUnitName = ['資訊工程學系', '資工所', '網媒所']
# requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
requestvenueId = ['86', '87','88','89'] # court 4,5,6,7

requestMonth = datetime.now().month+1
requestYear = datetime.now().year

requestTime = datetime(requestYear, requestMonth, 1)
monthList = [i for i in range(1,13)]

requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
requestStatus = []
monthList = [i for i in range(1,13)]
res = []
isDrawn = True

## calendar
weekdayS = calendar.monthrange(requestTime.year,requestTime.month)[0]
days = calendar.monthrange(requestTime.year,requestTime.month)[1]
weeks = math.ceil((weekdayS+days)/7)

## crawler
for court in requestvenueId:
    key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
    r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)
    j1 = r.json()
    j2 = [x for x in j1 if x['statusDraw'] == 0] # 1: winner 2: loser

    for day in range(1,days+1):
        daystr = datetime(requestTime.year,requestTime.month,day).strftime("%Y-%m-%d 00:00:00")
        j3 = [x for x in j2 if x['rentDate'] == daystr]
        poolA = [x for x in j3 if x['rentTimePeriod'] == '18:00~20:00']
        poolB = [x for x in j3 if x['rentTimePeriod'] == '20:00~22:00']
        print(daystr[:10], len(poolA), len(poolB))
        # 'rentDate': '2020-09-30 00:00:00'
        res.append({"date":day, "courtID":int(court)-82, "poolAcnt": len(poolA), "poolBcnt": len(poolB)})

    res.sort(key = lambda s: s['date'])

    # print(int(court)-82)
    # print(len(poolA))
    # print(len(poolB))
    # for i in poolA:
    #     print(f'statusConfirm: {i["statusConfirm"]}, statusRent: {i["statusRent"]}, statusDraw: {i["statusDraw"]}')
    # for i in poolB:
    #     print(f'statusConfirm: {i["statusConfirm"]}, statusRent: {i["statusRent"]}, statusDraw: {i["statusDraw"]}') 




    # j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
    # res += j3
    # isDrawn = isDrawn and (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and j1 != []
    # requestStatus.append({'courtID':int(court)-82, 'requestChk': r.status_code == 200})





cal = [[{"date":0, "sticks":[]} for _ in range(7)] for _ in range(weeks)]
for i in range(1,days+1):
    cal[(i+weekdayS-1)//7][(i+weekdayS-1)%7] = {"date":i, "sticks":[]}

for i in res:
    date = int(i['date'])
    cal[(date+weekdayS-1)//7][(date+weekdayS-1)%7]['sticks'].append(i)

print(cal)

## current output
# [
#     {'date': 23, 
#     'sticks': [
#         {'courtID': 4, 'poolAcnt': 0, 'poolBcnt': 2}, 
#         {'courtID': 5, 'poolAcnt': 3, 'poolBcnt': 3}, 
#         {'courtID': 6, 'poolAcnt': 4, 'poolBcnt': 4}, 
#         {'courtID': 7, 'poolAcnt': 1, 'poolBcnt': 3}]
#     },
#     {'date': 24, 
#     'sticks': [
#         {'courtID': 4, 'poolAcnt': 0, 'poolBcnt': 2}, 
#         {'courtID': 5, 'poolAcnt': 3, 'poolBcnt': 0}, 
#         {'courtID': 6, 'poolAcnt': 2, 'poolBcnt': 4}, 
#         {'courtID': 7, 'poolAcnt': 1, 'poolBcnt': 3}]
#     }
# ]


