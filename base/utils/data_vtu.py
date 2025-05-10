import requests
import json
import datetime
# from .utils.airtime_vtu import _post_request_headers

def request_headers():
    headers = {
    'api-key': '4e85c5b543323d420bb26abf4da7ff8c',
    'public-key': 'PK_494c0e3b4f7553e1b6128fc817a85f1df521aaad703',
    'Content-Type': 'application/json'
}
    return headers

def _post_request_headers():
    headers = {
    'api-key': '4e85c5b543323d420bb26abf4da7ff8c',
    'secret-key': 'SK_9331f08f9bfe1fda8ed70420a67229bf333259b73b3',
    'Content-Type': 'application/json'
    }
    return headers

def request_id_generator():
    todays_date = datetime.datetime.now()
    date_string = todays_date.strftime("%Y%m%d%H%M%S")
    return date_string

def get_mtn_data_options(network):
    try:
        headers = request_headers()
        mtn_data_url = f'https://sandbox.vtpass.com/api/service-variations?serviceID={network}-data'
        response = requests.get(mtn_data_url, headers=headers)
        parsed_data = json.loads(response.text)
        mtn_data_options = parsed_data['content']['variations']
        return mtn_data_options
    except Exception as err:
        return err

def get_airtel_data_options(network):
    try:
        headers = request_headers()
        airtel_data_url = f'https://sandbox.vtpass.com/api/service-variations?serviceID={network}-data'
        response = requests.get(airtel_data_url, headers=headers)
        parsed_data = json.loads(response.text)
        airtel_data_options = parsed_data['content']['variations']
        return airtel_data_options
    except Exception as err:
        return err

def get_glo_data_options(network):
    try:
        headers = request_headers()
        glo_data_url = f'https://sandbox.vtpass.com/api/service-variations?serviceID={network}-data'
        response = requests.get(glo_data_url, headers=headers)
        parsed_data = json.loads(response.text)
        glo_data_options = parsed_data['content']['variations']
        return glo_data_options
    except Exception as err:
        return err

def get_glo_sme_data_options(network):
    try:
        headers = request_headers()
        glo_sme_data_url = f'https://sandbox.vtpass.com/api/service-variations?serviceID={network}-sme-data'
        response = requests.get(glo_sme_data_url, headers=headers)
        parsed_data = json.loads(response.text)
        glo_sme_data_options = parsed_data['content']['variations']
        return glo_sme_data_options
    except Exception as err:
        return err

def get_9mobile_data_options(network):
    try:
        headers = request_headers()
        _9mobile_data_url = f'https://sandbox.vtpass.com/api/service-variations?serviceID={network}-data'
        response = requests.get(_9mobile_data_url, headers=headers)
        parsed_data = json.loads(response.text)
        _9mobile_data_options = parsed_data['content']['variations']
        return _9mobile_data_options
    except Exception as err:
        return err
    
def get_data_options():
    mtn = get_mtn_data_options("mtn")
    airtel = get_airtel_data_options("airtel")
    glo = get_glo_data_options("glo")
    glo_sme = get_glo_sme_data_options("glo")
    etisalat = get_9mobile_data_options('etisalat')
    data_options = mtn + airtel + glo + glo_sme + etisalat
    return data_options


def purchase_data(network, amount, billersPhone, variation_code, user_phone_number):
    try:
        base_url = 'https://sandbox.vtpass.com/api/pay'
        request_id = request_id_generator()
        headers = _post_request_headers()

        payload = {
            "request_id" : request_id,
            "serviceID" : f"{network}-data",
            "billersCode" : billersPhone,
            "variation_code" : variation_code,
            "amount" : amount,
            "phone" : user_phone_number,
        }
        #08011111111
        response = requests.post(base_url, headers=headers, data=json.dumps(payload))
        parsed_data = json.loads(response.text)
        response_msg = parsed_data['response_description']
        return response_msg
    except Exception as err:
        return err



