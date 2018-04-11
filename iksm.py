# eli fessler
# clovervidia
from __future__ import print_function
from builtins import input
import requests, json, re
import os, base64, hashlib, hmac
import getpass

session = requests.Session()
version = "unknown"

def log_in(ver):
	'''Logs in to a Nintendo Account and returns a session_token.'''

	authenticated = False

	global version
	version = ver

	token = re.compile(r'(eyJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)')

	auth_state = base64.urlsafe_b64encode(os.urandom(36))

	auth_code_verifier = base64.urlsafe_b64encode(os.urandom(32))
	auth_cv_hash = hashlib.sha256()
	auth_cv_hash.update(auth_code_verifier.replace(b"=",b""))
	auth_code_challenge = base64.urlsafe_b64encode(auth_cv_hash.digest())

	app_head = {
		'Host':                      'accounts.nintendo.com',
		'Connection':                'keep-alive',
		'Cache-Control':             'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent':                'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
		'Accept':                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8n',
		'DNT':                       '1',
		'Accept-Encoding':           'gzip, deflate, br',
	}

	body = {
		'state':                                auth_state,
		'redirect_uri':                         'npf71b963c1b7b6d119://auth',
		'client_id':                            '71b963c1b7b6d119',
		'scope':                                'openid user user.birthday user.mii user.screenName',
		'response_type':                        'session_token_code',
		'session_token_code_challenge':         auth_code_challenge.replace(b"=",b""),
		'session_token_code_challenge_method': 'S256',
		'theme':                               'login_form'
	}

	url = 'https://accounts.nintendo.com/connect/1.0.0/authorize'
	r = session.get(url, headers=app_head, params=body)

	csrf_token = token.findall(r.text)[0]

	post_login = r.history[0].url

	print("\nMake sure you have fully read the \"Cookie generation\" section of the readme before proceeding. To manually input a cookie instead, enter \"skip\" at the prompt below.")
	print("\nNavigate to this URL in your browser:")
	print(post_login)
	print("Log in, right click the \"Use this account\" button, copy the link address, and paste it below:")
	while True:
		try:
			use_account_url = input("")
			if use_account_url == "skip":
				return "skip"
			session_token_code = re.search('de=(.*)\&', use_account_url)
			return get_session_token(session_token_code.group(1), auth_code_verifier)
		except KeyboardInterrupt:
			print("\nBye!")
			exit(1)
		except:
			print("Malformed URL. Please try again, or press Ctrl+C to exit.")
			print("URL:", end=' ')

def get_session_token(session_token_code, auth_code_verifier):
	'''Helper function for log_in().'''

	app_head = {
		'User-Agent':      'OnlineLounge/1.1.2 NASDKAPI Android',
		'Accept-Language': 'en-US',
		'Accept':          'application/json',
		'Content-Type':    'application/x-www-form-urlencoded',
		'Host':            'accounts.nintendo.com',
		'Connection':      'Keep-Alive',
		'Accept-Encoding': 'gzip'
	}

	body = {
		'client_id':                   '71b963c1b7b6d119',
		'session_token_code':          session_token_code,
		'session_token_code_verifier': auth_code_verifier.replace(b"=",b"")
	}

	url = 'https://accounts.nintendo.com/connect/1.0.0/api/session_token'

	r = session.post(url, headers=app_head, data=body)
	return json.loads(r.text)["session_token"]

