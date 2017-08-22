#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

class Login(object):
    def __init__(self, username, password):
        self.session_token = self.login(username, password)

    def rand(self):
        return ''.join(random.choice(string.ascii_letters) for _ in range(50))

    def hash(self, text):
        text = hashlib.sha256(text.encode()).digest()
        text = base64.urlsafe_b64encode(text).decode()
        return text.replace('=', '')

    def hmac(self, username, password, csrf_token):
        msg = '{}:{}:{}'.format(username, password, csrf_token)
        return hmac.new(csrf_token[-8:].encode(), msg=msg.encode(), digestmod=hashlib.sha256).hexdigest()

    def unpack(self, data):
        data = data.split('.')[1]
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += '='* (4 - missing_padding)
        return json.loads(base64.urlsafe_b64decode(data.encode()))

    def login(self, username, password):
        verifier = self.rand()
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'OnlineLounge/1.0.4 NASDKAPI Android'
        }
        while True:
            print('Try Login...')
            url = 'https://accounts.nintendo.com/connect/1.0.0/authorize'
            payload = {
                'client_id'                           : ClientID,
                'redirect_uri'                        : 'npf{}://auth'.format(ClientID),
                'response_type'                       : 'session_token_code',
                'scope'                               : 'openid user user.birthday user.mii user.screenName',
                'session_token_code_challenge'        : self.hash(verifier),
                'session_token_code_challenge_method' : 'S256',
                'state'                               : self.rand(),
                'theme'                               : 'login_form'
            }
            content = Session.get(url, params=payload, headers=headers).text
            csrf_token = JWToken.findall(content)[0]
            post_login = self.unpack(csrf_token)['_ext']['p']['post_login_redirect_uri']

            url = 'https://accounts.nintendo.com/login'
            payload = {
                'csrf_token'                          : csrf_token,
                'display'                             : '',
                'post_login_redirect_uri'             : post_login,
                'redirect_after'                      : 5,
                'subject_id'                          : username,
                'subject_password'                    : password,
                '_h'                                  : self.hmac(username, password, csrf_token),
            }
            content = Session.post(url, data=payload, headers=headers).text
            token_code = JWToken.findall(content)[0]
            if self.unpack(token_code)['typ'] == 'session_token_code':
                break

        url = 'https://accounts.nintendo.com/connect/1.0.0/api/session_token'
        payload = {
            'client_id': ClientID,
            'session_token_code': token_code,
            'session_token_code_verifier': verifier
        }
        content = Session.post(url, data=payload, headers=headers).json()
        return content['session_token']

def main():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    session_token = Login(username, password).session_token

    print('Here is your session_token:')
    print(session_token)

if __name__ == '__main__':
    main()
