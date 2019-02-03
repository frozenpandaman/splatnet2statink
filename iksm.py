# eli fessler
# clovervidia
from __future__ import print_function
from builtins import input
import requests, json, re, sys
import os, base64, hashlib
import uuid, time

session = requests.Session()
version = "unknown"

def log_in(ver):
	'''Logs in to a Nintendo Account and returns a session_token.'''

	global version
	version = ver

	token = re.compile(r'(eyJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)')

	auth_state = base64.urlsafe_b64encode(os.urandom(36))

	auth_code_verifier = base64.urlsafe_b64encode(os.urandom(32))
	auth_cv_hash = hashlib.sha256()
	auth_cv_hash.update(auth_code_verifier.replace(b"=", b""))
	auth_code_challenge = base64.urlsafe_b64encode(auth_cv_hash.digest())

	app_head = {
		'Host':                      'accounts.nintendo.com',
		'Connection':                'keep-alive',
		'Cache-Control':             'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent':                'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
		'Accept':                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8n',
		'DNT':                       '1',
		'Accept-Encoding':           'gzip,deflate,br',
	}

	body = {
		'state':                                auth_state,
		'redirect_uri':                         'npf71b963c1b7b6d119://auth',
		'client_id':                            '71b963c1b7b6d119',
		'scope':                                'openid user user.birthday user.mii user.screenName',
		'response_type':                        'session_token_code',
		'session_token_code_challenge':         auth_code_challenge.replace(b"=", b""),
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
	print("Log in, right click the \"Select this person\" button, copy the link address, and paste it below:")
	while True:
		try:
			use_account_url = input("")
			if use_account_url == "skip":
				return "skip"
			session_token_code = re.search('de=(.*)&', use_account_url)
			return get_session_token(session_token_code.group(1), auth_code_verifier)
		except KeyboardInterrupt:
			print("\nBye!")
			sys.exit(1)
		except:
			print("Malformed URL. Please try again, or press Ctrl+C to exit.")
			print("URL:", end=' ')

def get_session_token(session_token_code, auth_code_verifier):
	'''Helper function for log_in().'''

	app_head = {
		'User-Agent':      'OnlineLounge/1.4.1 NASDKAPI Android',
		'Accept-Language': 'en-US',
		'Accept':          'application/json',
		'Content-Type':    'application/x-www-form-urlencoded',
		'Content-Length':  '540',
		'Host':            'accounts.nintendo.com',
		'Connection':      'Keep-Alive',
		'Accept-Encoding': 'gzip'
	}

	body = {
		'client_id':                   '71b963c1b7b6d119',
		'session_token_code':          session_token_code,
		'session_token_code_verifier': auth_code_verifier.replace(b"=", b"")
	}

	url = 'https://accounts.nintendo.com/connect/1.0.0/api/session_token'

	r = session.post(url, headers=app_head, data=body)
	return json.loads(r.text)["session_token"]

def get_cookie(session_token, userLang, ver):
	'''Returns a new cookie provided the session_token.'''

	global version
	version = ver

	timestamp = int(time.time())
	guid = str(uuid.uuid4())

	app_head = {
		'Host': 'accounts.nintendo.com',
		'Accept-Encoding': 'gzip',
		'Content-Type': 'application/json; charset=utf-8',
		'Accept-Language': userLang,
		'Content-Length': '437',
		'Accept': 'application/json',
		'Connection': 'Keep-Alive',
		'User-Agent': 'OnlineLounge/1.4.1 NASDKAPI Android'
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
			'User-Agent': 'OnlineLounge/1.4.1 NASDKAPI Android',
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
		sys.exit(1)
	url = "https://api.accounts.nintendo.com/2.0.0/users/me"

	r = requests.get(url, headers=app_head)
	user_info = json.loads(r.text)

	nickname = user_info["nickname"]

	# get access token
	app_head = {
		'Host': 'api-lp1.znc.srv.nintendo.net',
		'Accept-Language': userLang,
		'User-Agent': 'com.nintendo.znca/1.4.1 (Android/7.1.2)',
		'Accept': 'application/json',
		'X-ProductVersion': '1.4.1',
		'Content-Type': 'application/json; charset=utf-8',
		'Connection': 'Keep-Alive',
		'Authorization': 'Bearer',
		'Content-Length': '1036',
		'X-Platform': 'Android',
		'Accept-Encoding': 'gzip'
	}

	body = {}
	try:
		idToken = id_response["id_token"]
		parameter = {
			'f': get_f_from_flapg_api(idToken, guid, timestamp),
			'naIdToken': idToken,
			'naCountry': user_info["country"],
			'naBirthday': user_info["birthday"],
			'language': user_info["language"],
			'requestId': guid,
			'timestamp': timestamp
		}
	except SystemExit:
		sys.exit(1)
	except:
		print("Error(s) from Nintendo:")
		print(json.dumps(id_response, indent=2))
		print(json.dumps(user_info, indent=2))
		sys.exit(1)
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v1/Account/Login"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_token = json.loads(r.text)

	# get splatoon access token
	try:
		app_head = {
			'Host': 'api-lp1.znc.srv.nintendo.net',
			'User-Agent': 'com.nintendo.znca/1.4.1 (Android/7.1.2)',
			'Accept': 'application/json',
			'X-ProductVersion': '1.4.1',
			'Content-Type': 'application/json; charset=utf-8',
			'Connection': 'Keep-Alive',
			'Authorization': 'Bearer {}'.format(splatoon_token["result"]["webApiServerCredential"]["accessToken"]),
			'Content-Length': '37',
			'X-Platform': 'Android',
			'Accept-Encoding': 'gzip'
		}
	except:
		print("Error from Nintendo:")
		print(json.dumps(splatoon_token, indent=2))
		sys.exit(1)

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
			'X-IsAppAnalyticsOptedIn': 'false',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip,deflate',
			'X-GameWebToken': splatoon_access_token["result"]["accessToken"],
			'Accept-Language': userLang,
			'X-IsAnalyticsOptedIn': 'false',
			'Connection': 'keep-alive',
			'DNT': '0',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
			'X-Requested-With': 'com.nintendo.znca'
		}
	except:
		print("Error from Nintendo:")
		print(json.dumps(splatoon_access_token, indent=2))
		sys.exit(1)

	url = "https://app.splatoon2.nintendo.net/?lang={}".format(userLang)

	r = requests.get(url, headers=app_head)

	return r.cookies["iksm_session"]

def get_hash_from_s2s_api(id_token, timestamp):
	'''Passes an id_token and timestamp to the s2s API and fetches the resultant hash from the response.'''

	# check to make sure we're allowed to contact the API. stop spamming my web server pls
	config_file = open("config.txt", "r")
	config_data = json.load(config_file)
	config_file.close()
	try:
		num_errors = config_data["api_errors"]
	except:
		num_errors = 0

	if num_errors >= 5:
		print("Too many errors received from the splatnet2statink API. Further requests have been blocked until the \"api_errors\" line is manually removed from config.txt. If this issue persists, please contact @frozenpandaman on Twitter/GitHub for assistance.")
		sys.exit(1)

	# proceed normally
	try:
		api_app_head = { 'User-Agent': "splatnet2statink/{}".format(version) }
		api_body = { 'naIdToken': id_token, 'timestamp': timestamp }
		api_response = requests.post("https://elifessler.com/s2s/api/gen", headers=api_app_head, data=api_body)
		return json.loads(api_response.text)["hash"]
	except:
		print("Error from the splatnet2statink API:\n{}".format(json.dumps(json.loads(api_response.text), indent=2)))

		# add 1 to api_errors in config
		config_file = open("config.txt", "r")
		config_data = json.load(config_file)
		config_file.close()
		try:
			num_errors = config_data["api_errors"]
		except:
			num_errors = 0
		num_errors += 1
		config_data["api_errors"] = num_errors

		config_file = open("config.txt", "w") # from write_config()
		config_file.seek(0)
		config_file.write(json.dumps(config_data, indent=4, sort_keys=True, separators=(',', ': ')))
		config_file.close()

		sys.exit(1)

def get_f_from_flapg_api(id_token, guid, timestamp):
	'''Passes in headers to the flapg API (Android emulator) and fetches the f token from the response.'''

	try:
		api_app_head = {
			'x-token': id_token,
			'x-time': str(timestamp),
			'x-guid': guid,
			'x-hash': get_hash_from_s2s_api(id_token, timestamp)
		}
		api_response = requests.get("https://flapg.com/ika2/api/login", headers=api_app_head)
		f = json.loads(api_response.text)['f']
		return f
	except:
		try: # if api_response never gets set
			if api_response.text:
				print("Error from the flapg API:\n{}".format(json.dumps(json.loads(api_response.text), indent=2)))
			elif api_response.status_code == requests.codes.not_found:
				print("Error from the flapg API: Error 404 (incorrect headers).")
			else:
				print("Error from the flapg API: Error {}.".format(api_response.status_code))
		except:
			pass
		sys.exit(1)

def enter_cookie():
	'''Prompts the user to enter their iksm_session cookie'''

	new_cookie = input("Go to the page below to find instructions to obtain your iksm_session cookie:\nhttps://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions\nEnter it here: ")
	while len(new_cookie) != 40:
		new_cookie = input("Cookie is invalid. Please enter it again.\nCookie: ")
	return new_cookie
