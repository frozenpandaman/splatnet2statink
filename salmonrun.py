# eli fessler
from __future__ import print_function
from builtins import input
import requests, json

version = "unknown"
cookie = ""
api_key = ""
app_head = {}

def salmon_load_json():
	'''Returns Salmon Run summary JSON from online.'''

	print("Pulling Salmon Run data from online...")
	url = "https://app.splatoon2.nintendo.net/api/coop_results"
	results_list = requests.get(url, headers=app_head, cookies=dict(iksm_session=cookie))
	return json.loads(results_list.text)

def salmon_post_profile(profile):
	''' Update stat.ink Salmon Run stats/profile.'''

	payload = {
		"work_count":        profile["card"]["job_num"],
		"total_golden_eggs": profile["card"]["golden_ikura_total"],
		"total_eggs":        profile["card"]["ikura_total"],
		"total_rescued":     profile["card"]["help_total"],
		"total_point":       profile["card"]["kuma_point_total"]
	}

	url  = 'https://stat.ink/api/v2/salmon-stats'
	auth = {'Authorization': 'Bearer {}'.format(api_key)}
	updateprofile = requests.post(url, headers=auth, data=payload)

	if updateprofile.ok:
		print("Successfully updated your Salmon Run profile.")
	else:
		print("Error from stat.ink:")
		print(updateprofile.text)

def salmon_post_shift(i, results):
	'''Uploads shift #i from the provided results dictionary.'''

	print("Not implemented yet by the stat.ink API.")
	exit(0)

	# payload = {'agent': 'splatnet2statink', 'agent_version': version, 'automated': 'yes'}

	# job_id = results[i]["job_id"]
	# principal_id = results[i]["my_result"]["pid"]
	# namespace = uuid.UUID(u'{73cf052a-fd0b-11e7-a5ee-001b21a098c2}')
	# name = "{}@{}".format(job_id, principal_id)
	# payload["uuid"] = str(uuid.uuid5(namespace, name))

	# title_num = int(results[i]["grade"]["id"])
	# translate_titles = {5: "profreshional", 4: "overachiever", 3: "go_getter", 2: "part_timer", 1: "apprentice", 0: "intern"}
	# payload["title"] = translate_titles[title_num]

	# ...

	# url  = 'https://stat.ink/api/v2/salmon'
	# auth = {'Authorization': 'Bearer {}'.format(api_key), 'Content-Type': 'application/json'}
	# postshift = requests.post(url, headers=auth, data=payload)

	# # Response
	# headerloc = postshift.headers.get('location')
	# if headerloc != None:
	# 	if postshift.status_code == 302: # receive redirect
	# 		print("Shift #{} already uploaded to {}".format(i+1, headerloc))
	# 		# continue trying to upload remaining
	# 	else: # http status code should be OK (200)
	# 		print("Shift #{} uploaded to {}".format(i+1, headerloc))
	# else: # error of some sort
	# 	print("Error uploading shift #{}. Message from server:".format(i+1))
	# 	print(postshift.content.decode("utf-8"))
	# 	if i != 0: # don't prompt for final shift
	# 		cont = input('Continue? [Y/n] ')
	# 		if cont[0].lower() == "n":
	# 			print("Exiting.")
	# 			exit(1)

def salmon_get_data():
	'''Retrieves JSON data from SplatNet.'''

	data = salmon_load_json()
	if cookie == "" or "code" in data:
		print("Blank or invalid cookie. Please run splatnet2statink in non-Salmon Run mode to obtain a cookie.")
		exit(1)

	try:
		profile = data["summary"]
		results = data["results"]
	except KeyError:
		print("Error reading JSON from online.")
		exit(1)

	return profile, results

def salmon_get_num_shifts():
	'''Prompt user to upload a certain number of recent shift data.'''

	try:
		n = int(input("Number of recent Salmon Run shifts to upload (0-50)? "))
	except ValueError:
		print("Exiting without uploading any shifts.")
		exit(0)
	if n < 1:
		print("Exiting without uploading any shifts.")
		exit(0)
	elif n > 50:
		print("SplatNet 2 only stores the 50 most recent shifts. Exiting.")
		exit(1)
	else:
		return n

def upload_salmon_run(s2s_version, s2s_cookie, s2s_api_key, s2s_app_head):
	'''Main process for uploading Salmon Run shifts.'''

	global version
	version = s2s_version
	global cookie
	cookie = s2s_cookie
	global api_key
	api_key = s2s_api_key
	global app_head
	app_head = s2s_app_head

	profile, results = salmon_get_data()
	salmon_post_profile(profile)
	# n = salmon_get_num_shifts()
	# for i in reversed(range(n)):
	# 	salmon_post_shift(i, results)