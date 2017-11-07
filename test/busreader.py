import time #used to get current time
import json #used to format json
import requests #used to request from API

class BusData(object):  #The BusData object
    def __init__(self): #Initialize the object
        self.API_key = '0f5599c2be174e18ae203fb50ecbc15b'   #API key for the CUMTD API
        self.version = 'v2.2'   #The v2.2 (Just a requirement)
        self.format = 'json'    #Python reads json better
        self.busstopnames = []  #A list of bus stop names
        self.busstopids = []    #A list of bus stop ids
        self.busstopcodes = []  #A list of bus stop codes
        self.stopdata = self.getstops()['stops']    #initialize the above lists
        for stop in self.stopdata:
            self.busstopnames.append(stop['stop_name'])
            self.busstopids.append(stop['stop_id'])
            self.busstopcodes.append(stop['code'])

    def getURL(self,method):    #get the URL for API using the method
        url = 'https://developer.cumtd.com/api/'
        url += self.version
        url += '/'
        url += self.format
        url += '/'
        url += method
        return url

    def getcalendardatesbydate(self):   #get the current time information
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

    def getnews(self):  #get the news from CUMTD (what?)
        params = dict(
            key = self.API_key
        )
        resp = requests.get(url=self.getURL('getnews'),params=params)
        return json.loads(resp.text)

    def getreroutes(self):  #get reroutes of the buses
        params = dict(
            key=self.API_key
        )
        resp = requests.get(url=self.getURL('getreroutes'), params=params)
        return json.loads(resp.text)

    def getstops(self): #get all the stops from CUMTD
        params = dict(
            key = self.API_key
        )
        resp = requests.get(url=self.getURL('getstops'), params=params)
        return json.loads(resp.text)

    def getstopidfromname(self,name):   #get the stop ID from the name of the bus stop
        return self.busstopids[self.busstopnames.index(name)]

    def getstoptimesbystop(self,stopid):    #get the stop times by stop ID
        params = dict(
            key = self.API_key,
            stop_id = stopid
        )
        resp = requests.get(url=self.getURL('getstoptimesbystop'),params=params)
        return json.loads(resp.text)

    def getstoptimesbystopname(self,stopname):  #get the stop times by stop name
        return self.getstoptimesbystop(self.getstopidfromname(stopname))

    def getdeparturesbystop(self,stopid):   #get the departure times by stop ID
        params = dict(
            key = self.API_key,
            stop_id = stopid
        )
        resp = requests.get(url=self.getURL('getdeparturesbystop'),params=params)
        return json.loads(resp.text)

    def getdeparturesbystopname(self,stopname): #get the departure times by stop names
        return self.getdeparturesbystop(self.getstopidfromname(stopname))

if __name__ == '__main__':  #test function
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