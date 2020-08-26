from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse 
import requests
from datetime import datetime, timedelta
import calendar
import json
import math
from queue import Queue
import threading

requestyearUserUnitName = ['資訊工程學系', '資工所', '網媒所']
requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7

# Create your views here.
def index(request):
    '''
    res: [
        {"rentdate": yyyy-MM-dd, "venueName": xxxx, "rentTimePeriod": HH:mm:ss~HH:mm:ss ...},
        ...
    ]
    cal: [
        {
            "date": 1, # day 1
            "courts": [
                {"rentdate": d, "venueName": xxxx, "rentTimePeriod": HH:mm:ss~HH:mm:ss ...},
                ...
            ]
        },
        ...
    ]
    '''
    if 'month' in request.GET and request.GET['month']:
        requestMonth = int(request.GET['month'])
    else:
        requestMonth = datetime.now().month

    if 'year' in request.GET and request.GET['year']:
        requestYear = int(request.GET['year'])
    else:
        requestYear = datetime.now().year

    currentYear = datetime.now().year ## for copyright year
    requestTime = datetime(requestYear, requestMonth, 1)
    requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d") ## yyyy-MM-dd
    requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d") ## yyyy-MM-dd
    monthList = [i for i in range(1,13)]
    monthselect = [""]*12
    monthselect[requestMonth-1] = "selected"
    res = []
    isDrawn = True
    q = Queue()
    threads = []

    for court in requestvenueId:
        key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
        t = threading.Thread(target=threadIndex, args=(q, key))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    for _ in range(q.qsize()):
        data = q.get()
        res += data['res']
        isDrawn &= data['isDrawn']
    
    res.sort(key = lambda s: s['rentDate'])

    ## calendar
    weekdayS = calendar.monthrange(requestTime.year,requestTime.month)[0]
    days = calendar.monthrange(requestTime.year,requestTime.month)[1]
    weeks = math.ceil((weekdayS+days)/7)
    
    cal = [[{"date":0, "courts":[]} for _ in range(7)] for _ in range(weeks)]
    for i in range(1,days+1):
        cal[(i+weekdayS-1)//7][(i+weekdayS-1)%7] = {"date":i, "courts":[]}

    ## add court to calendar
    for i in res:
        date = int(i['rentDate'][-2:])
        cal[(date+weekdayS-1)//7][(date+weekdayS-1)%7]['courts'].append(i)
    
    return render(request, 'home/index.html', locals())

def threadIndex(q, key):
    '''
    input:
        q: return data
        key: contain 'rentDateS', 'rentDateE', 'venueId'
    '''

    court = key['venueId']
    r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)
    j1 = r.json()
    res = [x for x in j1 if x['yearUserUnitName'] in requestyearUserUnitName and x['statusDraw'] == 1]
    for i in res: i['rentDate'] = i['rentDate'][:10] ## yyyy-MM-dd HH:mm:ss -> yyyy-MM-dd

    isDrawn = (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and j1 != []

    q.put({"court": int(court)-82, "res": res, "isDrawn": isDrawn})

def ana(request):
    '''
    res: [
        [0, 0, 0, 0, 0, 0, 0, 0], # day 1 court 4,5,6,7 18:00 / court 4,5,6,7 20:00
        [0, 0, 0, 0, 0, 0, 0, 0], # day 2 court 4,5,6,7 18:00 / court 4,5,6,7 20:00
        ...
    ]
    cal: [
        {
            "date": 1, # day 1
            "sticks": [0, 0, 0, 0, 0, 0, 0, 0] # just like res
            "colors": ["", "", "", "", "", "", "", ""] # color of each time slice which depends on the quantity of sticks
        },
        ...
    ]
    '''

    if 'month' in request.GET and request.GET['month']:
        requestMonth = int(request.GET['month'])
    else:
        requestMonth = (datetime.now() + timedelta(days=31)).month

    if 'year' in request.GET and request.GET['year']:
        requestYear = int(request.GET['year'])
    else:
        requestYear = (datetime.now() + timedelta(days=31)).year
    
    currentYear = datetime.now().year ## for copyright year
    requestTime = datetime(requestYear, requestMonth, 1)
    requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d") ## yyyy-MM-dd
    requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d") ## yyyy-MM-dd
    monthList = [i for i in range(1,13)]
    monthselect = [""]*12
    monthselect[requestMonth-1] = "selected"

    ## calendar info
    weekdayS = calendar.monthrange(requestTime.year,requestTime.month)[0]
    days = calendar.monthrange(requestTime.year,requestTime.month)[1]
    weeks = math.ceil((weekdayS+days)/7)

    res = [[0] * 8 for i in range(days)]
    isDrawn = True
    q = Queue()
    threads = []
    
    for court in requestvenueId:
        key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
        t = threading.Thread(target=threadAna, args=(q, days, key))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    for _ in range(q.qsize()):
        data = q.get()
        for i in range(days):
            res[i][data['court']-4] = data['res'][i][0]
            res[i][data['court']] = data['res'][i][1]
            isDrawn &= data['isDrawn']

    ## calendar
    cal = [[{"date":0, "sticks":[], "colors":[]} for _ in range(7)] for _ in range(weeks)]
    for i in range(1,days+1):
        color = res[i-1].copy()
        for j in range(8):
            if color[j] == 0: color[j] = ""
            elif color[j] < 5: color[j] = "green"
            elif color[j] < 10: color[j] = "orange"
            else: color[j] = "red"
        cal[(i+weekdayS-1)//7][(i+weekdayS-1)%7] = {"date":i, "sticks":res[i-1], "colors": color}

    return render(request, 'home/ana.html', locals())

def threadAna(q, days, key):
    '''
    input:
        q: return data
        days: number of day in request month
        key: contain 'rentDateS', 'rentDateE', 'venueId'
    '''

    court = key['venueId']
    r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)
    j1 = r.json()
    # j2 = j1

    isDrawn = (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and j1 != []
    res = []

    for day in range(1,days+1):
        daystr = key['rentDateS'][:-2] + str(day).zfill(2) + " 00:00:00" ## yyyy-MM-dd 00:00:00
        j3 = [x for x in j1 if x['rentDate'] == daystr]
        poolA = [x for x in j3 if x['rentTimePeriod'] == '18:00~20:00']
        poolB = [x for x in j3 if x['rentTimePeriod'] == '20:00~22:00']
        res.append([len(poolA), len(poolB)])
    
    q.put({"court": int(court)-82, "res": res, "isDrawn": isDrawn})