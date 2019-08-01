#!/usr/bin/env python
# -*- coding: utf-8 -*-

# eli fessler
# clovervidia
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import input
from builtins import zip
from builtins import str
from builtins import range
from past.utils import old_div
import os.path, argparse, sys
import requests, json, time, datetime, random, re
import msgpack, uuid
import iksm, dbs, salmonrun
from io import BytesIO
from operator import itemgetter
from distutils.version import StrictVersion
from subprocess import call
# PIL/Pillow imported at bottom

A_VERSION = "1.5.1"

print("splatnet2statink v{}".format(A_VERSION))

# place config.txt in same directory as script (bundled or not)
if getattr(sys, 'frozen', False):
	app_path = os.path.dirname(sys.executable)
elif __file__:
	app_path = os.path.dirname(__file__)
config_path = os.path.join(app_path, "config.txt")

try:
	config_file = open(config_path, "r")
	config_data = json.load(config_file)
	config_file.close()
except (IOError, ValueError):
	print("Generating new config file.")
	config_data = {"api_key": "", "cookie": "", "user_lang": "", "session_token": ""}
	config_file = open(config_path, "w")
	config_file.seek(0)
	config_file.write(json.dumps(config_data, indent=4, sort_keys=True, separators=(',', ': ')))
	config_file.close()
	config_file = open(config_path, "r")
	config_data = json.load(config_file)
	config_file.close()

#########################
## API KEYS AND TOKENS ##
API_KEY       = config_data["api_key"] # for stat.ink
YOUR_COOKIE   = config_data["cookie"] # iksm_session
try: # support for pre-v1.0.0 config.txts
	SESSION_TOKEN = config_data["session_token"] # to generate new cookies in the future
except:
	SESSION_TOKEN = ""
USER_LANG     = config_data["user_lang"] # only works with your game region's supported languages
#########################

debug = False # print out payload and exit. can use with geargrabber2.py & saving battle jsons

if "app_timezone_offset" in config_data:
	app_timezone_offset = str(config_data["app_timezone_offset"])
else:
	app_timezone_offset = str(int((time.mktime(time.gmtime()) - time.mktime(time.localtime()))/60))

if "app_unique_id" in config_data:
	app_unique_id = str(config_data["app_unique_id"])
else:
	app_unique_id = "32449507786579989234" # random 19-20 digit token. used for splatnet store

if "app_user_agent" in config_data:
	app_user_agent = str(config_data["app_user_agent"])
else:
	app_user_agent = 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36'

app_head = {
	'Host': 'app.splatoon2.nintendo.net',
	'x-unique-id': app_unique_id,
	'x-requested-with': 'XMLHttpRequest',
	'x-timezone-offset': app_timezone_offset,
	'User-Agent': app_user_agent,
	'Accept': '*/*',
	'Referer': 'https://app.splatoon2.nintendo.net/home',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': USER_LANG
}

translate_weapons       = dbs.weapons
translate_stages        = dbs.stages
translate_profile_color = dbs.profile_colors
translate_fest_rank     = dbs.fest_ranks
translate_headgear      = dbs.headgears
translate_clothing      = dbs.clothes
translate_shoes         = dbs.shoes
translate_ability       = dbs.abilities

def custom_key_exists(key, checkiftrue=False):
	'''Checks if a given custom key exists in config.txt and, optionally, if it is set to true.'''

	# https://github.com/frozenpandaman/splatnet2statink/wiki/custom-keys
	if key not in ["ignore_private", "app_timezone_offset", "app_unique_id", "app_user_agent"]:
		print("(!) checking unexpected custom key")
	if checkiftrue:
		return True if key in config_data and config_data[key].lower() == "true" else False
	else:
		return True if key in config_data else False

def gen_new_cookie(reason):
	'''Attempts to generate a new cookie in case the provided one is invalid.'''

	manual = False

	if reason == "blank":
		print("Blank cookie.")
	elif reason == "auth": # authentication error
		print("The stored cookie has expired.")
	else: # server error or player hasn't battled before
		print("Cannot access SplatNet 2 without having played at least one battle online.")
		sys.exit(1)
	if SESSION_TOKEN == "":
		print("session_token is blank. Please log in to your Nintendo Account to obtain your session_token.")
		new_token = iksm.log_in(A_VERSION)
		if new_token == None:
			print("There was a problem logging you in. Please try again later.")
		else:
			if new_token == "skip": # user has opted to manually enter cookie
				manual = True
				print("\nYou have opted against automatic cookie generation and must manually input your iksm_session cookie.\n")
			else:
				print("\nWrote session_token to config.txt.")
			config_data["session_token"] = new_token
			write_config(config_data)
	elif SESSION_TOKEN == "skip":
		manual = True
		print("\nYou have opted against automatic cookie generation and must manually input your iksm_session cookie. You may clear this setting by removing \"skip\" from the session_token field in config.txt.\n")

	if manual:
		new_cookie = iksm.enter_cookie()
	else:
		print("Attempting to generate new cookie...")
		acc_name, new_cookie = iksm.get_cookie(SESSION_TOKEN, USER_LANG, A_VERSION)
	config_data["cookie"] = new_cookie
	write_config(config_data)
	if manual:
		print("Wrote iksm_session cookie to config.txt.")
	else:
		print("Wrote iksm_session cookie for {} to config.txt.".format(acc_name))

def write_config(tokens):
	'''Writes config file and updates the global variables.'''

	config_file = open(config_path, "w")
	config_file.seek(0)
	config_file.write(json.dumps(tokens, indent=4, sort_keys=True, separators=(',', ': ')))
	config_file.close()

	config_file = open(config_path, "r")
	config_data = json.load(config_file)

	global API_KEY
	API_KEY = config_data["api_key"]
	global SESSION_TOKEN
	SESSION_TOKEN = config_data["session_token"]
	global YOUR_COOKIE
	YOUR_COOKIE = config_data["cookie"]
	global USER_LANG
	USER_LANG = config_data["user_lang"]

	config_file.close()

def load_json(bool):
	'''Returns results JSON from online.'''

	if bool:
		print("Pulling data from online...") # grab data from SplatNet 2
	url = "https://app.splatoon2.nintendo.net/api/results"
	results_list = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
	return json.loads(results_list.text)

def check_statink_key():
	'''Checks if a valid length API key has been provided and, if not, prompts the user to enter one.'''

	if API_KEY == "skip":
		return
	elif len(API_KEY) != 43:
		new_api_key = ""
		while len(new_api_key.strip()) != 43 and new_api_key.strip() != "skip":
			if new_api_key.strip() == "" and API_KEY.strip() == "":
				new_api_key = input("stat.ink API key: ")
			else:
				print("Invalid stat.ink API key. Please re-enter it below.")
				new_api_key = input("stat.ink API key: ")
			config_data["api_key"] = new_api_key
		write_config(config_data)
	return

