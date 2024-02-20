# eli fessler
# clovervidia
from __future__ import print_function
from builtins import input
import requests, json, re, sys
import os, base64, hashlib, urllib
import uuid, time, random, string
from bs4 import BeautifulSoup

session = requests.Session()
version = "unknown"
nsoapp_version = "2.8.1"

# structure:
# log_in() -> get_session_token()
# get_cookie() -> call_imink_api() -> f
# enter_cookie()
# get_nsoapp_version()

# place config.txt in same directory as script (bundled or not)
if getattr(sys, 'frozen', False):
	app_path = os.path.dirname(sys.executable)
elif __file__:
	app_path = os.path.dirname(__file__)
config_path = os.path.join(app_path, "config.txt")

def get_nsoapp_version():
	'''Fetches the current Nintendo Switch Online app version from the Apple App Store.'''

	global nsoapp_version
	try:
		page = requests.get("https://apps.apple.com/us/app/nintendo-switch-online/id1234806557")
		soup = BeautifulSoup(page.text, 'html.parser')
		elt = soup.find("p", {"class": "whats-new__latest__version"})
		ver = elt.get_text().replace("Version ","").strip()
		return ver
	except:
		return nsoapp_version

def log_in(ver):
	'''Logs in to a Nintendo Account and returns a session_token.'''

	global version
	version = ver

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
		'User-Agent':                'Mozilla/5.0 (Linux; Android 14; Pixel 7a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36',
		'Accept':                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8n',
		'DNT':                       '1',
		'Accept-Encoding':           'gzip,deflate,br',
	}

	body = {
		'state':                               auth_state,
		'redirect_uri':                        'npf71b963c1b7b6d119://auth',
		'client_id':                           '71b963c1b7b6d119',
		'scope':                               'openid user user.birthday user.mii user.screenName',
		'response_type':                       'session_token_code',
		'session_token_code_challenge':        auth_code_challenge.replace(b"=", b""),
		'session_token_code_challenge_method': 'S256',
		'theme':                               'login_form'
	}

	print("\nMake sure you have fully read the \"Cookie generation\" section of the readme before proceeding. To manually input a cookie instead, enter \"skip\" at the prompt below.")
	print("\nNavigate to this URL in your browser:")
	print('https://accounts.nintendo.com/connect/1.0.0/authorize?{}'.format(urllib.parse.urlencode(body)))

	print("Log in, right click the \"Select this account\" button, copy the link address, and paste it below:")
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
		except AttributeError:
			print("Malformed URL. Please try again, or press Ctrl+C to exit.")
			print("URL:", end=' ')
		except KeyError: # session_token not found
			print("\nThe URL has expired. Please log out and back into your Nintendo Account and try again.")
			sys.exit(1)

