import time
import json
import requests

class BusData(object):
    def __init__(self):
        self.API_key = '0f5599c2be174e18ae203fb50ecbc15b'
        self.version = 'v2.2'
        self.format = 'json'
        self.busstopnames = []
        self.busstopids = []
        self.busstopcodes = []
        self.stopdata = self.getstops()['stops']
        for stop in self.stopdata:
            self.busstopnames.append(stop['stop_name'])
            self.busstopids.append(stop['stop_id'])
            self.busstopcodes.append(stop['code'])

    def getURL(self,method):
        url = 'https://developer.cumtd.com/api/'
        url += self.version
        url += '/'
        url += self.format
        url += '/'
        url += method
        return url

    def getcalendardatesbydate(self):
        localtime = time.localtime(time.time())
        dat = ''
        dat += str(localtime[0])
        dat += '-'
        dat += str(localtime[1])
        dat += '-'
        dat += str(localtime[2])
        params = dict(
            key = self.API_key,
            date = dat
        )
        resp = requests.get(url=self.getURL('getcalendardatesbydate'), params=params)
        return json.loads(resp.text)

    def getnews(self):
        params = dict(
            key = self.API_key
        )
        resp = requests.get(url=self.getURL('getnews'),params=params)
        return json.loads(resp.text)

    def getreroutes(self):
        params = dict(
            key=self.API_key
        )
        resp = requests.get(url=self.getURL('getreroutes'), params=params)
        return json.loads(resp.text)

    def getstops(self):
        params = dict(
            key = self.API_key
        )
        resp = requests.get(url=self.getURL('getstops'), params=params)
        return json.loads(resp.text)

    def getstopidfromname(self,name):
        return self.busstopids[self.busstopnames.index(name)]

    def getstoptimesbystop(self,stopid):
        params = dict(
            key = self.API_key,
            stop_id = stopid
        )
        resp = requests.get(url=self.getURL('getstoptimesbystop'),params=params)
        return json.loads(resp.text)

    def getstoptimesbystopname(self,stopname):
        return self.getstoptimesbystop(self.getstopidfromname(stopname))

    def getdeparturesbystop(self,stopid):
        params = dict(
            key = self.API_key,
            stop_id = stopid
        )
        resp = requests.get(url=self.getURL('getdeparturesbystop'),params=params)
        return json.loads(resp.text)

    def getdeparturesbystopname(self,stopname):
        return self.getdeparturesbystop(self.getstopidfromname(stopname))

if __name__ == '__main__':
    b = BusData()
    stopname = 'Transit Plaza'
    departures = b.getdeparturesbystopname(stopname)['departures']
    text = ''
    for departure in departures:
        text += departure['headsign']
        text += ' is arriving in '
        text += str(departure['expected_mins'])
        text += ' minutes. '
    print text