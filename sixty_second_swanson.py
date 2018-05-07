import requests, time, pushbullet_key
from pushbullet import Pushbullet

USED_QUOTES = []
URL = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
API_KEY = pushbullet_key.get_key()

try:
    PB = Pushbullet(API_KEY)

except Exception as ex:
    print ex
    
def swanson():
    
    RESPONSE = requests.get(URL)
    if RESPONSE.text not in USED_QUOTES:
        
        USED_QUOTES.append(RESPONSE.text)
        QUOTE = RESPONSE.text.replace('[', '', 1)
        NEW_QUOTE = QUOTE.replace(']', '', 1)
        PUSH = PB.push_note('Sixty Second Swanson', NEW_QUOTE)
    
    else:
        swanson()
    
while True:
    swanson()
    time.sleep(60)