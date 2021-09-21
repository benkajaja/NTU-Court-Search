import requests
from datetime import datetime
import calendar

requestyearUserUnitName = ['資訊工程學系', '資訊工程學研究所', '資訊網路與多媒體研究所']
requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
weekday = ['一', '二', '三', '四', '五', '六', '日']

class crawler():
    def __init__(self):
        self.debug = False

    def validateInputDate(self, input):
        try:
            date = datetime.strptime(input, '%Y/%m')
        except ValueError:
            # raise ValueError("Incorrect data format, should be YYYY/MM")
            date = datetime.now()
        
        return date

    def getText(self, input):
        if self.debug:
            return self.craw_court()
        else:
            text = ""
            requestTime = self.validateInputDate(input)

            requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
            requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
            # print("From %s To %s" % (requestDateS, requestDateE))
            res = []
            isDrawn = True

            ## crawler
            for court in requestvenueId:

                key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
                r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)

                # print(r.status_code)
                j1 = r.json()
                isDrawn = isDrawn and (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and r.json() != []
                j2 = [x for x in j1 if x['statusDraw'] == 1] # 1: winner 2: loser
                j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
                res += j3

            if not isDrawn: return "還沒抽呢：）"

            for i in res:
                i['rentDate'] = i['rentDate'][:10]
                i['weekDay'] =  weekday[datetime.strptime(i['rentDate'], '%Y-%m-%d').weekday()]
                i['rentTimePeriodCh'] = i['rentTimePeriod']
                if i['rentTimePeriodCh'] == "18:00~20:00": i['rentTimePeriodCh'] = "前"
                elif i['rentTimePeriodCh'] == "20:00~22:00": i['rentTimePeriodCh'] = "後"

            ## show
            # res.sort(key = lambda s: s['rentDate'])
            res.sort(key = lambda s: (s['rentDate'], s['rentTimePeriod']))
            for i in res:
                # text = text + "-------------------------------------\n"
                # text = text + 'rentDate:' + str(i['rentDate']) + '\n'
                # text = text + 'rentTimePeriod:' + str(i['rentTimePeriod']) + '\n'
                # text = text + 'venueName:' + str(i['venueName']) + '\n'
                # text = text + 'yearUserUnitName:' + str(i['yearUserUnitName']) + '\n'
                # text = text + 'statusDraw:' + str(i['statusDraw']) + '\n'
                # text += str(i['rentDate']) + "(" + str(i['weekDay']) + ") " + str(i['rentTimePeriodCh']) + " " + str(i['venueName']) + '\n'
                text += i['rentDate'] + "(" + i['weekDay'] + ") " + i['rentTimePeriodCh'] + " " + i['venueName'] + '\n'

            return text 

    def craw_court(self):
        text = ""
        requestyearUserUnitName = ['資訊工程學系', '資訊工程學研究所', '資訊網路與多媒體研究所']
        requestvenueId = ['86', '87', '88', '89'] # court 4,5,6,7
        requestTime = datetime.now() # or datetime(2020, 6, 1)
        requestDateS =  datetime(requestTime.year,requestTime.month,1).strftime("%Y-%m-%d")
        requestDateE =  datetime(requestTime.year,requestTime.month,calendar.monthrange(requestTime.year, requestTime.month)[1]).strftime("%Y-%m-%d")
        print("From %s To %s" % (requestDateS, requestDateE))
        res = []
        isDrawn = True

        ## crawler
        for court in requestvenueId:

            key = {'rentDateS': requestDateS, 'rentDateE': requestDateE, 'venueId': court}
            r = requests.get('https://pe.ntu.edu.tw/api/rent/yearuserrent', params = key)

            # print(r.status_code)
            j1 = r.json()
            isDrawn = isDrawn and (not any(jj['statusRent']==2 and jj['statusDraw']==0 for jj in j1)) and r.json() != []
            j2 = [x for x in j1 if x['statusDraw'] == 1] # 1: winner 2: loser
            j3 = [x for x in j2 if x['yearUserUnitName'] in requestyearUserUnitName]
            res += j3

        for i in res:
            i['rentDate'] = i['rentDate'][:10]

        ## show
        res.sort(key = lambda s: s['rentDate'])
        for i in res:
            text = text + "-------------------------------------\n"
            text = text + 'venueName:' + str(i['venueName']) + '\n'
            text = text + 'yearUserUnitName:' + str(i['yearUserUnitName']) + '\n'
            text = text + 'statusDraw:' + str(i['statusDraw']) + '\n'
            text = text + 'rentDate:' + str(i['rentDate']) + '\n'
            text = text + 'rentTimePeriod:' + str(i['rentTimePeriod']) + '\n'

        return text