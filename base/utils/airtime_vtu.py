import requests
import json
import datetime

#SK_124f1e0e5906efb897f3959a1768c3b8e6309725f9b
def _post_request_headers():
    headers = {
    'api-key': '4e85c5b543323d420bb26abf4da7ff8c',
    'secret-key': 'SK_9331f08f9bfe1fda8ed70420a67229bf333259b73b3',
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