def get_session_token(session_token_code, auth_code_verifier):
	'''Helper function for log_in().'''

	nsoapp_version = get_nsoapp_version()

	app_head = {
		'User-Agent':      'OnlineLounge/' + nsoapp_version + ' NASDKAPI Android',
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

	nsoapp_version = get_nsoapp_version()

	global version
	version = ver

	# timestamp = time.time_ns() // 1000000
	# guid = str(uuid.uuid4())

	app_head = {
		'Host':            'accounts.nintendo.com',
		'Accept-Encoding': 'gzip',
		'Content-Type':    'application/json; charset=utf-8',
		'Accept-Language': userLang,
		'Content-Length':  '439',
		'Accept':          'application/json',
		'Connection':      'Keep-Alive',
		'User-Agent':      'Dalvik/2.1.0 (Linux; U; Android 14; Pixel 7a Build/UQ1A.240105.004)'
	}

	body = {
		'client_id':     '71b963c1b7b6d119', # Splatoon 2 service
		'session_token': session_token,
		'grant_type':    'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token'
	}

	url = "https://accounts.nintendo.com/connect/1.0.0/api/token"

	r = requests.post(url, headers=app_head, json=body)
	id_response = json.loads(r.text)

	# get user info
	try:
		app_head = {
			'User-Agent':      'NASDKAPI; Android',
			'Accept-Language': userLang,
			'Accept':          'application/json',
			'Authorization':   'Bearer {}'.format(id_response["access_token"]),
			'Host':            'api.accounts.nintendo.com',
			'Connection':      'Keep-Alive',
			'Accept-Encoding': 'gzip'
		}
	except:
		print("Not a valid authorization request. Please delete config.txt and try again.")
		print("Error from Nintendo (in api/token step):")
		print(json.dumps(id_response, indent=2))
		sys.exit(1)
	url = "https://api.accounts.nintendo.com/2.0.0/users/me"

	r = requests.get(url, headers=app_head)
	user_info = json.loads(r.text)

	nickname = user_info["nickname"]
	na_id    = user_info["id"]

	# get access token
	app_head = {
		'Host':             'api-lp1.znc.srv.nintendo.net',
		'Accept-Language':  userLang,
		'User-Agent':       'com.nintendo.znca/' + nsoapp_version + ' (Android/14)',
		'Accept':           'application/json',
		'X-ProductVersion': nsoapp_version,
		'Content-Type':     'application/json; charset=utf-8',
		'Connection':       'Keep-Alive',
		'Authorization':    'Bearer',
		# 'Content-Length':   '1036',
		'X-Platform':       'Android',
		'Accept-Encoding':  'gzip'
	}

	body = {}
	try:
		idToken = id_response["id_token"]
		f, uuid, timestamp = call_imink_api(idToken, 1, na_id)

		parameter = {
			'f':          f,
			'naIdToken':  idToken,
			'timestamp':  timestamp,
			'requestId':  uuid,
			'naCountry':  user_info["country"],
			'naBirthday': user_info["birthday"],
			'language':   user_info["language"]
		}
	except SystemExit:
		sys.exit(1)
	except:
		print("Error(s) from Nintendo:")
		print(json.dumps(id_response, indent=2))
		print(json.dumps(user_info, indent=2))
		sys.exit(1)
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v3/Account/Login"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_token = json.loads(r.text)

	try:
		idToken       = splatoon_token["result"]["webApiServerCredential"]["accessToken"]
		coral_user_id = splatoon_token["result"]["user"]["id"]
		f, uuid, timestamp = call_imink_api(idToken, 2, na_id, coral_user_id)
	except:
		print("Error from Nintendo (in Account/Login step):")
		print(json.dumps(splatoon_token, indent=2))
		sys.exit(1)

	# get splatoon access token
	try:
		app_head = {
			'Host':             'api-lp1.znc.srv.nintendo.net',
			'User-Agent':       'com.nintendo.znca/' + nsoapp_version + ' (Android/14)',
			'Accept':           'application/json',
			'X-ProductVersion': nsoapp_version,
			'Content-Type':     'application/json; charset=utf-8',
			'Connection':       'Keep-Alive',
			'Authorization':    'Bearer {}'.format(splatoon_token["result"]["webApiServerCredential"]["accessToken"]),
			'Content-Length':   '37',
			'X-Platform':       'Android',
			'Accept-Encoding':  'gzip'
		}
	except:
		print("Error from Nintendo (in Account/Login step):")
		print(json.dumps(splatoon_token, indent=2))
		sys.exit(1)

	body = {}
	parameter = {
		'id':                5741031244955648,
		'f':                 f,
		'registrationToken': idToken,
		'timestamp':         timestamp,
		'requestId':         uuid,
	}
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v2/Game/GetWebServiceToken"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_access_token = json.loads(r.text)

	# get cookie
	try:
		app_head = {
			'Host':                    'app.splatoon2.nintendo.net',
			'X-IsAppAnalyticsOptedIn': 'false',
			'Accept':                  'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding':         'gzip,deflate',
			'X-GameWebToken':          splatoon_access_token["result"]["accessToken"],
			'Accept-Language':         userLang,
			'X-IsAnalyticsOptedIn':    'false',
			'Connection':              'keep-alive',
			'DNT':                     '1',
			'User-Agent':              'Mozilla/5.0 (Linux; Android 14; Pixel 7a Build/UQ1A.240105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.230 Mobile Safari/537.36',
			'X-Requested-With':        'com.nintendo.znca'
		}
	except:
		print("Error from Nintendo (in Game/GetWebServiceToken step):")
		print(json.dumps(splatoon_access_token, indent=2))
		sys.exit(1)

	url = "https://app.splatoon2.nintendo.net/?lang={}".format(userLang)
	r = requests.get(url, headers=app_head)
	return nickname, r.cookies["iksm_session"]

def call_imink_api(id_token, step, na_id, coral_user_id=None):
	'''Passes naIdToken & user ID to the imink API and fetches the response (f token, UUID, timestamp).'''

	try:
		api_head = {
			'User-Agent':   'splatnet2statink/{}'.format(version),
			'Content-Type': 'application/json; charset=utf-8'
		}
		api_body = {
			'token':       id_token,
			'hash_method': step,
			'na_id':       na_id
		}
		if step == 2 and coral_user_id is not None:
			api_body["coral_user_id"] = coral_user_id

		api_response = requests.post("https://api.imink.app/f", data=json.dumps(api_body), headers=api_head)
		resp = json.loads(api_response.text)

		f = resp["f"]
		uuid = resp["request_id"]
		timestamp = resp["timestamp"]
		return f, uuid, timestamp
	except:
		try: # if api_response never gets set
			if api_response.text:
				print(u"Error from the imink API:\n{}".format(json.dumps(json.loads(api_response.text), indent=2, ensure_ascii=False)))
			else:
				print("Error from the imink API: Error {}.".format(api_response.status_code))
		except:
			pass
		sys.exit(1)

def enter_cookie():
	'''Prompts the user to enter their iksm_session cookie'''

	new_cookie = input("Go to the page below to find instructions to obtain your iksm_session cookie:\nhttps://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions\nEnter it here: ")
	while len(new_cookie) != 40:
		new_cookie = input("Cookie is invalid. Please enter it again.\nCookie: ")
	return new_cookie
