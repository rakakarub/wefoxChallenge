import requests
import json
import os


class RestClientService:
    def __init__(self):
        self.base_url = 'http://' + os.getenv('API_BASE') + ':' + os.getenv('API_PORT')
        self.headers = {'content-type': 'application/json'}

    def check_payment(self, payment_data):
        url = self.base_url + '/payment'
        response = requests.post(url=url, headers=self.headers, data=json.dumps(payment_data))
        response.raise_for_status()
        return response.ok

    def log_error(self, payment_id, error_type, description):
        url = self.base_url + '/log'

        json_data = {
            'payment_id': payment_id,
            'error_type': error_type,
            'error_description': description
        }
        requests.post(url=url, headers=self.headers,data=json.dumps(json_data))
