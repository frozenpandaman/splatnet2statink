#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
splatnet2statink.py
Takes battle data from the SplatNet 2 app and uploads it to stat.ink.

Copyright (C) 2017 eli fessler
Copyright (C) 2017 clovervidia
Copyright (C) 2017 RoyXiang
Copyright (C) 2017 mkody
Copyright (C) 2017 Tiryoh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os.path, argparse, sys
import requests, json, time, datetime, random, re
import msgpack
import iksm, dbs
from io import BytesIO
from operator import itemgetter

A_VERSION = "0.0.42"

print "splatnet2statink v" + A_VERSION

try:
	config_file = open("config.txt", "r")
	config_data = json.load(config_file)
	config_file.close()
except:
	print "Could not read config.txt. Generating new config file."
	config_data = {"api_key": "", "cookie": "", "session_token": "", "user_lang": ""}
	config_file = open("config.txt", "w")
	config_file.seek(0)
	config_file.write(json.dumps(config_data, indent=4, sort_keys=True, separators=(',', ': ')))
	config_file.close()
	config_file = open("config.txt", "r")
	config_data = json.load(config_file)
	config_file.close()

#########################
## API KEYS AND TOKENS ##
API_KEY       = config_data["api_key"] # for stat.ink
YOUR_COOKIE   = config_data["cookie"] # iksm_session
SESSION_TOKEN = config_data["session_token"] # to generate new cookies in the future
USER_LANG     = config_data["user_lang"] # only works with your game region's supported languages
#########################

debug = False

app_head = {
	'Host': 'app.splatoon2.nintendo.net',
	'x-unique-id': '32449507786579989234', # random 19-20 digit token. used for splatnet store
	'x-requested-with': 'XMLHttpRequest',
	'x-timezone-offset': '0',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
	'Accept': '*/*',
	'Referer': 'https://app.splatoon2.nintendo.net/home',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': USER_LANG
}

translate_weapons = dbs.weapons
translate_stages = dbs.stages
# translate_headgear = dbs.headgears
# translate_clothing = dbs.clothes
# translate_shoes = dbs.shoes
# translate_ability = dbs.abilities
translate_profile_color = dbs.profile_colors
translate_fest_rank = dbs.fest_ranks

def gen_new_cookie(reason):
	'''Attempts to generate new cookie in case provided one is invalid.'''

	if reason == "blank":
		print "Blank cookie. Trying to generate one given your session_token..."
	elif reason == "auth": # authentication error
		print "Bad cookie. Trying to generate a new one given your session_token..."
	else: # server error or player hasn't battled before
		print "Cannot access SplatNet 2 without having played at least one battle online."
		exit(1)
	if SESSION_TOKEN == "":
		print "session_token is blank. Please log in to your Nintendo Account to obtain your session_token."
		new_token = iksm.log_in()
		if new_token == None:
			print "There was a problem logging you in. Please try again later."
		else:
			config_data["session_token"] = new_token
			write_config(config_data)
			print "\nWrote session_token to config.txt."

		new_cookie = iksm.get_cookie(SESSION_TOKEN, USER_LANG) # error handling in get_cookie()
		config_data["cookie"] = new_cookie
		write_config(config_data)
		print "Wrote iksm_session cookie to config.txt.\nYour cookie: " + new_cookie

def write_config(tokens):
	'''Writes config file and updates the global variables.'''

	config_file = open("config.txt", "w")
	config_file.seek(0)
	config_file.write(json.dumps(tokens, indent=4, sort_keys=True, separators=(',', ': ')))
	config_file.close()

	config_file = open("config.txt", "r")
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
		print "Pulling data from online..." # grab data from SplatNet 2
	url = "https://app.splatoon2.nintendo.net/api/results"
	r = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
	return json.loads(r.text)

def check_statink_key():
	'''Check if a valid length API key has been provided and, if not, prompts the user to enter one.'''

	if len(API_KEY) != 43:
		new_api_key = ""
		while len(new_api_key.strip()) != 43:
			if new_api_key.strip() == "" and API_KEY.strip() == "":
				new_api_key = raw_input("stat.ink API key: ")
			else:
				print "Invalid stat.ink API key. Please re-enter it below."
				new_api_key = raw_input("stat.ink API key: ")
			config_data["api_key"] = new_api_key
		write_config(config_data)
	return

