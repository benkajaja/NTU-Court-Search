from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse 
import requests
from datetime import datetime
import calendar
import json
import math

# Create your views here.
def index(request):
    requestyearUserUnitName = ['資訊工程學系', '資工所', '網媒所']
    requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
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
    res = []

    ## crawler
    for court in requestvenueId:
        key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
        r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)
        j1 = r.json()
        j2 = [x for x in j1 if x['statusDraw'] == 1] # 1: winner 2: loser
        j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
        res += j3
    
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
    
    monthList = [i for i in range(1,13)]
        
    return render(request, 'home/index.html', locals())
