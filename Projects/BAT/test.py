import simplejson as json
import time
import base64
import hashlib
import httplib2
import hmac

ACCESS_TOKEN = '422077c1-f498-417e-9f3a-d91685769e59'
SECRET_KEY = '8d51556f-47af-4384-a813-4bc99a9fc696'

URL = 'https://api.coinone.co.kr/v2/account/balance/'
PAYLOAD = {
    "access_token": ACCESS_TOKEN,
}

def get_encoded_payload(payload):
    payload['nonce'] = int(time.time()*1000)

    dumped_json = json.dumps(payload)
    encoded_json = base64.b64encode(dumped_json)
    return encoded_json

def get_signature(encoded_payload, secret_key):
    signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
    return signature.hexdigest()

def get_response(url, payload):
    encoded_payload = get_encoded_payload(payload)
    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
    }
    http = httplib2.Http()
    response, content = http.request(URL, 'POST', headers=headers, body=encoded_payload)
    return content

def get_result():
    content = get_response(URL, PAYLOAD)
    content = json.loads(content)

    return content

if __name__   == "__main__":
    print(get_result())
