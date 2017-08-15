# clovervidia
import requests, json

CLIENT_ID = "71b963c1b7b6d119" # should be the same for everyone
SESSION_TOKEN = "" # put your session_token here, and keep it secret

def main():
	getIDToken()

def getIDToken():
	if SESSION_TOKEN == "":
		print "Please enter your session token in iksm.py."
		return None

	app_head = {
		'Host': 'accounts.nintendo.com',
		'Accept-Encoding': 'gzip, deflate',
		'Content-Type': 'application/json;charset=utf-8',
		'Accept-Language': 'en-US',
		'Content-Length': '437',
		'Accept': 'application/json',
		'Connection': 'keep-alive',
		'User-Agent': 'OnlineLounge/1.0.4 NASDKAPI Android'
	}

	body = {
		'client_id': CLIENT_ID,
		'session_token': SESSION_TOKEN,
		'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token'
	}

	url = "https://accounts.nintendo.com/connect/1.0.0/api/token"

	r = requests.post(url, headers=app_head, json=body)
	id_response = json.loads(r.text)

	return getUserInfo(id_response)

def getUserInfo(id_response):
	app_head = {
		'User-Agent': 'OnlineLounge/1.0.4 NASDKAPI Android',
		'Accept-Language': 'en-US',
		'Accept': 'application/json',
		'Authorization': 'Bearer ' + id_response["access_token"],
		'Host': 'api.accounts.nintendo.com',
		'Connection': 'Keep-Alive',
		'Accept-Encoding': 'gzip',
	}

	url = "https://api.accounts.nintendo.com/2.0.0/users/me"

	r = requests.get(url, headers=app_head)
	user_info = json.loads(r.text)

	return getAccessToken(id_response, user_info)

def getAccessToken(id_response, user_info):
	app_head = {
		'Host': 'api-lp1.znc.srv.nintendo.net',
		'Accept-Language': 'en-us',
		'User-Agent': 'com.nintendo.znca/1.0.4 (Android/7.1.2)',
		'Accept': 'application/json',
		'X-ProductVersion': '1.0.4',
		'Content-Type': 'application/json; charset=utf-8',
		'Connection': 'keep-alive',
		'Authorization': 'Bearer',
		'Content-Length': '906',
		'X-Platform': 'Android',
		'Accept-Encoding': 'gzip, deflate',
	}

	body = {}
	parameter = {
		'naIdToken': id_response["id_token"],
		'naCountry': user_info["country"],
		'naBirthday': user_info["birthday"],
		'language': user_info["language"],
	}
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v1/Account/Login"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_token = json.loads(r.text)

	return getSplatoonAccessToken(splatoon_token)

def getSplatoonAccessToken(splatoon_token):
	app_head = {
		'Host': 'api-lp1.znc.srv.nintendo.net',
		'Accept-Language': 'en-us',
		'User-Agent': 'com.nintendo.znca/1.0.4 (Android/7.1.2)',
		'Accept': 'application/json',
		'X-ProductVersion': '1.0.4',
		'Content-Type': 'application/json; charset=utf-8',
		'Connection': 'keep-alive',
		'Authorization': 'Bearer ' + splatoon_token["result"]["webApiServerCredential"]["accessToken"],
		'Content-Length': '37',
		'X-Platform': 'Android',
		'Accept-Encoding': 'gzip, deflate',
	}

	body = {}
	parameter = {
		"id": 5741031244955648,
	}
	body["parameter"] = parameter

	url = "https://api-lp1.znc.srv.nintendo.net/v1/Game/GetWebServiceToken"

	r = requests.post(url, headers=app_head, json=body)
	splatoon_access_token = json.loads(r.text)

	return getCookie(splatoon_access_token)

def getCookie(splatoon_access_token):
	app_head = {
		'Host': 'app.splatoon2.nintendo.net',
		'X-IsAppAnalyticsOptedIn': 'true',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'X-GameWebToken': splatoon_access_token["result"]["accessToken"],
		'Accept-Language': 'en-us',
		'X-IsAnalyticsOptedIn': 'true',
		'Connection': 'keep-alive',
		'DNT': '0',
		'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
	}

	url = "https://app.splatoon2.nintendo.net/?lang=en-US"

	r = requests.get(url, headers=app_head)

	return r.cookies["iksm_session"]

if __name__ == "__main__":
	main()
