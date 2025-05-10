import requests
import json
import datetime
from django.conf import settings

def request_headers():
    headers = {
    'api-key': settings.VTPASS_API_KEY,
    'public-key': settings.VTPASS_PUBLIC_KEY,
    'Content-Type': 'application/json'
}
    return headers

def _post_request_headers():
    headers = {
    'api-key': settings.VTPASS_API_KEY,
    'secret-key': settings.VTPASS_SECRET_KEY,
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



