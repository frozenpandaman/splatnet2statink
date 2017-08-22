# The MIT License

# Copyright (c) 2017 Daniel

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import base64
import hashlib
import hmac
import random
import re
import string
import json

Session = requests.Session()
Retrier = Retry(total=3, read=3, connect=3, backoff_factor=0.3, status_forcelist=(500, 502, 504))
adapter = HTTPAdapter(max_retries=Retrier)
Session.mount('http://', adapter)
Session.mount('https://', adapter)

JWToken = re.compile(r'(eyJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)')
ClientID = '71b963c1b7b6d119'

class Nintendo(object):
    def __init__(self, session_token=''):
        self.session_token = session_token
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'com.nintendo.znca/1.0.4 (Android/6.0.1)'
        }

    def access_token(self, service):
        url = 'https://accounts.nintendo.com/connect/1.0.0/api/token'
        payload = {
            'client_id': ClientID,
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token',
            'session_token': self.session_token
        }
        content = Session.post(url, json=payload, headers=self.headers).json()

        url = 'https://api-lp1.znc.srv.nintendo.net/v1/Account/GetToken'
        payload = {
            'parameter': {
                'naIdToken': content['id_token'],
                'naCountry': 'null',
                'naBirthday': 'null',
                'language': 'null'
            }
        }
        self.headers['Authorization'] = 'Bearer {}'.format(content['access_token'])
        content = Session.post(url, json=payload, headers=self.headers).json()

        url = 'https://api-lp1.znc.srv.nintendo.net/v1/Game/ListWebServices'
        payload = {}
        self.headers['Authorization'] = 'Bearer {}'.format(content['result']['webApiServerCredential']['accessToken'])
        content = Session.post(url, json=payload, headers=self.headers).json()
        serivce = list(filter(lambda x: x['name'] == service, content['result']))[0]

        url = 'https://api-lp1.znc.srv.nintendo.net/v1/Game/GetWebServiceToken'
        payload = {
            'parameter': {
                'id': serivce['id']
            }
        }
        content = Session.post(url, json=payload, headers=self.headers).json()
        return content['result']['accessToken']


class Splatoon(Nintendo):
    def __init__(self, arg):
        super(Splatoon, self).__init__(arg)

        url = 'https://app.splatoon2.nintendo.net'
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
            'x-gamewebtoken': self.access_token('Splatoon 2')
        }
        content = Session.get(url, headers=headers).text

        self.unique_id = re.findall(r'data-unique-id="(\d*)"', content)[0]
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-unique-id': self.unique_id
        }

    def get_stages(self):
        url = 'https://app.splatoon2.nintendo.net/api/data/stages'
        content = Session.get(url, headers=self.headers).json()
        return content

    def get_festivals(self):
        url = 'https://app.splatoon2.nintendo.net/api/festivals/active'
        content = Session.get(url, headers=self.headers).json()
        return content

    def get_schedules(self):
        url = 'https://app.splatoon2.nintendo.net/api/schedules'
        content = Session.get(url, headers=self.headers).json()
        return content

    def get_records(self):
        url = 'https://app.splatoon2.nintendo.net/api/records'
        content = Session.get(url, headers=self.headers).json()
        return content

    def get_results(self):
        url = 'https://app.splatoon2.nintendo.net/api/results'
        content = Session.get(url, headers=self.headers).json()
        return content

    def get_timeline(self):
        url = 'https://app.splatoon2.nintendo.net/api/timeline'
        content = Session.get(url, headers=self.headers).json()
        return content

    def get_merchandises(self):
        url = 'https://app.splatoon2.nintendo.net/api/onlineshop/merchandises'
        content = Session.get(url, headers=self.headers).json()
        return content

    def buy_merchandises(self, mid):
        url = 'https://app.splatoon2.nintendo.net/api/onlineshop/order/{}'.format(mid)
        content = Session.post(url, files={'override': (None, '1')}, headers=self.headers).json()
        return content
