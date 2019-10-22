'''
Created on Jul 15, 2019

@author: gjwang
'''
import json
import hmac
from hashlib import sha256
from time import time

import requests
import uuid

from py.api_test import ORDER_STATE_OPEN, ORDER_STATE_CLOSED

API_KEY_PRIVATE_PATH = '/api/v1/private'
API_KEY_PUBLIC_PATH  = '/api/v1/public'
ACCOUNT_PRIVATE_PATH = '/account'


def get_cur_time_ms():
    """
    :return: current timestamp in milliseconds
    """
    return int(time()*1000)


class AwsClientBase(object):
    def __init__(self, api_base_url, account_base_url=None, headers=None, cookies=None):
        if api_base_url:
            private_path = API_KEY_PRIVATE_PATH
            self.base_url = api_base_url
        elif account_base_url:
            private_path = ACCOUNT_PRIVATE_PATH
            self.base_url = account_base_url
            self.headers = headers
            self.cookies = cookies
        else:
            assert('Need to set base url')

        self.private_url_base = self.base_url + private_path
        self.public_url_base = self.base_url + API_KEY_PUBLIC_PATH

    def send_request(self, url, json=None, data=None, method='POST', headers=None, cookies=None):        
        if method=='POST':
            ret = requests.post(url, json=json, data=data, headers=headers, cookies=cookies)
        else:
            ret = requests.get(url, params=data, headers=headers, cookies=cookies)
        return ret
        
    def get_balance(self, account_type='trading', headers=None):

        data = {
                'account_type': account_type, #default account_type=trading
                }
        
        url = self.private_url_base + '/balance'
        ret = self.send_request(url, data, None, 'POST', headers, self.cookies)
        return ret
    
    def create_order(self, symbol, side, qty, price, _type='limit', user_id=0):
        data = {
            'cid': 'cid_' + uuid.uuid1().hex,
            'symbol': symbol,
            'side': side,
            'qty': qty,
            'price': price,
            'type': _type,
            'user_id': user_id
        }

        url = self.private_url_base + '/order/create'
        ret = self.send_request(url, data, None, 'POST', self.headers, self.cookies)
        print(ret.text)
        return ret
    
    def get_order_state(self, order_id, symbol):
        data = {'order_id': order_id,
                'symbol': symbol,
                }
        url = self.private_url_base  + '/order/state'
        ret = self.send_request(url, data, None, 'POST', self.headers, self.cookies)
        print(ret.text)
        return ret
    
    def cancel_order(self, order_id, symbol):
        data = {'order_id': order_id,
                'symbol': symbol,
                }

        url = self.private_url_base + '/order/cancel'
        ret = self.send_request(url, data, None, 'POST', self.headers, self.cookies)
        print(ret.text)
        return ret
    

class AwsexApiKeyClient(AwsClientBase):
    """
    Use api_key/api_secret as auth
    """
    def __init__(self, url_base, api_key=None, api_secret=None):
        super(AwsexApiKeyClient, self).__init__(url_base)

        self.api_key = api_key
        self.api_secret = api_secret

    def signature(self, api_secret, data):
        return hmac.new(api_secret, data, sha256).hexdigest()

    def get_data_str(self, data={}):
        '''
        Add nonce to data dict
        '''
        data['nonce'] = get_cur_time_ms()
        data_str = json.dumps(data, separators=(',', ':'))
        return data_str
    
    def get_signed_headers(self, data):
        signature = self.signature(self.api_secret.encode('utf8'), data.encode('utf8'))
        headers = {'api_key': self.api_key,
                   'signature': signature,
                   }
        return headers
    
    def signature_test(self):
        url = self.private_url_base + '/test'
        
        data_str = self.get_data_str()
        signed_headers = self.get_signed_headers(data_str)
        result = self.send_request(url, data=data_str, headers=signed_headers)
        return result
    
    def get_timestamp_ms(self):
        url = self.public_url_base + '/timestamp'
        result = self.send_request(url)
        return result

    def get_symbols(self, method='GET'):
        url = self.public_url_base + '/symbols'
        result = self.send_request(url, method=method)
        return result

    def get_balance(self, account_type='trading'):
        data = {
                'currency':"BTC",
                'account_type': account_type, #default account_type=trading
                }
        
        data_str = self.get_data_str(data)
        signed_headers = self.get_signed_headers(data_str)
        url = self.private_url_base + '/balance'
        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret
    
    def list_balance(self, account_type='trading'):
        data = {
                'account_type': account_type, #default account_type=trading
                }
        
        data_str = self.get_data_str(data)
        signed_headers = self.get_signed_headers(data_str)
        url = self.private_url_base + '/balance/list'
        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret
    
    def create_order(self, symbol, side, qty, price, _type='limit'):
        #cid: client define order id(uuid)
        data = {'cid': 'cid_' + uuid.uuid1().hex,
                'symbol': symbol,
                'side': side,
                'qty': qty,
                'price': price,
                'type':_type,
                }

        url = self.private_url_base + '/order/create'
        data_str = self.get_data_str(data)
        signed_headers = self.get_signed_headers(data_str)
        
#         print('create_order url=%s, data_str=%s' %(url, data_str))
        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret
    
    def get_order_state(self, order_id, symbol):
        data = {'order_id': order_id,
                'symbol': symbol,
                }
        
        url = self.private_url_base  + '/order/state'
        data_str = self.get_data_str(data)
        signed_headers = self.get_signed_headers(data_str)

        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret
    
    def cancel_order(self, order_id, symbol):
        data = {'order_id': order_id,
                'symbol': symbol,
                }

        url = self.private_url_base + '/order/cancel'
        data_str = self.get_data_str(data)
        signed_headers = self.get_signed_headers(data_str)

        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret

    def list_active_order(self, symbol):
        url = self.private_url_base + '/order/active/list'

        data = {
            'state': '',
            'side': '',
            'symbol': symbol,
            'start_tm_ms': 0,
            'end_tm_ms': get_cur_time_ms(),
            'limit': 20
        }
        if data['state']:
            assert data['state'] in ORDER_STATE_OPEN

        data_str = self.get_data_str(data);
        signed_headers = self.get_signed_headers(data_str)

        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret

    def list_history_order(self, symbol):
        data = {
            'state': '',
            'side': '',
            'symbol': symbol,
            'start_tm_ms': 0,
            'end_tm_ms': get_cur_time_ms(),
            'limit': 20
        }
        if data['state']:
            assert data['state'] in ORDER_STATE_CLOSED

        data_str = self.get_data_str(data);
        signed_headers = self.get_signed_headers(data_str)

        url = self.private_url_base + '/order/history/list'
        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret

    def list_trade(self, symbol):
        data = {
            'symbol': symbol,
            'start_tm_ms': 0,
            'end_tm_ms': get_cur_time_ms(),
            'limit': 20
        }
        data_str = self.get_data_str(data);
        signed_headers = self.get_signed_headers(data_str)

        url = self.private_url_base + '/trade/list'
        ret = self.send_request(url, None, data_str, 'POST', signed_headers, None)
        return ret