def set_language():
	'''Prompts the user to set their game language.'''

	if USER_LANG == "":
		print "Default game language is en-US. Press Enter to accept, or type in a language code.\nSee readme for language codes."
		language_code = raw_input("")

		if language_code == "":
			config_data["user_lang"] = "en-US"
			write_config(config_data)
			return
		else:
			while re.findall("^[a-z]{2}", language_code) == []:
				print "Invalid language code. Please try entering it again."
				language_code = raw_input("")
			config_data["user_lang"] = language_code
			write_config(config_data)

	return

def main():
	'''I/O and setup.'''

	check_statink_key()

	set_language()

	parser = argparse.ArgumentParser()
	parser.add_argument("-M", required=False, action="store_true",
						help="run in realtime monitoring mode")
	parser.add_argument("-s", required=False, action="store_true",
						help="don't upload scoreboard result image")
	parser.add_argument("-i", dest="filename", required=False,
						help="results JSON file", metavar="file.json")
	parser.add_argument("-t", required=False, action="store_true",
						help="dry run for testing (won't upload to stat.ink)")
	parser_result = parser.parse_args()

	is_m = parser_result.M
	is_s = parser_result.s
	is_t = parser_result.t
	filename = parser_result.filename;
	return is_m, is_s, is_t, filename;

def monitor_battles(s_flag, t_flag, debug):
	'''Monitor JSON for changes/new battles and upload them.'''

	if filename != None: # local file provided
		print "Cannot run in monitoring mode provided a local file. Exiting."
		exit(1)

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
			print "Cannot access SplatNet 2 without having played at least one battle online."
			exit(1)

	# don't upload any of the ones already in the file
	battles = []
	for result in results:
		battles.append(int(result["battle_number"]))

	secs = 90
	print "Waiting for new battles... (checking every 1.5 minutes)" # allow this to be customized?

	try:
		while True:
			for i in range(secs, -1, -1):
				sys.stdout.write("Press Ctrl+C to exit. " + str(i) + "  ")
				sys.stdout.flush()
				time.sleep(1)
				sys.stdout.write("\r")
			data = load_json(False)
			results = data["results"]
			for result in results[::-1]: # reversed chrono order
				if int(result["battle_number"]) not in battles:
					print "New battle result detected at %s!" % datetime.datetime.fromtimestamp(int(result["start_time"])).strftime('%I:%M:%S %p').lstrip("0")
					battles.append(int(result["battle_number"]))
					post_battle(0, [result], s_flag, t_flag, is_m, debug)
	except KeyboardInterrupt:
		print "\nBye!"

def get_num_battles():
	'''Returns number of battles to upload along with results json.'''

	while True:
		if filename != None:
			if not os.path.exists(filename):
				argparse.ArgumentParser().error("File %s does not exist!" % filename) # exit
			with open(filename) as data_file:
				data = json.load(data_file)
		else: # no argument
			data = load_json(True)

		try:
			results = data["results"]
		except KeyError:
			if YOUR_COOKIE == "":
				reason = "blank"
			elif data["code"] == "AUTHENTICATION_ERROR":
				reason = "auth"
			else:
				reason = "other"
			gen_new_cookie(reason)
			continue

		try:
			n = int(raw_input("Number of recent battles to upload (0-50)? "))
		except ValueError:
			print "Please enter an integer between 0 and 50."
			exit(0)
		if n < 1:
			print "Exiting without uploading anything."
			exit(0)
		elif n > 50:
			print "SplatNet 2 only stores the 50 most recent battles. Exiting."
			exit(0)
		else:
			return n, results;

