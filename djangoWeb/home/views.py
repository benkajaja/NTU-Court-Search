from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse 
import requests
from datetime import datetime, timedelta
import calendar
import json
import math

requestyearUserUnitName = ['資訊工程學系', '資工所', '網媒所']
requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7

# Create your views here.
def index(request):
    
    if 'month' in request.GET and request.GET['month']:
        # requestMonth = datetime(2020, int(request.GET['month']), 1)
        requestMonth = int(request.GET['month'])
    else:
        requestMonth = datetime.now().month

    if 'year' in request.GET and request.GET['year']:
        requestYear = int(request.GET['year'])
    else:
        requestYear = datetime.now().year

    requestTime = datetime(requestYear, requestMonth, 1)
    
    requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
    requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
    requestStatus = []
    monthList = [i for i in range(1,13)]
    monthselect = [""]*12
    monthselect[requestMonth-1] = "selected"
    res = []
    isDrawn = True

    ## crawler
    for court in requestvenueId:
        key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
        r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)
        j1 = r.json()
        j2 = [x for x in j1 if x['statusDraw'] == 1] # 1: winner 2: loser
        j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
        res += j3
        isDrawn = isDrawn and (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and j1 != []
        requestStatus.append({'courtID':int(court)-82, 'requestChk': r.status_code == 200})
    
    for i in res:
        i['rentDate'] = i['rentDate'][:10]
    
    res.sort(key = lambda s: s['rentDate'])

    ## calendar
    weekdayS = calendar.monthrange(requestTime.year,requestTime.month)[0]
    days = calendar.monthrange(requestTime.year,requestTime.month)[1]
    weeks = math.ceil((weekdayS+days)/7)
    
    cal = [[{"date":0, "courts":[]} for _ in range(7)] for _ in range(weeks)]
    for i in range(1,days+1):
        cal[(i+weekdayS-1)//7][(i+weekdayS-1)%7] = {"date":i, "courts":[]}

    ## add court
    for i in res:
        date = int(i['rentDate'][-2:])
        cal[(date+weekdayS-1)//7][(date+weekdayS-1)%7]['courts'].append(i)
    
    return render(request, 'home/index.html', locals())


def ana(request):

    if 'month' in request.GET and request.GET['month']:
        requestMonth = int(request.GET['month'])
    else:
        requestMonth = (datetime.now() + timedelta(days=31)).month

    if 'year' in request.GET and request.GET['year']:
        requestYear = int(request.GET['year'])
    else:
        requestYear = (datetime.now() + timedelta(days=31)).year
    
    requestTime = datetime(requestYear, requestMonth, 1)

    requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
    requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
    requestStatus = []
    monthList = [i for i in range(1,13)]
    monthselect = [""]*12
    monthselect[requestMonth-1] = "selected"

    ## calendar info
    weekdayS = calendar.monthrange(requestTime.year,requestTime.month)[0]
    days = calendar.monthrange(requestTime.year,requestTime.month)[1]
    weeks = math.ceil((weekdayS+days)/7)

    res = [[0] * 8 for i in range(days)]

    isDrawn = True

    ## crawler
    for court in requestvenueId:
        key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
        r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)
        j1 = r.json()
        # j2 = [x for x in j1 if x['statusDraw'] == 0] # 1: winner 2: loser
        j2 = j1

        isDrawn = isDrawn and (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and j1 != []

        for day in range(1,days+1):
            daystr = datetime(requestTime.year,requestTime.month,day).strftime("%Y-%m-%d 00:00:00")
            j3 = [x for x in j2 if x['rentDate'] == daystr]
            poolA = [x for x in j3 if x['rentTimePeriod'] == '18:00~20:00']
            poolB = [x for x in j3 if x['rentTimePeriod'] == '20:00~22:00']
            res[day-1][int(court)-86] = len(poolA)
            res[day-1][int(court)-82] = len(poolB)

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