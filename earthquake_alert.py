import time, datetime, requests, json
import pushbullet_key
from pushbullet import Pushbullet

api_key = pushbullet_key.get_key()
try:
    pb = Pushbullet(api_key)

except Exception as ex:
    print ex

'''URL to retrieve data from'''
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

'''Initiate UPDATES array to store new earthquake alerts'''
UPDATES = []

'''Initate earthquake_print function, takes json input, outputs data to console in readable format'''
def earthquake_print(data):
    
    for i in data['features']:
        
        if i['id'] not in UPDATES:
            
            UPDATES.append(i['id'])
            title = i['properties']['title']
            event_type = i['properties']['type'] 
            ms = i['properties']['time']
            event_time = datetime.datetime.fromtimestamp(ms/1000)
            link = i['properties']['url']
            content = 'Type: {}\t{}\n{}'.format(event_type, event_time, link)
            push = pb.push_note(title, content)
            print title
            print content
            
def get_earthquakes():
    
    try:
        resp = requests.get(URL)
        resp = json.loads(resp.text)
        count =  resp['metadata']['count']
        
        if count != 0:
            earthquake_print(resp)
        else:
            pass        
        
    except Exception as ex:
        print ex
    
if __name__ == '__main__':
    seconds = 30
    while True:
        get_earthquakes()
        time.sleep(seconds)