def get_cookie(session_token, userLang):
	'''Returns a new cookie provided the session_token.'''

	app_head = {
		'Host': 'accounts.nintendo.com',
		'Accept-Encoding': 'gzip, deflate',
		'Content-Type': 'application/json;charset=utf-8',
		'Accept-Language': userLang,
		'Content-Length': '437',
		'Accept': 'application/json',
		'Connection': 'keep-alive',
		'User-Agent': 'OnlineLounge/1.1.2 NASDKAPI Android'
	}

	body = {
		'client_id': '71b963c1b7b6d119', # should always be the same
		'session_token': session_token,
		'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token'
	}

	url = "https://accounts.nintendo.com/connect/1.0.0/api/token"

	r = requests.post(url, headers=app_head, json=body)
	id_response = json.loads(r.text)

	# get user info
	try:
		app_head = {
			'User-Agent': 'OnlineLounge/1.1.2 NASDKAPI Android',
			'Accept-Language': userLang,
			'Accept': 'application/json',
			'Authorization': 'Bearer {}'.format(id_response["access_token"]),
			'Host': 'api.accounts.nintendo.com',
			'Connection': 'Keep-Alive',
			'Accept-Encoding': 'gzip'
		}
	except:
		print("Not a valid authorization request. Please delete config.txt and try again.")
		print("Error from Nintendo:")
		print(json.dumps(id_response, indent=2))
		exit(1)
	url = "https://api.accounts.nintendo.com/2.0.0/users/me"

	r = requests.get(url, headers=app_head)
	user_info = json.loads(r.text)

	nickname = user_info["nickname"]

	# get access token
	app_head = {
		'Host': 'api-lp1.znc.srv.nintendo.net',
		'Accept-Language': userLang,
		'User-Agent': 'com.nintendo.znca/1.1.2 (Android/7.1.2)',
		'Accept': 'application/json',
		'X-ProductVersion': '1.1.2',
		'Content-Type': 'application/json; charset=utf-8',
		'Connection': 'keep-alive',
		'Authorization': 'Bearer',
		'Content-Length': '987',
		'X-Platform': 'Android',
		'Accept-Encoding': 'gzip'
	}

	body = {}
	try:
		parameter = {
			'f': get_f_from_s2s_api(id_response["id_token"]),
			'naIdToken': id_response["id_token"],
			'naCountry': user_info["country"],
			'naBirthday': user_info["birthday"],
			'language': user_info["language"]
		}
	except:
		print("Error(s) from Nintendo:")
		print(json.dumps(id_response, indent=2))
		print(json.dumps(user_info, indent=2))
		exit(1)
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v1/Account/Login"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_token = json.loads(r.text)

	# get splatoon access token
	try:
		app_head = {
			'Host': 'api-lp1.znc.srv.nintendo.net',
			'Accept-Language': userLang,
			'User-Agent': 'com.nintendo.znca/1.1.2 (Android/7.1.2)',
			'Accept': 'application/json',
			'X-ProductVersion': '1.1.2',
			'Content-Type': 'application/json; charset=utf-8',
			'Connection': 'keep-alive',
			'Authorization': 'Bearer {}'.format(splatoon_token["result"]["webApiServerCredential"]["accessToken"]),
			'Content-Length': '37',
			'X-Platform': 'Android',
			'Accept-Encoding': 'gzip, deflate'
		}
	except:
		print("Error from Nintendo:")
		print(json.dumps(splatoon_token, indent=2))
		exit(1)

	body = {}
	parameter = {
		"id": 5741031244955648
	}
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v1/Game/GetWebServiceToken"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_access_token = json.loads(r.text)

	# get cookie
	try:
		app_head = {
			'Host': 'app.splatoon2.nintendo.net',
			'X-IsAppAnalyticsOptedIn': 'true',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'X-GameWebToken': splatoon_access_token["result"]["accessToken"],
			'Accept-Language': userLang,
			'X-IsAnalyticsOptedIn': 'true',
			'Connection': 'keep-alive',
			'DNT': '0',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36'
		}
	except:
		print("Error from Nintendo:")
		print(json.dumps(splatoon_access_token, indent=2))
		exit(1)

	url = "https://app.splatoon2.nintendo.net/?lang={}".format(userLang)

	r = requests.get(url, headers=app_head)

	return r.cookies["iksm_session"]

def get_f_from_s2s_api(id_token):
	'''Passes an id_token to the splatnet2statink API and fetches the f token from the response.'''
	try:
		api_app_head = { 'User-Agent': "splatnet2statink/" + version }
		api_body = { 'naIdToken': id_token }
		api_response = requests.post("https://elifessler.com/s2s/api/gen", headers=api_app_head, data=api_body)
		return json.loads(api_response.text)["f"]
	except:
		print("Error from the splatnet2statink API:\n" + json.dumps(json.loads(api_response.text), indent=2))
		exit(1)

def enter_cookie():
	'''Prompts the user to enter their iksm_session cookie'''

	new_cookie = input("Go to the page below to find instructions to obtain your iksm_session cookie:\nhttps://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions\nEnter it here: ")
	while len(new_cookie) != 40:
		new_cookie = input("Cookie is invalid. Please enter it again.\nCookie: ")
	return new_cookie