def set_scoreboard(payload, battle_number, mystats):
	'''Returns a new payload with the players key (scoreboard) present.'''

	url = "https://app.splatoon2.nintendo.net/api/results/" + battle_number
	battle = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
	battledata = json.loads(battle.text)

	try:
		battledata["battle_number"]
	except KeyError:
		print "Problem retrieving battle. Continuing without scoreboard statistics."
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

	ally_scoreboard = []
	for n in xrange(len(battledata["my_team_members"])):
		ally_stats = []
		ally_stats.append(battledata["my_team_members"][n]["sort_score"])
		ally_stats.append(battledata["my_team_members"][n]["kill_count"] +
						  battledata["my_team_members"][n]["assist_count"])
		ally_stats.append(battledata["my_team_members"][n]["kill_count"])
		ally_stats.append(battledata["my_team_members"][n]["special_count"])
		ally_stats.append(battledata["my_team_members"][n]["death_count"])
		ally_stats.append(translate_weapons[int(battledata["my_team_members"][n]["player"]["weapon"]["id"])])
		ally_stats.append(battledata["my_team_members"][n]["player"]["player_rank"])
		if mode == "gachi" or mode == "league":
			try:
				ally_stats.append(battledata["my_team_members"][n]["player"]["udemae"]["name"].lower())
			except:
				ally_stats.append("c-")
			ally_stats.append(None) # points of turf inked is null in ranked/league battle
		elif mode == "regular" or mode == "fes":
			ally_stats.append(None) # udemae (rank) is null in turf war
			if result == "victory":
				ally_stats.append(battledata["my_team_members"][n]["game_paint_point"] + 1000)
			else:
				ally_stats.append(battledata["my_team_members"][n]["game_paint_point"])
		ally_stats.append(1) # my team? (yes)
		ally_stats.append(0) # is me? (no)
		ally_stats.append(battledata["my_team_members"][n]["player"]["nickname"])
		if mode == "fes":
			ally_stats.append(translate_fest_rank[battledata["my_team_members"][n]["player"]["fes_grade"]["rank"]])
		else:
			ally_stats.append(None)
		ally_stats.append(battledata["my_team_members"][n]["player"]["principal_id"])
		ally_scoreboard.append(ally_stats)

	my_stats = []
	my_stats.append(battledata["player_result"]["sort_score"])
	my_stats.append(k_or_a)
	my_stats.append(battledata["player_result"]["kill_count"])
	my_stats.append(special)
	my_stats.append(death)
	my_stats.append(translate_weapons[int(weapon)])
	my_stats.append(level_before)
	if mode == "gachi" or mode == "league":
		my_stats.append(rank_before)
		my_stats.append(None) # points of turf inked is null if ranked/league battle
	elif mode == "regular" or mode == "fes":
		my_stats.append(None) # udemae (rank) is null if turf war
		if result == "victory":
			my_stats.append(turfinked + 1000)
		else:
			my_stats.append(turfinked)
	my_stats.append(1) # my team? (yes)
	my_stats.append(1) # is me? (yes)
	my_stats.append(battledata["player_result"]["player"]["nickname"])
	if mode == "fes":
		my_stats.append(title_before)
	else:
		my_stats.append(None)
	my_stats.append(principal_id)
	ally_scoreboard.append(my_stats)

	# scoreboard sorted by sort_score, then k+a, then k, then s, then d (more = better), then name
	# discussion: https://github.com/frozenpandaman/splatnet2statink/issues/6
	if rule != "turf_war":
		sorted_ally_scoreboard = sorted(ally_scoreboard, key=itemgetter(0, 1, 2, 3, 4, 11), reverse=True)
	else:
		sorted_ally_scoreboard = sorted(ally_scoreboard, key=itemgetter(8, 1, 2, 3, 4, 11), reverse=True)

	for n in xrange(len(sorted_ally_scoreboard)):
		if sorted_ally_scoreboard[n][10] == 1: # if it's me, position in sorted list is my rank in team
			payload["rank_in_team"] = n + 1 # account for 0 indexing
			break

	enemy_scoreboard = []
	for n in xrange(len(battledata["other_team_members"])):
		enemy_stats = []
		enemy_stats.append(battledata["other_team_members"][n]["sort_score"])
		enemy_stats.append(battledata["other_team_members"][n]["kill_count"] +
						   battledata["other_team_members"][n]["assist_count"])
		enemy_stats.append(battledata["other_team_members"][n]["kill_count"])
		enemy_stats.append(battledata["other_team_members"][n]["special_count"])
		enemy_stats.append(battledata["other_team_members"][n]["death_count"])
		enemy_stats.append(translate_weapons[int(battledata["other_team_members"][n]["player"]["weapon"]["id"])])
		enemy_stats.append(battledata["other_team_members"][n]["player"]["player_rank"])
		if mode == "gachi" or mode == "league":
			try:
				enemy_stats.append(battledata["other_team_members"][n]["player"]["udemae"]["name"].lower())
			except:
				enemy_stats.append("c-")
			enemy_stats.append(None) # points of turf inked is null in league
		elif mode == "regular" or mode == "fes":
			enemy_stats.append(None)
			if result == "defeat":
				enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"] + 1000)
			else:
				enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"])
		enemy_stats.append(0) # my team? (no)
		enemy_stats.append(0) # is me? (no)
		enemy_stats.append(battledata["other_team_members"][n]["player"]["nickname"])
		if mode == "fes":
			enemy_stats.append(translate_fest_rank[battledata["other_team_members"][n]["player"]["fes_grade"]["rank"]])
		else:
			enemy_stats.append(None)
		enemy_stats.append(battledata["other_team_members"][n]["player"]["principal_id"])
		enemy_scoreboard.append(enemy_stats)

	if rule != "turf_war":
		sorted_enemy_scoreboard = sorted(enemy_scoreboard, key=itemgetter(0, 1, 2, 3, 4, 11), reverse=True)
	else:
		sorted_enemy_scoreboard = sorted(enemy_scoreboard, key=itemgetter(8, 1, 2, 3, 4, 11), reverse=True)

	full_scoreboard = sorted_ally_scoreboard + sorted_enemy_scoreboard

	payload["players"] = []
	for n in xrange(len(full_scoreboard)):
		# sort score, k/a, kills, specials, deaths, weapon, level, rank, turf inked, is my team, is me, nickname, splatfest rank, splatnet principal_id
		detail = {
			"team":           "my" if full_scoreboard[n][9] == 1 else "his",
			"is_me":          "yes" if full_scoreboard[n][10] == 1 else "no",
			"weapon":         full_scoreboard[n][5],
			"level":          full_scoreboard[n][6],
			"rank_in_team":   n + 1 if n < 4 else n - 3,
			"kill_or_assist": full_scoreboard[n][1],
			"kill":           full_scoreboard[n][2],
			"death":          full_scoreboard[n][4],
			"special":        full_scoreboard[n][3],
			"point":          full_scoreboard[n][8],
			"name":           full_scoreboard[n][11],
			"splatnet_id":    full_scoreboard[n][13]
		}
		if mode == "gachi" or mode == "league":
			detail["rank"] = full_scoreboard[n][7]
		if mode == "fes":
			detail["fest_title"] = full_scoreboard[n][12]
		payload["players"].append(detail)

	return payload # return new payload w/ players key

# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md
def post_battle(i, results, s_flag, t_flag, m_flag, debug):
	'''Uploads battle #i from the provided dictionary.'''

	#############
	## PAYLOAD ##
	#############
	payload = {'agent': 'splatnet2statink', 'agent_version': A_VERSION}

	##################
	## LOBBY & MODE ##
	##################
	lobby = results[i]["game_mode"]["key"] # regular, league_team, league_pair, private, fes_solo, fes_team
	if lobby == "regular": # turf war solo
		payload["lobby"] = "standard"
		payload["mode"] = "regular"
	elif lobby == "gachi": # ranked solo
		payload["lobby"] = "standard"
		payload["mode"] = "gachi"
	elif lobby == "league_pair": # league pair
		payload["lobby"] = "squad_2"
		payload["mode"] = "gachi"
	elif lobby == "league_team": # league team
		payload["lobby"] = "squad_4"
		payload["mode"] = "gachi"
	elif lobby == "private": # private battle
		payload["lobby"] = "private"
		payload["mode"] = "private"
	elif lobby == "fes_solo": # splatfest solo
		payload["lobby"] = "standard"
		payload["mode"] = "fest"
	elif lobby == "fes_team":# splatfest team
		payload["lobby"] = "squad_4"
		payload["mode"] = "fest"

	##########
	## RULE ##
	##########
	rule = results[i]["rule"]["key"] # turf_war, rainmaker, splat_zones, tower_control
	if rule == "turf_war":
		payload["rule"] = "nawabari"
	elif rule == "splat_zones":
		payload["rule"] = "area"
	elif rule == "tower_control":
		payload["rule"] = "yagura"
	elif rule == "rainmaker":
		payload["rule"] = "hoko"

	###########
	## STAGE ##
	###########
	stage = int(results[i]["stage"]["id"])
	payload["stage"] = translate_stages[stage]

	############
	## WEAPON ##
	############
	weapon = int(results[i]["player_result"]["player"]["weapon"]["id"])
	payload["weapon"] = translate_weapons[weapon]

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
		payload["my_team_percent"] = my_percent
		payload["his_team_percent"] = their_percent
	elif mode == "gachi" or mode == "league":
		payload["my_team_count"] = my_count
		payload["his_team_count"] = their_count
		if my_count == 100 or their_count == 100:
			payload["knock_out"] = "yes"
		else:
			payload["knock_out"] = "no"

	################
	## TURF INKED ##
	################
	turfinked = results[i]["player_result"]["game_paint_point"] # without bonus
	if rule == "turf_war": # only upload if TW
		if result == "victory":
			payload["my_point"] = turfinked + 1000 # win bonus
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
	payload["level"]       = level_before
	payload["level_after"] = level_after

	##########
	## RANK ##
	##########
	try: # only occur in either TW xor ranked
		rank_before = results[i]["player_result"]["player"]["udemae"]["name"].lower()
		rank_after  = results[i]["udemae"]["name"].lower()
		rank_exp = results[i]["player_result"]["player"]["udemae"]["s_plus_number"]
		rank_exp_after = results[i]["udemae"]["s_plus_number"]
		if rank_before == None:
			rank_before = "c-"
			rank_after = "c-"
	except: # in case of private battles where a player has never played ranked before
		rank_before = "c-"
		rank_after = "c-"
	if rule != "turf_war": # only upload if ranked
		payload["rank"]       = rank_before
		payload["rank_after"] = rank_after
		payload["rank_exp"] = rank_exp
		payload["rank_exp_after"] = rank_exp_after

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
	bn = results[i]["battle_number"]
	payload["private_note"] = "Battle #" + bn
	payload["splatnet_number"] = bn
	principal_id = results[i]["player_result"]["player"]["principal_id"]
	if mode == "league":
		payload["my_team_id"] = results[i]["tag_id"]

	############################
	## SPLATFEST TITLES/POWER ##
	############################ https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md#fest_title-fest_title_after
	if mode == "fes":
		title_before = results[i]["player_result"]["player"]["fes_grade"]["rank"]
		title_after = results[i]["fes_grade"]["rank"]
		payload["fest_power"] = results[i]["fes_power"]
		payload["my_team_power"] = results[i]["my_estimate_fes_power"]
		payload["his_team_power"] = results[i]["other_estimate_fes_power"]
		payload["fest_title"] = translate_fest_rank[title_before]
		payload["fest_title_after"] = translate_fest_rank[title_after]
	else:
		title_before = None

	################
	## SCOREBOARD ##
	################
	if YOUR_COOKIE != "": # if no cookie set, don't do this, as it requires online & will fail
		mystats = [mode, rule, result, k_or_a, death, special, weapon, level_before, rank_before, turfinked, title_before, principal_id]
		payload = set_scoreboard(payload, bn, mystats)

	##################
	## IMAGE RESULT ##
	##################
	if not s_flag:
		url = "https://app.splatoon2.nintendo.net/api/share/results/%s" % bn
		share_result = requests.post(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
		if share_result.status_code == requests.codes.ok:
			image_result_url = share_result.json().get("url")
			if image_result_url:
				image_result = requests.get(image_result_url, stream=True)
				if image_result.status_code == requests.codes.ok:
					payload["image_result"] = BytesIO(image_result.content).getvalue()
		if m_flag:
			url_profile = "https://app.splatoon2.nintendo.net/api/share/profile"
			settings = {'stage': stage, 'color': translate_profile_color[random.randrange(0, 6)]}
			share_result = requests.post(url_profile, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE), data=settings)
			if share_result.status_code == requests.codes.ok:
				profile_result_url = share_result.json().get("url")
				if profile_result_url:
					profile_result = requests.get(profile_result_url, stream=True)
					if profile_result.status_code == requests.codes.ok:
						payload["image_gear"] = BytesIO(profile_result.content).getvalue()

	##########
	## GEAR ## not in API v2 yet
	########## https://github.com/fetus-hina/stat.ink/blob/master/API.md#gears
	# headgear_id = results[i]["player_result"]["player"]["head"]["id"]
	# clothing_id = results[i]["player_result"]["player"]["clothes"]["id"]
	# shoes_id    = results[i]["player_result"]["player"]["shoes"]["id"]
	# payload["headgear"] = translate_headgear[int(headgear_id)]
	# payload["clothing"] = translate_clothing[int(clothing_id)]
	# payload["shoes"]    = translate_shoes[int(shoes_id)]

	###############
	## ABILITIES ## not in API v2 yet
	############### https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/ability.md
	# headgear_subs, clothing_subs, shoes_subs = ([-1,-1,-1] for i in xrange(3))
	# for j in xrange(3):
	# 	try:
	# 		headgear_subs[j] = results[i]["player_result"]["player"]["head_skills"]["subs"][j]["id"]
	# 	except:
	# 		headgear_subs[j] = '-1'
	# 	try:
	# 		clothing_subs[j] = results[i]["player_result"]["player"]["clothes_skills"]["subs"][j]["id"]
	# 	except:
	# 		clothing_subs[j] = '-1'
	# 	try:
	# 		shoes_subs[j] = results[i]["player_result"]["player"]["shoes_skills"]["subs"][j]["id"]
	# 	except:
	# 		shoes_subs[j] = '-1'
	# payload["headgear_main"]   = translate_ability[int(headgear_main)]
	# payload["clothing_main"]   = translate_ability[int(clothing_main)]
	# payload["shoes_main_name"] = translate_ability[int(shoes_main)]
	# payload["headgear_sub1"] = translate_ability[int(headgear_subs[0])]
	# payload["headgear_sub2"] = translate_ability[int(headgear_subs[1])]
	# payload["headgear_sub3"] = translate_ability[int(headgear_subs[2])]
	# payload["clothing_sub1"] = translate_ability[int(clothing_subs[0])]
	# payload["clothing_sub2"] = translate_ability[int(clothing_subs[1])]
	# payload["clothing_sub3"] = translate_ability[int(clothing_subs[2])]
	# payload["shoes_sub1"]    = translate_ability[int(shoes_subs[0])]
	# payload["shoes_sub2"]    = translate_ability[int(shoes_subs[1])]
	# payload["shoes_sub3"]    = translate_ability[int(shoes_subs[2])]

	#############
	## DRY RUN ##
	#############
	if t_flag: # -t provided
		payload["test"] = "dry_run" # works the same as 'validate' for now

	#**************
	#*** OUTPUT ***
	#**************
	if debug:
		print ""
		print json.dumps(payload).replace("\"", "'")
	else:
		# POST to stat.ink
		# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/request-body.md
		url     = 'https://stat.ink/api/v2/battle'
		auth    = {'Authorization': 'Bearer ' + API_KEY, 'Content-Type': 'application/x-msgpack'}

		if payload["agent"] != os.path.splitext(sys.argv[0])[0]:
			print "Could not upload. Please contact @frozenpandaman on Twitter/GitHub for assistance."
			exit(1)
		r2 = requests.post(url, headers=auth, data=msgpack.packb(payload))

		# Response
		try:
			print "Battle #" + str(i+1) + " uploaded to " + r2.headers.get('location') # display url
		except TypeError: # r.headers.get is likely NoneType, i.e. we received an error
			if t_flag:
				print "Battle #" + str(i+1) + " - message from server:"
			else:
				print "Error uploading battle #" + str(i+1) + ". Message from server:"
			print r2.content
			if not t_flag:
				cont = raw_input('Continue (y/n)? ')
				if cont[0].lower() == "n":
					print "Exiting."
					exit(1)

if __name__ == "__main__":
	is_m, is_s, is_t, filename = main()
	if is_m:
		monitor_battles(is_s, is_t, debug)
	else:
		n, results = get_num_battles()
		for i in reversed(xrange(n)):
			post_battle(i, results, is_s, is_t, is_m, debug)
		if debug:
			print ""
