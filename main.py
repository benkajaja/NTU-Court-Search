import requests
from datetime import datetime
import calendar

requestyearUserUnitName = ['資訊工程學系', '資工所', '網媒所']
requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
requestTime = datetime(2020, 5, 1) # or datetime.now()
requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
print("From %s To %s" % (requestDateS, requestDateE))
res = []

## crawler
for court in requestvenueId:
    # reqUrl = 'https://pe.ntu.edu.tw/api/rent/yearuserrent?' + \
    #          'rentDateS=' + requestDateS + '&'\
    #          'rentDateE=' + requestDateE + '&'\
    #          'venueId=' + court
    # r = requests.get(reqUrl)

    key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
    r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)

    # print(r.status_code)
    j1 = r.json()
    j2 = [x for x in j1 if x['statusDraw'] == 1] # 1: winner 2: loser
    j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
    res += j3
    
## show
res.sort(key = lambda s: s['rentDate'])
for i in res:
    print("-------------------------------------")
    print('venueName:', i['venueName'])
    print('yearUserUnitName:', i['yearUserUnitName'])
    print('statusDraw:', i['statusDraw'])
    print('rentDate:', i['rentDate'])
    print('rentTimePeriod:', i['rentTimePeriod'])