def set_language():
	'''Prompts the user to set their game language.'''

	if USER_LANG == "":
		print("Default locale is en-US. Press Enter to accept, or enter your own (see readme for list).")
		language_code = input("")

		if language_code == "":
			config_data["user_lang"] = "en-US"
			write_config(config_data)
			return
		else:
			language_list = ["en-US", "es-MX", "fr-CA", "ja-JP", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT", "nl-NL", "ru-RU"]
			while language_code not in language_list:
				print("Invalid language code. Please try entering it again.")
				language_code = input("")
			config_data["user_lang"] = language_code
			write_config(config_data)
	return

def check_for_updates():
	'''Checks the version of the script against the latest version in the repo and updates dbs.py.'''

	latest_script = requests.get("https://raw.githubusercontent.com/frozenpandaman/splatnet2statink/master/splatnet2statink.py")
	new_version = re.search(r'= "([\d.]*)"', latest_script.text).group(1)
	try:
		update_available = StrictVersion(new_version) != StrictVersion(A_VERSION)
		if update_available:
			print("There is a new version (v{}) available.".format(new_version), end='')
			if os.path.isdir(".git"): # git user
				update_now = input("\nWould you like to update now? [Y/n] ")
				if update_now == "" or update_now[0].lower() == "y":
					FNULL = open(os.devnull, "w")
					call(["git", "checkout", "."], stdout=FNULL, stderr=FNULL)
					call(["git", "checkout", "master"], stdout=FNULL, stderr=FNULL)
					call(["git", "pull"], stdout=FNULL, stderr=FNULL)
					print("Successfully updated to v{}. Please restart splatnet2statink.".format(new_version))
					return True
				else:
					print("Remember to update later with \"git pull\" to get the latest version.\n")
			else: # non-git user
				print(" Visit the site below to update:\nhttps://github.com/frozenpandaman/splatnet2statink\n")
				# dbs_freshness = time.time() - os.path.getmtime("dbs.py")
				if getattr(sys, 'frozen', False): # bundled
					pass
				else:
					latest_db = requests.get("https://raw.githubusercontent.com/frozenpandaman/splatnet2statink/master/dbs.py")
					try:
						if latest_db.status_code == 200: # require proper response from github
							local_db = open("dbs.py", "w")
							local_db.write(latest_db.text)
							local_db.close()
					except: # if we can't open the file
						pass # then we don't modify the database
	except: # if there's a problem connecting to github
		pass # then we assume there's no update available

def main():
	'''I/O and setup.'''

	if check_for_updates():
		sys.exit(0)

	check_statink_key()
	set_language()

	parser = argparse.ArgumentParser()
	parser.add_argument("-M", dest="N", required=False, nargs="?", action="store",
						help="monitoring mode; pull data every N secs (default: 300)", const=300)
	parser.add_argument("-r", required=False, action="store_true",
						help="retroactively post unuploaded battles")
	parser.add_argument("-s", required=False, action="store_true",
						help="don't post scoreboard result image")
	parser.add_argument("-t", required=False, action="store_true",
						help="dry run for testing (won't post to stat.ink)")
	parser.add_argument("--salmon", required=False, action="store_true",
						help="uploads salmon run shifts")
	parser.add_argument("-i", dest="filename", required=False, help=argparse.SUPPRESS)

	parser_result = parser.parse_args()

	is_s = parser_result.s
	is_t = parser_result.t
	is_r = parser_result.r
	filename = parser_result.filename
	salmon = parser_result.salmon

	salmon_and_not_r = True if salmon and len(sys.argv) == 3 and "-r" not in sys.argv else False
	salmon_and_more = True if salmon and len(sys.argv) > 3 else False
	if salmon_and_not_r or salmon_and_more:
		print("Can only use --salmon flag alone or with -r. Exiting.")
		sys.exit(1)

	if parser_result.N != None:
		try:
			m_value = int(parser_result.N)
		except ValueError:
			print("Number provided must be an integer. Exiting.")
			sys.exit(1)
		if m_value < 0:
				print("No.")
				sys.exit(1)
		elif m_value < 60:
				print("Minimum number of seconds in monitoring mode is 60. Exiting.")
				sys.exit(1)
	else:
		m_value = -1

	return m_value, is_s, is_t, is_r, filename, salmon

def load_results(calledby=""):
	'''Returns the data we need from the results JSON, if possible.'''

	# initial checks
	try:
		if filename != None: # local file provided (users should not really be using this)
			if calledby == "monitor": # hits first
				vp = "run in monitoring mode"
			elif calledby == "populate": # -r and -M
				vp = "check for previously-unuploaded battles"
			else:
				vp = "run"
			print("Cannot {} given a local file. Exiting.".format(vp))
			sys.exit(1)
	except NameError: # some other script is probably plugging into s2s and calling load_results() directly
		pass

	data = load_json(False)
	try:
		results = data["results"] # all we care about
	except KeyError:
		if YOUR_COOKIE == "":
			reason = "blank"
		elif data["code"] == "AUTHENTICATION_ERROR":
			reason = "auth"
		else:
			reason = "other" # server error or player hasn't battled before
		gen_new_cookie(reason)
		data = load_json(False)
		try:
			results = data["results"] # try again with correct tokens; shouldn't get an error now...
		except: # ...as long as there are actually battles to fetch (i.e. has played online)
			print("Cannot access SplatNet 2 without having played at least one battle online.")
			sys.exit(1)

	return results

def populate_battles(s_flag, t_flag, r_flag, debug):
	'''Populates the battles list with SplatNet battles. Optionally uploads unuploaded battles.'''

	results = load_results("populate")

	battles = [] # 50 recent battles on splatnet

	# if r_flag, check if there are any battles in splatnet that aren't on stat.ink
	if r_flag:
		print("Checking if there are previously-unuploaded battles...")
		printed = False
		url  = 'https://stat.ink/api/v2/user-battle?only=splatnet_number&count=100'
		auth = {'Authorization': 'Bearer {}'.format(API_KEY)}
		resp = requests.get(url, headers=auth)
		try:
			statink_battles = json.loads(resp.text) # 100 recent battles on stat.ink. should avoid dupes
		except:
			print("Encountered an error while checking recently-uploaded battles. Is stat.ink down?")
			sys.exit(1)

	# always does this to populate battles array, regardless of r_flag
	for i, result in reversed(list(enumerate(results))):
		bn = int(result["battle_number"]) # get all recent battle_numbers
		battles.append(bn) # for main process, don't upload any of the ones already in the file
		if r_flag:
			if bn not in statink_battles: # one of the splatnet battles isn't on stat.ink (unuploaded)
				if not printed:
					printed = True
					print("Previously-unuploaded battles detected. Uploading now...")
				post_battle(0, [result], s_flag, t_flag, -1, True if i == 0 else False, debug, False)

	if r_flag and not printed:
		print("No previously-unuploaded battles found.")

	return battles

def monitor_battles(s_flag, t_flag, r_flag, secs, debug):
	'''Monitors JSON for changes/new battles and uploads them.'''

	results = load_results("monitor") # make sure we can do it first. if error, throw it before main process

	battles = populate_battles(s_flag, t_flag, r_flag, debug)
	wins, losses, splatfest_wins, splatfest_losses, mirror_matches = [0]*5 # init all to 0

	# main process
	mins = str(round(old_div(float(secs), 60.0), 2))
	if mins[-2:] == ".0":
		mins = mins[:-2]
	print("Waiting for new battles... (checking every {} minutes)".format(mins))

	try:
		while True:
			for i in range(secs, -1, -1):
				sys.stdout.write("Press Ctrl+C to exit. {} ".format(i))
				sys.stdout.flush()
				time.sleep(1)
				sys.stdout.write("\r")
			data = load_json(False)
			results = data["results"]
			for i, result in reversed(list(enumerate(results))): # reversed chrono order
				if int(result["battle_number"]) not in battles:
					if result["game_mode"]["key"] == "private" and custom_key_exists("ignore_private", True):
						pass
					else:
						worl = "Won" if result["my_team_result"]["key"] == "victory" else "Lost"
						splatfest_match = True if result["game_mode"]["key"] in ["fes_solo", "fes_team"] else False
						if splatfest_match: # keys will exist
							my_key = result["my_team_fes_theme"]["key"]
							their_key = result["other_team_fes_theme"]["key"]
							mirror_match = True if my_key == their_key else False
						if worl == "Won": # Win
							wins += 1
							if splatfest_match and not mirror_match:
								splatfest_wins += 1
						else: # Lose
							losses += 1
							if splatfest_match and not mirror_match:
								splatfest_losses += 1
						if splatfest_match and mirror_match:
							mirror_matches += 1
						fullname = result["stage"]["name"]
						mapname = translate_stages.get(translate_stages.get(int(result["stage"]["id"]), ""), fullname)
						print("New battle result detected at {}! ({}, {})".format(datetime.datetime.fromtimestamp(int(result["start_time"])).strftime('%I:%M:%S %p').lstrip("0"), mapname, worl))
					battles.append(int(result["battle_number"]))
					# if custom key prevents uploading, we deal with that in post_battle
					# i will be 0 if most recent battle out of those since last posting
					post_battle(0, [result], s_flag, t_flag, secs, True if i == 0 else False, debug, True)
	except KeyboardInterrupt:
		print("\nChecking to see if there are unuploaded battles before exiting...")
		data = load_json(False) # so much repeated code
		results = data["results"]
		foundany = False
		for i, result in reversed(list(enumerate(results))):
				if int(result["battle_number"]) not in battles:
					if result["game_mode"]["key"] == "private" and custom_key_exists("ignore_private", True):
						pass
					else:
						foundany = True
						worl = "Won" if result["my_team_result"]["key"] == "victory" else "Lost"
						splatfest_match = True if result["game_mode"]["key"] in ["fes_solo", "fes_team"] else False
						if splatfest_match: # keys will exist
							my_key = result["my_team_fes_theme"]["key"]
							their_key = result["other_team_fes_theme"]["key"]
							mirror_match = True if my_key == their_key else False
						if worl == "Won": # Win
							wins += 1
							if splatfest_match and not mirror_match:
								splatfest_wins += 1
						else: # Lose
							losses += 1
							if splatfest_match and not mirror_match:
								splatfest_losses += 1
						if splatfest_match and mirror_match:
							mirror_matches += 1
						fullname = result["stage"]["name"]
						mapname = translate_stages.get(translate_stages.get(int(result["stage"]["id"]), ""), fullname)
						print("New battle result detected at {}! ({}, {})".format(datetime.datetime.fromtimestamp(int(result["start_time"])).strftime('%I:%M:%S %p').lstrip("0"), mapname, worl))
					battles.append(int(result["battle_number"]))
					post_battle(0, [result], s_flag, t_flag, secs, True if i == 0 else False, debug, True)
		if foundany:
			print("Successfully uploaded remaining battles.")
		else:
			print("No remaining battles found.")
		w_plural = "" if wins == 1 else "s"
		l_plural = "" if losses == 1 else "es"
		print("%d win%s and %d loss%s this session." % (wins, w_plural, losses, l_plural))
		if splatfest_wins != 0 or splatfest_losses != 0:
			w_plural = "" if splatfest_wins == 1 else "s"
			l_plural = "" if splatfest_losses == 1 else "es"
			m_plural = "" if mirror_matches == 1 else "es"
			print("{} win{} and {} loss{} against the other Splatfest team.".format(splatfest_wins, w_plural, splatfest_losses, l_plural))
			print("{} mirror match{} against your Splatfest team.".format(mirror_matches, m_plural))
		print("Bye!")

def get_num_battles():
	'''Returns number of battles to upload along with results JSON.'''

	while True:
		if filename != None:
			if not os.path.exists(filename):
				argparse.ArgumentParser().error("File {} does not exist!".format(filename)) # exit
			with open(filename) as data_file:
				try:
					data = json.load(data_file)
				except ValueError:
					print("Could not decode JSON object in this file.")
					sys.exit(1)
		else: # no argument
			data = load_json(True)

		try:
			results = data["results"]
		except KeyError: # either auth error json (online) or battle json (local file)
			if filename != None: # local file given, so seems like battle instead of results json
				data = json.loads("{{\"results\": [{}]}}".format(json.dumps(data)))
				try:
					results = data["results"]
				except KeyError:
					print("Ill-formatted JSON file.")
					sys.exit(1)
			else:
				if YOUR_COOKIE == "":
					reason = "blank"
				elif data["code"] == "AUTHENTICATION_ERROR":
					reason = "auth"
				else:
					reason = "other"
				gen_new_cookie(reason)
				continue

		try:
			n = int(input("Number of recent battles to upload (0-50)? "))
		except ValueError:
			print("Please enter an integer between 0 and 50. Exiting.")
			sys.exit(1)
		if n < 1:
			print("Exiting without uploading anything.")
			sys.exit(0)
		elif n > 50:
			print("SplatNet 2 only stores the 50 most recent battles. Exiting.")
			sys.exit(1)
		else:
			return n, results

def set_scoreboard(payload, battle_number, mystats, s_flag, battle_payload=None):
	'''Returns a new payload with the players key (scoreboard) present.'''

	if battle_payload != None:
		battledata = battle_payload
	else:
		url = "https://app.splatoon2.nintendo.net/api/results/{}".format(battle_number)
		battle = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
		battledata = json.loads(battle.text)

	try:
		battledata["my_team_members"] # only present in battle jsons
	except KeyError:
		print("Problem retrieving battle. Continuing without scoreboard statistics.")
		return payload # same payload as passed in, no modifications

	# common definitions from the mystats payload
	mode         = mystats[0]
	rule         = mystats[1]
	result       = mystats[2]
	k_or_a       = mystats[3]
	death        = mystats[4]
	special      = mystats[5]
	weapon       = mystats[6]
	level_before = mystats[7]
	rank_before  = mystats[8]
	turfinked    = mystats[9]
	try:
		title_before = translate_fest_rank[mystats[10]]
	except:
		pass
	principal_id = mystats[11]
	star_rank    = mystats[12]
	gender       = mystats[13]
	my_species   = mystats[14]

	ally_scoreboard = []
	for n in range(len(battledata["my_team_members"])):
		ally_stats = []
		ally_stats.append(battledata["my_team_members"][n]["sort_score"]) # 0
		ally_stats.append(battledata["my_team_members"][n]["kill_count"] +
						  battledata["my_team_members"][n]["assist_count"]) # 1
		ally_stats.append(battledata["my_team_members"][n]["kill_count"]) # 2
		ally_stats.append(battledata["my_team_members"][n]["special_count"]) # 3
		ally_stats.append(battledata["my_team_members"][n]["death_count"]) # 4
		ally_stats.append("#{}".format(battledata["my_team_members"][n]["player"]["weapon"]["id"])) # 5
		ally_stats.append(battledata["my_team_members"][n]["player"]["player_rank"]) # 6
		if mode == "gachi" or mode == "league":
			try:
				ally_stats.append(battledata["my_team_members"][n]["player"]["udemae"]["name"].lower()) # 7
			except:
				ally_stats.append(None) # 7
			ally_stats.append(battledata["my_team_members"][n]["game_paint_point"]) # 8
		elif mode == "regular" or mode == "fes":
			ally_stats.append(None) # 7 - udemae (rank) is null in turf war
			if result == "victory":
				ally_stats.append(battledata["my_team_members"][n]["game_paint_point"] + 1000) # 8
			else:
				ally_stats.append(battledata["my_team_members"][n]["game_paint_point"]) # 8
		ally_stats.append(1) # 9 - my team? (yes)
		ally_stats.append(0) # 10 - is me? (no)
		if s_flag:
			ally_stats.append(None) # 11
		else:
			ally_stats.append(battledata["my_team_members"][n]["player"]["nickname"]) # 11
		if mode == "fes":
			ally_stats.append(translate_fest_rank[battledata["my_team_members"][n]["player"]["fes_grade"]["rank"]]) # 12
		else:
			ally_stats.append(None) # 12
		ally_pid = battledata["my_team_members"][n]["player"]["principal_id"]
		if s_flag:
			ally_stats.append(None) # 13
		else:
			ally_stats.append(ally_pid) # 13
		ally_stats.append(battledata["my_team_members"][n]["player"]["star_rank"]) # 14
		ally_stats.append(battledata["my_team_members"][n]["player"]["player_type"]["style"]) # 15
		ally_stats.append(battledata["my_team_members"][n]["player"]["player_type"]["species"][:-1]) # 16
		try:
			if battledata["crown_players"] != None and ally_pid in battledata["crown_players"]:
				ally_stats.append("yes") # 17
			else:
				ally_stats.append("no") # 17
		except:
			ally_stats.append("no") # 17
		ally_scoreboard.append(ally_stats)

	my_stats = []
	my_stats.append(battledata["player_result"]["sort_score"]) # 0
	my_stats.append(k_or_a) # 1
	my_stats.append(battledata["player_result"]["kill_count"]) # 2
	my_stats.append(special) # 3
	my_stats.append(death) # 4
	my_stats.append("#{}".format(weapon)) # 5
	my_stats.append(level_before) # 6
	if mode == "gachi" or mode == "league":
		my_stats.append(rank_before) # 7
		my_stats.append(turfinked) # 8
	elif mode == "regular" or mode == "fes":
		my_stats.append(None) # 7 - udemae (rank) is null in turf war
		if result == "victory":
			my_stats.append(turfinked + 1000) # 8
		else:
			my_stats.append(turfinked) # 8
	my_stats.append(1) # 9 - my team? (yes)
	my_stats.append(1) # 10 - is me? (yes)
	my_stats.append(battledata["player_result"]["player"]["nickname"]) # 11
	if mode == "fes":
		my_stats.append(title_before) # 12
	else:
		my_stats.append(None) # 12
	my_stats.append(principal_id) # 13
	my_stats.append(star_rank) # 14
	my_stats.append(gender) # 15
	my_stats.append(my_species) # 16
	try:
		if battledata["crown_players"] != None and principal_id in battledata["crown_players"]:
			my_stats.append("yes") #17
		else:
			my_stats.append("no") #17
	except:
		my_stats.append("no") # 17
	ally_scoreboard.append(my_stats)

	# scoreboard sort order: sort_score (or turf inked), k+a, specials, deaths (more = better), kills, nickname
	# discussion: https://github.com/frozenpandaman/splatnet2statink/issues/6
	if rule != "turf_war":
		sorted_ally_scoreboard = sorted(ally_scoreboard, key=itemgetter(0, 1, 3, 4, 2, 11), reverse=True)
	else:
		sorted_ally_scoreboard = sorted(ally_scoreboard, key=itemgetter(8, 1, 3, 4, 2, 11), reverse=True)

	for n in range(len(sorted_ally_scoreboard)):
		if sorted_ally_scoreboard[n][10] == 1: # if it's me, position in sorted list is my rank in team
			payload["rank_in_team"] = n + 1 # account for 0 indexing
			break

	enemy_scoreboard = []
	for n in range(len(battledata["other_team_members"])):
		enemy_stats = []
		enemy_stats.append(battledata["other_team_members"][n]["sort_score"]) # 0
		enemy_stats.append(battledata["other_team_members"][n]["kill_count"] +
						   battledata["other_team_members"][n]["assist_count"]) # 1
		enemy_stats.append(battledata["other_team_members"][n]["kill_count"]) # 2
		enemy_stats.append(battledata["other_team_members"][n]["special_count"]) # 3
		enemy_stats.append(battledata["other_team_members"][n]["death_count"]) # 4
		enemy_stats.append("#{}".format(battledata["other_team_members"][n]["player"]["weapon"]["id"])) # 5
		enemy_stats.append(battledata["other_team_members"][n]["player"]["player_rank"]) # 6
		if mode == "gachi" or mode == "league":
			try:
				enemy_stats.append(battledata["other_team_members"][n]["player"]["udemae"]["name"].lower()) # 7
			except:
				enemy_stats.append(None) # 7
			enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"]) # 8
		elif mode == "regular" or mode == "fes":
			enemy_stats.append(None) # 7 - udemae (rank) is null in turf war
			if result == "defeat":
				enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"] + 1000) # 8
			else:
				enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"]) # 8
		enemy_stats.append(0) # 9 - my team? (no)
		enemy_stats.append(0) # 10 - is me? (no)
		if s_flag:
			enemy_stats.append(None) # 11
		else:
			enemy_stats.append(battledata["other_team_members"][n]["player"]["nickname"]) # 11
		if mode == "fes":
			enemy_stats.append(translate_fest_rank[battledata["other_team_members"][n]["player"]["fes_grade"]["rank"]]) # 12
		else:
			enemy_stats.append(None) # 12
		enemy_pid = battledata["other_team_members"][n]["player"]["principal_id"]
		if s_flag:
			enemy_stats.append(None) # 13
		else:
			enemy_stats.append(enemy_pid) # 13
		enemy_stats.append(battledata["other_team_members"][n]["player"]["star_rank"]) # 14
		enemy_stats.append(battledata["other_team_members"][n]["player"]["player_type"]["style"]) # 15
		enemy_stats.append(battledata["other_team_members"][n]["player"]["player_type"]["species"][:-1]) # 16
		try:
			if battledata["crown_players"] != None and enemy_pid in battledata["crown_players"]:
				enemy_stats.append("yes") # 17
			else:
				enemy_stats.append("no") # 17
		except:
			enemy_stats.append("no") # 17
		enemy_scoreboard.append(enemy_stats)

	if rule != "turf_war":
		sorted_enemy_scoreboard = sorted(enemy_scoreboard, key=itemgetter(0, 1, 3, 4, 2, 11), reverse=True)
	else:
		sorted_enemy_scoreboard = sorted(enemy_scoreboard, key=itemgetter(8, 1, 3, 4, 2, 11), reverse=True)

	full_scoreboard = sorted_ally_scoreboard + sorted_enemy_scoreboard

	payload["players"] = []
	for n in range(len(full_scoreboard)):
		# sort score, k+a, kills, specials, deaths, weapon, level, rank, turf inked, is my team, is me, nickname, splatfest rank, splatnet principal_id, star_rank, gender, species, top_500
		detail = {
			"team":           "my" if full_scoreboard[n][9] == 1 else "his",
			"is_me":          "yes" if full_scoreboard[n][10] == 1 else "no",
			"weapon":         full_scoreboard[n][5],
			"level":          full_scoreboard[n][6],
			"rank_in_team":   n + 1 if n < 4 else n - 3, # pos 0-7 on scoreboard -> 1-4 for each
			"kill_or_assist": full_scoreboard[n][1],
			"kill":           full_scoreboard[n][2],
			"death":          full_scoreboard[n][4],
			"special":        full_scoreboard[n][3],
			"point":          full_scoreboard[n][8],
			"name":           full_scoreboard[n][11],
			"splatnet_id":    full_scoreboard[n][13],
			"star_rank":      full_scoreboard[n][14],
			"gender":         full_scoreboard[n][15],
			"species":        full_scoreboard[n][16],
		}
		try:
			detail["top_500"] = full_scoreboard[n][17]
		except:
			pass
		if mode == "gachi" or mode == "league":
			detail["rank"] = full_scoreboard[n][7]
		if mode == "fes":
			detail["fest_title"] = full_scoreboard[n][12]
		payload["players"].append(detail)

	if s_flag:
		for i in range(len(battledata["my_team_members"])):
			battledata["my_team_members"][i]["player"]["nickname"] = None
			battledata["my_team_members"][i]["player"]["principal_id"] = None
		for i in range(len(battledata["other_team_members"])):
			battledata["other_team_members"][i]["player"]["nickname"] = None
			battledata["other_team_members"][i]["player"]["principal_id"] = None

	if not debug: # we should already have our original json if we're using debug mode
		payload["splatnet_json"] = battledata

	return payload # return modified payload w/ players key

# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md
def post_battle(i, results, s_flag, t_flag, m_flag, sendgears, debug, ismonitor=False):
	'''Uploads battle #i from the provided results dictionary.'''

	#############
	## PAYLOAD ##
	#############
	payload = {'agent': 'splatnet2statink', 'agent_version': A_VERSION, 'automated': 'yes'}
	agent_variables = {'upload_mode': "Monitoring" if ismonitor else "Manual"}
	payload["agent_variables"] = agent_variables
	bn = results[i]["battle_number"]
	ver4 = True if "version" in results[i] and results[i]["version"] >= 4 else False # splatfest only
	principal_id = results[i]["player_result"]["player"]["principal_id"]
	namespace = uuid.UUID(u'{73cf052a-fd0b-11e7-a5ee-001b21a098c2}')
	name = "{}@{}".format(bn, principal_id)
	if sys.version_info[0] < 3:
		payload["uuid"] = str(uuid.uuid5(namespace, name.encode('ascii')))
	else:
		payload["uuid"] = str(uuid.uuid5(namespace, name))

	##################
	## LOBBY & MODE ##
	##################
	lobby = results[i]["game_mode"]["key"]
	if lobby == "regular": # turf war
		payload["lobby"] = "standard"
		payload["mode"]  = "regular"
	elif lobby == "gachi": # ranked solo
		payload["lobby"] = "standard"
		payload["mode"]  = "gachi"
	elif lobby == "league_pair": # league pair
		payload["lobby"] = "squad_2"
		payload["mode"]  = "gachi"
	elif lobby == "league_team": # league team
		payload["lobby"] = "squad_4"
		payload["mode"]  = "gachi"
	elif lobby == "private": # private battle
		payload["lobby"] = "private"
		payload["mode"]  = "private"
	elif lobby == "fes_solo": # splatfest pro / solo
		payload["lobby"] = "fest_pro" if ver4 else "standard"
		payload["mode"]  = "fest"
		# ["fes_mode"]["key"] == "fes.result.challenge"
	elif lobby == "fes_team": # splatfest normal / team
		payload["lobby"] = "fest_normal" if ver4 else "squad_4"
		payload["mode"]  = "fest"
		# ["fes_mode"]["key"] == "fes.result.regular"

	##########
	## RULE ##
	##########
	rule = results[i]["rule"]["key"]
	if rule == "turf_war":
		payload["rule"] = "nawabari"
	elif rule == "splat_zones":
		payload["rule"] = "area"
	elif rule == "tower_control":
		payload["rule"] = "yagura"
	elif rule == "rainmaker":
		payload["rule"] = "hoko"
	elif rule == "clam_blitz":
		payload["rule"] = "asari"

	###########
	## STAGE ##
	###########
	stage = int(results[i]["stage"]["id"])
	payload["stage"] = "#{}".format(stage)

	############
	## WEAPON ##
	############
	weapon = int(results[i]["player_result"]["player"]["weapon"]["id"])
	payload["weapon"] = "#{}".format(weapon)

	############
	## RESULT ##
	############
	result = results[i]["my_team_result"]["key"] # victory, defeat
	if result == "victory":
		payload["result"] = "win"
	elif result == "defeat":
		payload["result"] = "lose"

	##########################
	## TEAM PERCENTS/COUNTS ##
	##########################
	try:
		my_percent    = results[i]["my_team_percentage"]
		their_percent = results[i]["other_team_percentage"]
	except KeyError:
		pass # don't need to handle - won't be put into the payload unless relevant

	try:
		my_count    = results[i]["my_team_count"]
		their_count = results[i]["other_team_count"]
	except:
		pass

	mode = results[i]["type"] # regular, gachi, league, fes
	if mode == "regular" or mode == "fes":
		payload["my_team_percent"]  = my_percent
		payload["his_team_percent"] = their_percent
	elif mode == "gachi" or mode == "league":
		payload["my_team_count"]  = my_count
		payload["his_team_count"] = their_count
		if my_count == 100 or their_count == 100:
			payload["knock_out"] = "yes"
		else:
			payload["knock_out"] = "no"

	################
	## TURF INKED ##
	################
	turfinked = results[i]["player_result"]["game_paint_point"] # without bonus
	if rule == "turf_war":
		if result == "victory":
			payload["my_point"] = turfinked + 1000 # win bonus
		else:
			payload["my_point"] = turfinked
	else:
		payload["my_point"] = turfinked

	#################
	## KILLS, ETC. ##
	#################
	kill    = results[i]["player_result"]["kill_count"]
	k_or_a  = results[i]["player_result"]["kill_count"] + results[i]["player_result"]["assist_count"]
	special = results[i]["player_result"]["special_count"]
	death   = results[i]["player_result"]["death_count"]
	payload["kill"]           = kill
	payload["kill_or_assist"] = k_or_a
	payload["special"]        = special
	payload["death"]          = death

	###########
	## LEVEL ##
	###########
	level_before = results[i]["player_result"]["player"]["player_rank"]
	level_after  = results[i]["player_rank"]
	star_rank    = results[i]["star_rank"]
	payload["level"]       = level_before
	payload["level_after"] = level_after
	payload["star_rank"]   = star_rank

	##########
	## RANK ##
	##########
	try: # udemae not present in all modes
		rank_after     = results[i]["udemae"]["name"].lower() # non-null after playing first solo battle
		rank_before    = results[i]["player_result"]["player"]["udemae"]["name"].lower()
		rank_exp_after = results[i]["udemae"]["s_plus_number"]
		rank_exp       = results[i]["player_result"]["player"]["udemae"]["s_plus_number"]
	except: # based on in-game, not app scoreboard, which displays --- (null rank) as separate than C-
		rank_after, rank_before, rank_exp_after, rank_exp = None, None, None, None
		# e.g. private battle where a player has never played ranked before
	if rule != "turf_war": # only upload if ranked
		payload["rank_after"]     = rank_after
		payload["rank"]           = rank_before
		payload["rank_exp_after"] = rank_exp_after
		payload["rank_exp"]       = rank_exp

	try:
		if results[i]["udemae"]["is_x"]: # == true. results[i]["udemae"]["number"] should be 128
			payload["x_power_after"] = results[i]["x_power"] # can be null if not played placement games
			if mode == "gachi":
				payload["estimate_x_power"] = results[i]["estimate_x_power"] # team power, approx
			payload["worldwide_rank"] = results[i]["rank"] # goes below 500, not sure how low (doesn't exist in league)
		# top_500 from crown_players set in scoreboard method
	except:
		pass

	#####################
	## START/END TIMES ##
	#####################
	try:
		elapsed_time = results[i]["elapsed_time"] # apparently only a thing in ranked
	except KeyError:
		elapsed_time = 180 # turf war - 3 minutes in seconds
	payload["start_at"] = results[i]["start_time"]
	payload["end_at"]   = results[i]["start_time"] + elapsed_time

	###################
	## SPLATNET DATA ##
	###################
	payload["private_note"] = "Battle #{}".format(bn)
	payload["splatnet_number"] = bn
	if mode == "league":
		payload["my_team_id"] = results[i]["tag_id"]
		payload["league_point"] = results[i]["league_point"]
		payload["my_team_estimate_league_point"] = results[i]["my_estimate_league_point"]
		payload["his_team_estimate_league_point"] = results[i]["other_estimate_league_point"]
	if mode == "gachi":
		payload["estimate_gachi_power"] = results[i]["estimate_gachi_power"]
	gender = results[i]["player_result"]["player"]["player_type"]["style"]
	payload["gender"] = gender
	species = results[i]["player_result"]["player"]["player_type"]["species"][:-1]
	payload["species"] = species

	############################
	## SPLATFEST TITLES/POWER ##
	############################ https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md#fest_title-fest_title_after
	if mode == "fes":
		title_before   = results[i]["player_result"]["player"]["fes_grade"]["rank"]
		title_after    = results[i]["fes_grade"]["rank"]
		fest_exp_after = results[i]["fes_point"]

		# present in pro, 0 in normal
		payload["fest_power"] = results[i]["fes_power"]
		# universal system pre-ver.4. now present in both pro & normal but hidden in normal
		payload["my_team_estimate_fest_power"]  = results[i]["my_estimate_fes_power"]
		payload["his_team_estimate_fest_power"] = results[i]["other_estimate_fes_power"]

		payload["my_team_fest_theme"]  = results[i]["my_team_fes_theme"]["name"]
		payload["his_team_fest_theme"] = results[i]["other_team_fes_theme"]["name"]
		payload["fest_title"]          = translate_fest_rank[title_before]
		payload["fest_title_after"]    = translate_fest_rank[title_after]
		payload["fest_exp_after"]      = fest_exp_after
		points_gained = 0

		if ver4: # in ver.4, everything got multiplied x10...
			multiplier = 10
		else:
			multiplier = 1

		# TURF INKED EXP
		if results[i]["player_result"]["game_paint_point"] >= 200:
			points_gained += 1 * multiplier
		if results[i]["player_result"]["game_paint_point"] >= 400:
			points_gained += 1 * multiplier # +20 total (post-ver.4)

		# WIN BONUS EXP
		if result == "victory":
			# https://github.com/frozenpandaman/splatnet2statink/issues/52#issuecomment-414609225
			if results[i]["other_estimate_fes_power"] < 1400:
				points_gained += 3 * multiplier
			elif 1400 <= results[i]["other_estimate_fes_power"] < 1700:
				points_gained += 4 * multiplier
			elif 1700 <= results[i]["other_estimate_fes_power"] < 1800:
				points_gained += 5 * multiplier
			elif 1800 <= results[i]["other_estimate_fes_power"] < 1900:
				points_gained += 6 * multiplier
			elif results[i]["other_estimate_fes_power"] >= 1900:
				points_gained += 7 * multiplier

		if ver4:
			synergy_mult = results[i]["uniform_bonus"]
			if synergy_mult > 1:
				points_gained = round(points_gained * synergy_mult)

		# SPECIAL CASE - KING/QUEEN MAX
		if title_before == 4 and title_after == 4 and fest_exp_after == 0:
			payload["fest_exp"] = 0 # already at max, no exp gained

		# SPECIAL CASE - CHAMPION (999) TO KING/QUEEN
		elif title_before == 3 and title_after == 4:
			# fes_point == 0 should always be true (reached max). if reaching max *exactly*,
			# then fest_exp = 999 - points_gained. if curtailed rollover, no way to know
			# e.g. even if user got +70, max (999->0) could have been reached after, say, +20
			payload["fest_exp"] = None

		else:
			if title_before == title_after: # within same title
				fest_rank_rollover = 0
			elif title_before == 0 and title_after == 1: # fanboy/girl (100) to fiend (250)
				fest_rank_rollover = 10 * multiplier
			elif title_before == 1 and title_after == 2: # fiend (250) to defender (500)
				fest_rank_rollover = 25 * multiplier
			elif title_before == 2 and title_after == 3: # defender (500) to champion (999)
				fest_rank_rollover = 50 * multiplier
			payload["fest_exp"] = fest_rank_rollover + fest_exp_after - points_gained

		# avoid mysterious, fatal -1 case...
		if payload["fest_exp"] and payload["fest_exp"] < 0:
			payload["fest_exp"] = 0

	else: # not splatfest
		title_before = None # required to set for scoreboard param

	#####################
	## SPLATFEST VER.4 ##
	#####################
	if ver4 and mode == "fes":
		# indiv. & team fest_powers in above section
		payload["my_team_win_streak"]  = results[i]["my_team_consecutive_win"]
		payload["his_team_win_streak"] = results[i]["other_team_consecutive_win"]

		if results[i]["event_type"]["key"] == "10_x_match":
			payload["special_battle"] = "10x"
		elif results[i]["event_type"]["key"] == "100_x_match":
			payload["special_battle"] = "100x"

		total_clout_after = results[i]["contribution_point_total"] # after
		payload["total_clout_after"] = total_clout_after

		if lobby == "fes_team": # normal
			try:
				payload["my_team_nickname"] = results[i]["my_team_another_name"]
			except:
				pass
			try:
				payload["his_team_nickname"] = results[i]["other_team_another_name"]
			except:
				pass

		# synergy bonus
		if synergy_mult == 0: # always 0 in pro
			synergy_mult = 1.0
		payload["synergy_bonus"] = synergy_mult # max 2.0

		# clout
		clout = results[i]["contribution_point"]
		# in pro, = his_team_estimate_fest_power
		# in normal, = turfinked (if victory: +1000) -> = int(round(floor((clout * synergy_bonus) + 0.5)))
		payload["clout"] = clout
		payload["total_clout"] = total_clout_after - clout # before

	################
	## SCOREBOARD ##
	################
	if YOUR_COOKIE != "" or debug: # requires online (or battle json). if no cookie, don't do - will fail
		mystats = [mode, rule, result, k_or_a, death, special, weapon, level_before, rank_before, turfinked, title_before, principal_id, star_rank, gender, species]
		if filename == None:
			payload = set_scoreboard(payload, bn, mystats, s_flag)
		else:
			payload = set_scoreboard(payload, bn, mystats, s_flag, results[0])

	##################
	## IMAGE RESULT ##
	##################
	if not debug:
		url = "https://app.splatoon2.nintendo.net/api/share/results/{}".format(bn)
		share_result = requests.post(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
		if share_result.ok:
			image_result_url = share_result.json().get("url")
			if image_result_url:
				image_result = requests.get(image_result_url, stream=True)
				if image_result.ok:
					if not s_flag: # normal scoreboard
						payload["image_result"] = BytesIO(image_result.content).getvalue()
					else:
						players = [0] * 8 # in case battles are < 8 people. mark missing player-positions
						my_missing = 4 - (len(payload["splatnet_json"]["my_team_members"]) + 1)
						their_missing = 4 - len(payload["splatnet_json"]["other_team_members"])
						for u, v in zip(list(range(4)), list(range(3, -1, -1))):
							if my_missing >= u+1: # 1, 2, 3, 4
								players[v] = None # from back of my team's half
						for u, v in zip(list(range(4)), list(range(7, -3, -1))):
							if their_missing >= u+1:
								players[v] = None
						for p in range(len(payload["players"])):
							# by default, covers all non-me names.
							# could be modified, e.g. in quad squads only cover enemy names
							try:
								is_player_me = payload["players"][p]["is_me"]
							except:
								is_player_me = None
							lowest_zero = players.index(0) # fill in 0s (uninits) with values
							players[lowest_zero] = is_player_me
						if result == "defeat": # enemy team is on top
							players = players[4:] + players[:4]
						scoreboard = blackout(image_result.content, players)
						bytes_result = BytesIO()
						scoreboard.save(bytes_result, "PNG")
						payload["image_result"] = bytes_result.getvalue()
		if sendgears: # if most recent
			url_profile = "https://app.splatoon2.nintendo.net/api/share/profile"
			if stage >= 100: # fav_stage can't be Shifty Station(s)
				stages_ints = [k for k in translate_stages.keys() if isinstance(k, int) and k < 100]
				fav_stage = random.choice(stages_ints)
			else:
				fav_stage = stage
			settings = {'stage': fav_stage, 'color': translate_profile_color[random.randrange(0, 6)]}
			share_result = requests.post(url_profile, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE), data=settings)
			if share_result.ok:
				profile_result_url = share_result.json().get("url")
				if profile_result_url:
					profile_result = requests.get(profile_result_url, stream=True)
					if profile_result.ok:
						payload["image_gear"] = BytesIO(profile_result.content).getvalue()

	##########
	## GEAR ##
	########## https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md#gears-structure
	headgear_id = results[i]["player_result"]["player"]["head"]["id"]
	clothing_id = results[i]["player_result"]["player"]["clothes"]["id"]
	shoes_id    = results[i]["player_result"]["player"]["shoes"]["id"]
	payload["gears"] = {'headgear': {'secondary_abilities': []}, 'clothing': {'secondary_abilities': []}, 'shoes': {'secondary_abilities': []}}
	payload["gears"]["headgear"]["gear"] = "#{}".format(headgear_id)
	payload["gears"]["clothing"]["gear"] = "#{}".format(clothing_id)
	payload["gears"]["shoes"]["gear"]    = "#{}".format(shoes_id)

	###############
	## ABILITIES ##
	############### https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/ability.md
	headgear_subs, clothing_subs, shoes_subs = ([-1,-1,-1] for i in range(3))
	for j in range(3):
		try:
			headgear_subs[j] = results[i]["player_result"]["player"]["head_skills"]["subs"][j]["id"]
		except:
			headgear_subs[j] = '-1'
		try:
			clothing_subs[j] = results[i]["player_result"]["player"]["clothes_skills"]["subs"][j]["id"]
		except:
			clothing_subs[j] = '-1'
		try:
			shoes_subs[j] = results[i]["player_result"]["player"]["shoes_skills"]["subs"][j]["id"]
		except:
			shoes_subs[j] = '-1'
	headgear_main = results[i]["player_result"]["player"]["head_skills"]["main"]["id"]
	clothing_main = results[i]["player_result"]["player"]["clothes_skills"]["main"]["id"]
	shoes_main = results[i]["player_result"]["player"]["shoes_skills"]["main"]["id"]
	payload["gears"]["headgear"]["primary_ability"] = translate_ability.get(int(headgear_main), "")
	payload["gears"]["clothing"]["primary_ability"] = translate_ability.get(int(clothing_main), "")
	payload["gears"]["shoes"]["primary_ability"]    = translate_ability.get(int(shoes_main), "")
	for j in range(3):
		payload["gears"]["headgear"]["secondary_abilities"].append(translate_ability.get(int(headgear_subs[j]), ""))
		payload["gears"]["clothing"]["secondary_abilities"].append(translate_ability.get(int(clothing_subs[j]), ""))
		payload["gears"]["shoes"]["secondary_abilities"].append(translate_ability.get(int(shoes_subs[j]), ""))

	#############
	## DRY RUN ##
	#############
	if t_flag: # -t provided
		payload["test"] = "dry_run" # works the same as 'validate' for now

	#**************
	#*** OUTPUT ***
	#**************
	if debug:
		print("")
		print(json.dumps(payload).replace("'", "\'"))
	# adding support for a custom key? add to custom_key_exists() method, and
	# to "main process" section of monitor_battles, too. and the docs/wiki page of course
	elif lobby == "private" and custom_key_exists("ignore_private", True):
		if m_flag != -1: # monitoring mode
			pass
		else:
			print("Battle #{}: skipping upload based on ignore_private key.".format(i+1))
	else:
		# POST to stat.ink
		# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/request-body.md
		url  = 'https://stat.ink/api/v2/battle'
		auth = {'Authorization': 'Bearer {}'.format(API_KEY), 'Content-Type': 'application/x-msgpack'}

		if payload["agent"] != os.path.basename(__file__)[:-3]:
			print("Could not upload. Please contact @frozenpandaman on Twitter/GitHub for assistance.")
			sys.exit(1)
		postbattle = requests.post(url, headers=auth, data=msgpack.packb(payload), allow_redirects=False)

		# Response
		headerloc = postbattle.headers.get('location')
		if headerloc != None:
			if postbattle.status_code == 302: # receive redirect
				print("Battle #{} already uploaded to {}".format(i+1, headerloc))
				# continue trying to upload remaining
			else: # http status code should be OK (200)
				if not ismonitor and len(results) > 1:
					print("Battle #{} uploaded to {}".format(i+1, headerloc))
				else: # monitoring mode
					print("Battle uploaded to {}".format(headerloc))
		else: # error of some sort
			if t_flag:
				print("Battle #{} - message from server:".format(i+1))
			else:
				if not ismonitor and len(results) > 1:
					print("Error uploading battle #{}. Message from server:".format(i+1))
				else: # monitoring mode
					print("Error uploading battle. Message from server:")
			print(postbattle.content.decode("utf-8"))
			if not t_flag and i != 0: # don't prompt for final battle
				cont = input('Continue? [Y/n] ')
				if cont[0].lower() == "n":
					print("Exiting.")
					sys.exit(1)

def blackout(image_result_content, players):
	'''Given a scoreboard image as bytes and players array, returns the blacked-out scoreboard.'''

	scoreboard = Image.open(BytesIO(image_result_content)).convert("RGB")
	draw = ImageDraw.Draw(scoreboard)

	if "yes" in players:
		if players[0] == "no": # is_me is no, so censor
			draw.polygon([(719, 101), (719, 123), (849, 119), (849,  97)], fill="black")
		if players[1] == "no":
			draw.polygon([(721, 151), (721, 173), (851, 169), (851, 147)], fill="black")
		if players[2] == "no":
			draw.polygon([(723, 201), (723, 223), (853, 219), (853, 197)], fill="black")
		if players[3] == "no":
			draw.polygon([(725, 251), (725, 273), (855, 269), (855, 247)], fill="black")
		if players[4] == "no":
			draw.polygon([(725, 379), (725, 401), (855, 406), (855, 384)], fill="black")
		if players[5] == "no":
			draw.polygon([(723, 429), (723, 451), (853, 456), (853, 434)], fill="black")
		if players[6] == "no":
			draw.polygon([(721, 479), (721, 501), (851, 506), (851, 484)], fill="black")
		if players[7] == "no":
			draw.polygon([(719, 529), (719, 551), (849, 556), (849, 534)], fill="black")
	else: # no "me" - this shouldn't happen. if it does, let's just not censor anything in case
		pass
	return scoreboard

if __name__ == "__main__":
	m_value, is_s, is_t, is_r, filename, salmon = main()
	if salmon: # salmon run mode
		salmonrun.upload_salmon_run(A_VERSION, YOUR_COOKIE, API_KEY, app_head, is_r)
	else: # normal mode
		if is_s:
			from PIL import Image, ImageDraw
		if m_value != -1: # m flag exists
			monitor_battles(is_s, is_t, is_r, m_value, debug)
		elif is_r: # r flag exists without m, so run only the recent battle upload
			populate_battles(is_s, is_t, is_r, debug)
		else:
			n, results = get_num_battles()
			for i in reversed(range(n)):
				post_battle(i, results, is_s, is_t, m_value, True if i == 0 else False, debug)
			if debug:
				print("")
