# eli fessler
from __future__ import print_function
from builtins import input
import requests, json, uuid
import dbs

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

	## PRINT OUT, DON'T UPLOAD
	print("\nYour profile:")
	for x in payload:
		print("{}: {}".format(x, payload[x]))
	print()
	# url  = 'https://stat.ink/api/v2/salmon-stats'
	# auth = {'Authorization': 'Bearer {}'.format(api_key)}
	# updateprofile = requests.post(url, headers=auth, data=payload)

	# if updateprofile.ok:
	# 	print("Successfully updated your Salmon Run profile.")
	# else:
	# 	print("Error from stat.ink:")
	# 	print(updateprofile.text)

def salmon_post_shift(i, results):
	'''Uploads shift #i from the provided results dictionary.'''

	payload = {'agent': 'splatnet2statink', 'agent_version': version, 'automated': 'yes'}

	# stat.ink UUID
	job_id = results[i]["job_id"]
	principal_id = results[i]["my_result"]["pid"]
	namespace = uuid.UUID(u'{73cf052a-fd0b-11e7-a5ee-001b21a098c2}')
	name = "{}@{}".format(job_id, principal_id)
	payload["uuid"] = str(uuid.uuid5(namespace, name))

	###############################
	# Consistent throughout shift #
	###############################

	# Title
	title_num = int(results[i]["grade"]["id"])
	translate_titles = {5: "profreshional", 4: "overachiever", 3: "go_getter", 2: "part_timer", 1: "apprentice", 0: "intern"}
	payload["title"] = translate_titles[title_num]

	# Stage
	stage_img_url = results[i]["schedule"]["stage"]["image"]
	if "6d68f5baa75f3a94e5e9bfb89b82e7377e3ecd2c" in stage_img_url:
		payload["stage"] = "shaketoba"
	elif "e07d73b7d9f0c64e552b34a2e6c29b8564c63388" in stage_img_url:
		payload["stage"] = "donburako"
	elif "e9f7c7b35e6d46778cd3cbc0d89bd7e1bc3be493" in stage_img_url:
		payload["stage"] = "tokishirazu"
	elif "65c68c6f0641cc5654434b78a6f10b0ad32ccdee" in stage_img_url:
		payload["stage"] = "dam"

	# Special weapon
	translate_specials = {2: "pitcher", 7: "presser", 8: "jetpack", 9: "chakuchi"}
	payload["special_weapon"] = translate_specials[int(results[i]["my_result"]["special"]["id"])]

	# Boss count
	num_of_bosses = {}
	num_of_bosses["goldie"]    = results[i]["boss_counts"]["3"]["count"]
	num_of_bosses["steelhead"] = results[i]["boss_counts"]["6"]["count"]
	num_of_bosses["flyfish"]   = results[i]["boss_counts"]["9"]["count"]
	num_of_bosses["scrapper"]  = results[i]["boss_counts"]["12"]["count"]
	num_of_bosses["steel_eel"] = results[i]["boss_counts"]["13"]["count"]
	num_of_bosses["stinger"]   = results[i]["boss_counts"]["14"]["count"]
	num_of_bosses["maws"]      = results[i]["boss_counts"]["15"]["count"]
	num_of_bosses["griller"]   = results[i]["boss_counts"]["16"]["count"]
	num_of_bosses["drizzler"]  = results[i]["boss_counts"]["21"]["count"]
	payload["boss"] = num_of_bosses

	##################
	# Wave-dependent #
	##################

	num_waves = len(results[i]["wave_details"])
	print(num_waves)
	for wave in range(num_waves):
		wave_str = "wave_{}".format(wave+1)
		payload[wave_str] = {}

		# Water level
		payload[wave_str]["water_level"] = results[i]["wave_details"][wave]["water_level"]["key"] # low, normal, high

		# Known Occurrence
		# cohock_charge, fog, goldie_seeking, griller, mothership, rush
		event = results[i]["wave_details"][wave]["event_type"]["key"].replace("the-", "", 1).replace("-", "_")
		if event != "water_levels":
			payload[wave_str]["known_occurrence"] = event

		# Main Weapon
		payload[wave_str]["main_weapon"] = dbs.weapons.get(int(results[i]["my_result"]["weapon_list"][wave]["id"]), "")

	## PRINT OUT, DON'T UPLOAD
	print("\nShift details:")
	for x in payload:
		print("{}: {}".format(x, payload[x]))
	##########
	## POST ##
	##########
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

def salmon_get_num_shifts(results):
	'''Prompt user to upload a certain number of recent shift data.'''

	try:
		n = int(input("Number of recent Salmon Run shifts to upload (0-50)? "))
	except ValueError:
		print("Please enter an integer between 0 and 50. Exiting.")
		exit(0)
	if n < 1:
		print("Exiting without uploading any shifts.")
		exit(0)
	elif n > 50:
		print("SplatNet 2 only stores the 50 most recent shifts. Exiting.")
		exit(1)

	if len(results) == 0:
		print("You do not have any Salmon Run shifts recorded on SplatNet 2. Exiting.")
		exit(1)
	elif n > len(results):
		print("You do not have {} Salmon Run shifts recorded on SplatNet 2. Uploading all {}.".format(n, len(results)))
		n = len(results)

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

	print("\nNOTE: Not fully implemented or ready for use! This only prints out your Salmon Run info and doesn't upload anything yet.\n")

	profile, results = salmon_get_data()
	salmon_post_profile(profile)
	n = salmon_get_num_shifts(results)
	for i in reversed(range(n)):
		salmon_post_shift(i, results)