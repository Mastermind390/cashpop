import requests
import json
import datetime
from django.conf import settings

#SK_124f1e0e5906efb897f3959a1768c3b8e6309725f9b
def _post_request_headers():
    headers = {
    'api-key': 'b0e2a455b837dfe74b7ef71f5470f5dc',
    'secret-key': 'SK_37640fc3b9b7d9103aab21fd47e535bd982ccd47cc4',
    'Content-Type': 'application/json'
    }
    return headers

def buy_airtime(network, amount, phone):
    try:
        todays_date = datetime.datetime.now()
        date_string = todays_date.strftime("%Y%m%d%H%M%S")
        print(date_string)
        airtime_url = 'https://sandbox.vtpass.com/api/pay'
        headers = _post_request_headers()
        
        payload = {
            "request_id" : date_string,
            "serviceID" : network,
            "amount" : amount,
            "phone" : phone,
        }

        response = requests.post(airtime_url, headers=headers, data=json.dumps(payload))
        parsed_data = json.loads(response.text)
        response_msg = parsed_data['response_description']

        return response_msg
    except Exception as err:
        return err
    

airtime =buy_airtime('etisalat', 100, '08011111111')
print(airtime)