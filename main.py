import requests
from datetime import datetime
import calendar

requestyearUserUnitName = ['資訊工程學系', '資訊工程學研究所', '資訊網路與多媒體研究所']
requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
requestTime = datetime.now() # or datetime(2020, 6, 1)
requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
print("From %s To %s" % (requestDateS, requestDateE))
res = []
isDrawn = True

def haveCourt(x):
    if (x['statusRent'] == 1 or                         ## manual reserve
        x['statusDraw'] == 1 and x['statusRent'] == 2): ## winner
        return True
    else: 
        return False

def checkDrawn(x):
    return (not any(y['statusRent']==2 and y['statusDraw']==0 for y in x)) and x != []

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
    data = r.json()
    isDrawn = isDrawn and checkDrawn(data)
    myCourt = [x for x in data if x['yearUserUnitName'] in requestyearUserUnitName and haveCourt(x)]
    res += myCourt

for i in res:
    i['rentDate'] = i['rentDate'][:10]

## show
res.sort(key = lambda s: s['rentDate'])
for i in res:
    print("-------------------------------------")
    print('venueName:', i['venueName'])
    print('yearUserUnitName:', i['yearUserUnitName'])
    print('statusDraw:', i['statusDraw'])
    print('rentDate:', i['rentDate'])
    print('rentTimePeriod:', i['rentTimePeriod'])
