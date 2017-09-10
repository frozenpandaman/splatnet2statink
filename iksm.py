# eli fessler
# clovervidia
import requests, json, re
import os, base64, hashlib, hmac
import getpass

session = requests.Session()

def log_in():
	'''Logs in to a Nintendo Account and returns a session_token.'''

	authenticated = False

	token = re.compile(r'(eyJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)')

	auth_state = base64.urlsafe_b64encode(os.urandom(36))

	auth_code_verifier = base64.urlsafe_b64encode(os.urandom(32))
	auth_cv_hash = hashlib.sha256()
	auth_cv_hash.update(auth_code_verifier.replace("=",""))
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
		'session_token_code_challenge':         auth_code_challenge.replace("=",""),
		'session_token_code_challenge_method': 'S256',
		'theme':                               'login_form'
	}

	url = 'https://accounts.nintendo.com/connect/1.0.0/authorize'
	r = session.get(url, headers=app_head, params=body)

	csrf_token = token.findall(r.text)[0]

	post_login = r.history[0].url

	print "\nNavigate to this URL in your browser:"
	print post_login
	print "Log in, right click the \"Use this account\" button, copy the link address, and paste it below:"
	while True:
		try:
			use_account_url = raw_input("")
			session_token_code = re.search('de=(.*)\&', use_account_url)
			return get_session_token(session_token_code.group(1), auth_code_verifier)
		except KeyboardInterrupt:
			print "\nBye!"
			exit(1)
		except:
			print "Malformed URL. Please try again, or press Ctrl+C to exit."
			print "URL:",

def get_session_token(session_token_code, auth_code_verifier):
	app_head = {
		'User-Agent':      'OnlineLounge/1.0.4 NASDKAPI Android',
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
		'session_token_code_verifier': auth_code_verifier.replace("=","")
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
		'User-Agent': 'OnlineLounge/1.0.4 NASDKAPI Android'
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
			'User-Agent': 'OnlineLounge/1.0.4 NASDKAPI Android',
			'Accept-Language': userLang,
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + id_response["access_token"],
			'Host': 'api.accounts.nintendo.com',
			'Connection': 'Keep-Alive',
			'Accept-Encoding': 'gzip'
		}
	except:
		print "Not a valid authorization request. Please delete config.txt and try again."
		print "Error from Nintendo:\n" + json.dumps(id_response, indent=2)
		exit(1)
	url = "https://api.accounts.nintendo.com/2.0.0/users/me"

	r = requests.get(url, headers=app_head)
	user_info = json.loads(r.text)

	nickname = user_info["nickname"]

	# get access token
	app_head = {
		'Host': 'api-lp1.znc.srv.nintendo.net',
		'Accept-Language': userLang,
		'User-Agent': 'com.nintendo.znca/1.0.4 (Android/7.1.2)',
		'Accept': 'application/json',
		'X-ProductVersion': '1.0.4',
		'Content-Type': 'application/json; charset=utf-8',
		'Connection': 'keep-alive',
		'Authorization': 'Bearer',
		'Content-Length': '906',
		'X-Platform': 'Android',
		'Accept-Encoding': 'gzip, deflate'
	}

	body = {}
	try:
		parameter = {
			'naIdToken': id_response["id_token"],
			'naCountry': user_info["country"],
			'naBirthday': user_info["birthday"],
			'language': user_info["language"]
		}
	except:
		print "Error(s) from Nintendo:\n" + json.dumps(id_response, indent=2)
		print json.dumps(user_info, indent=2)
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
			'User-Agent': 'com.nintendo.znca/1.0.4 (Android/7.1.2)',
			'Accept': 'application/json',
			'X-ProductVersion': '1.0.4',
			'Content-Type': 'application/json; charset=utf-8',
			'Connection': 'keep-alive',
			'Authorization': 'Bearer ' + splatoon_token["result"]["webApiServerCredential"]["accessToken"],
			'Content-Length': '37',
			'X-Platform': 'Android',
			'Accept-Encoding': 'gzip, deflate'
		}
	except:
		print "Error from Nintendo:\n" + json.dumps(splatoon_token, indent=2)
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
		print "Error from Nintendo:\n" + json.dumps(splatoon_access_token, indent=2)
		exit(1)

	url = "https://app.splatoon2.nintendo.net/?lang=" + userLang

	r = requests.get(url, headers=app_head)

	return r.cookies["iksm_session"], nickname