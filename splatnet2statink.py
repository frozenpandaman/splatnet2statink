# eli fessler
# clovervidia
import os.path, argparse, sys
import requests, json
import iksm, dbs
from operator import itemgetter

A_VERSION = "0.0.25"

##############################
######## CHANGE BELOW ######## (Keep these secret!)
API_KEY       = "" # for splat.ink
YOUR_COOKIE   = "" # iksm_session
SESSION_TOKEN = "" # to generate new cookies in the future
######## CHANGE ABOVE ########
##############################

debug = False

app_head = {
	'Host': 'app.splatoon2.nintendo.net',
	'x-unique-id': '32449507786579989234', # random 19-20 digit num
	'x-requested-with': 'XMLHttpRequest',
	'x-timezone-offset': '0',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
	'Accept': '*/*',
	'Referer': 'https://app.splatoon2.nintendo.net/home',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US'
}
payload = {'agent': 'splatnet2statink', 'agent_version': A_VERSION}

translate_weapons = dbs.weapons
translate_stages = dbs.stages
# translate_headgear = dbs.headgears
# translate_clothing = dbs.clothes
# translate_shoes = dbs.shoes
# translate_ability = dbs.abilities


def gen_new_cookie(reason):
	'''Attempts to generate new cookie in case provided one is invalid.'''
	if reason == "blank":
		print "Blank cookie. Trying to generate one given your session_token..."
	else: # auth, error
		print "Bad cookie. Trying to generate a new one given your session_token..."
	if SESSION_TOKEN == "":
		print "session_token is blank. Could not generate cookie."
		exit(1)
	else:
		NEW_COOKIE = iksm.get_cookie(SESSION_TOKEN)
		print "New cookie: " + NEW_COOKIE + ".\nPlease set this as YOUR_COOKIE and run the script again."
		exit(0)

def load_json():
	'''Returns results JSON from online.'''

	print "Pulling data from online..." # grab data from SplatNet
	url = "https://app.splatoon2.nintendo.net/api/results"
	r = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
	return json.loads(r.text)

def get_num_battles():
	'''I/O and setup. Returns number of battles to upload along with results json.'''

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", dest="filename", required=False,
						help="results JSON file", metavar="file.json")
	parser.add_argument("-t", required=False, action="store_true",
						help="dry run for testing (don't upload to stat.ink)")
	parser.add_argument("-p", required=False, action="store_true",
						help="don't upload battle # as private note")
	parser_result = parser.parse_args()

	if parser_result.filename != None: # local file provided
		if not os.path.exists(parser_result.filename):
			parser.error("File %s does not exist!" % parser_result.filename) # exit
		with open(parser_result.filename) as data_file:
			data = json.load(data_file)
	else: # no argument
		data = load_json()

	try:
		results = data["results"] # all we care about
	except KeyError: # no 'results' key, which means...
		if YOUR_COOKIE == "":
			reason = "blank"
		elif data["code"] == "AUTHENTICATION_ERROR":
			reason = "auth"
		else:
			reason = "other"
		gen_new_cookie(reason)

	try:
		n = int(raw_input("Number of recent battles to upload (0-50)? "))
	except ValueError, ex:
		print "Please enter an integer between 0 and 50."
		exit(1)
	if n == 0:
		print "Exiting without uploading anything."
		exit(0)
	elif n > 50:
		print "SplatNet 2 only stores the 50 most recent battles. Exiting."
		exit(0)
	else:
		is_p = parser_result.p
		is_t = parser_result.t
		return n, results, is_p, is_t

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

	ally_scoreboard = []
	for n in xrange(len(battledata["my_team_members"])):
		ally_stats = []
		ally_stats.append(battledata["my_team_members"][n]["sort_score"])
		ally_stats.append(battledata["my_team_members"][n]["kill_count"] +
						  battledata["my_team_members"][n]["assist_count"])
		ally_stats.append(battledata["my_team_members"][n]["assist_count"])
		ally_stats.append(battledata["my_team_members"][n]["death_count"])
		ally_stats.append(battledata["my_team_members"][n]["special_count"])
		ally_stats.append(translate_weapons[int(battledata["my_team_members"][n]["player"]["weapon"]["id"])])
		ally_stats.append(battledata["my_team_members"][n]["player"]["player_rank"])
		if mode == "gachi":
			ally_stats.append(battledata["my_team_members"][n]["player"]["udemae"]["name"].lower()) # might have to apply a forced C- if no rank in a private battle
			ally_stats.append(None) # points of turf inked is null if ranked battle
		elif rule == "turf_war":
			ally_stats.append(None) # udemae (rank) is null if turf war
			if result == "victory":
				ally_stats.append(battledata["my_team_members"][n]["game_paint_point"] + 1000)
			else:
				ally_stats.append(battledata["my_team_members"][n]["game_paint_point"])
		ally_stats.append(1) # my team? (yes)
		ally_stats.append(0) # is me? (no)
		ally_scoreboard.append(ally_stats)

	my_stats = []
	my_stats.append(battledata["player_result"]["sort_score"])
	my_stats.append(k_or_a)
	my_stats.append(battledata["player_result"]["assist_count"])
	my_stats.append(death)
	my_stats.append(special)
	my_stats.append(translate_weapons[int(weapon)])
	my_stats.append(level_before)
	if mode == "gachi":
		my_stats.append(rank_before)
		my_stats.append(None) # points of turf inked is null if ranked battle
	elif mode == "regular" or mode == "fest":
		my_stats.append(None) # udemae (rank) is null if turf war
		if result == "victory":
			my_stats.append(turfinked + 1000)
		else:
			my_stats.append(turfinked)
	my_stats.append(1) # my team? (yes)
	my_stats.append(1) # is me? (yes)
	ally_scoreboard.append(my_stats)

	# scoreboard sorted by sort_score, then kills + assists, assists, deaths (higher = better, for some reason), & finally specials
	sorted_ally_scoreboard = sorted(ally_scoreboard, key=itemgetter(0, 1, 2, 3, 4), reverse=True)

	for n in xrange(len(sorted_ally_scoreboard)):
		if sorted_ally_scoreboard[n][-1] == 1:
			payload["rank_in_team"] = n + 1
			break

	enemy_scoreboard = []
	for n in xrange(len(battledata["other_team_members"])):
		enemy_stats = []
		enemy_stats.append(battledata["other_team_members"][n]["sort_score"])
		enemy_stats.append(battledata["other_team_members"][n]["kill_count"] +
						   battledata["other_team_members"][n]["assist_count"])
		enemy_stats.append(battledata["other_team_members"][n]["assist_count"])
		enemy_stats.append(battledata["other_team_members"][n]["death_count"])
		enemy_stats.append(battledata["other_team_members"][n]["special_count"])
		enemy_stats.append(translate_weapons[int(battledata["other_team_members"][n]["player"]["weapon"]["id"])])
		enemy_stats.append(battledata["other_team_members"][n]["player"]["player_rank"])
		if mode == "gachi":
			enemy_stats.append(battledata["other_team_members"][n]["player"]["udemae"]["name"].lower())  # might have to apply a forced C- if no rank in a private battle
			enemy_stats.append(None)
		elif rule == "turf_war":
			enemy_stats.append(None)
			if result == "defeat":
				enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"] + 1000)
			else:
				enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"])
		enemy_stats.append(0) # my team? (no)
		enemy_stats.append(0) # is me? (no)
		enemy_scoreboard.append(enemy_stats)

	sorted_enemy_scoreboard = sorted(enemy_scoreboard, key=itemgetter(0, 1, 2, 3, 4), reverse=True)

	full_scoreboard = sorted_ally_scoreboard + sorted_enemy_scoreboard

	payload["players"] = []
	for n in xrange(len(full_scoreboard)):
		detail = {
			"team": "my" if full_scoreboard[n][-2] == 1 else "his",
			"is_me": "yes" if full_scoreboard[n][-1] == 1 else "no",
			"weapon": full_scoreboard[n][5],
			"level": full_scoreboard[n][6],
			"rank_in_team": n + 1 if n < 4 else n - 3,
			"kill": full_scoreboard[n][1] - full_scoreboard[n][2],
			"death": full_scoreboard[n][3],
			"kill_or_assist": full_scoreboard[n][1],
			"special": full_scoreboard[n][4],
			"point": full_scoreboard[n][-3]
		}
		if mode == "gachi":
			detail["rank"] = full_scoreboard[n][-4]
		payload["players"].append(detail)

	return payload # return new payload w/ players key

# # https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md
def post_battle(i, results, payload, p_flag, t_flag, debug):
	'''Uploads battle #i from the provided dictionary.'''

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
		if rank_before == None:
			rank_before = "c-"
			rank_after = "c-"
	except: # in case of private battles where a player has never played ranked before
		rank_before = "c-"
		rank_after = "c-"
	if rule != "turf_war": # only upload if ranked
		payload["rank"]       = rank_before
		payload["rank_after"] = rank_after

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
	## BATTLE NUMBER ##
	###################
	bn = results[i]["battle_number"]
	if not p_flag: # -p not provided
		payload["private_note"] = "Battle #" + bn

	############################
	## SPLATFEST TITLES/POWER ##
	############################ https://github.com/fetus-hina/stat.ink/blob/master/API.md
	if mode == "fes":
		title_before = results[i]["player_result"]["player"]["fes_grade"]["rank"]
		title_after = results[i]["fes_grade"]["rank"]
		payload["fest_power"] = results[i]["fes_power"]
		payload["my_team_power"] = results[i]["my_estimate_fes_power"]
		payload["his_team_power"] = results[i]["other_estimate_fes_power"]
		if title_before == 0:
			payload["fest_title"] = "fanboy"
		elif title_before == 1:
			payload["fest_title"] = "fiend"
		elif title_before == 2:
			payload["fest_title"] = "defender"
		elif title_before == 3:
			payload["fest_title"] = "champion"
		elif title_before == 4:
			payload["fest_title"] = "king"
		if title_after == 0:
			payload["fest_title_after"] = "fanboy"
		elif title_after == 1:
			payload["fest_title_after"] = "fiend"
		elif title_after == 2:
			payload["fest_title_after"] = "defender"
		elif title_after == 3:
			payload["fest_title_after"] = "champion"
		elif title_after == 4:
			payload["fest_title_after"] = "king"

	################
	## SCOREBOARD ##
	################
	if YOUR_COOKIE != "": # if no cookie set, don't do this, as it requires online & will fail
		mystats = [mode, rule, result, k_or_a, death, special, weapon, level_before, rank_before, turfinked]
		payload = set_scoreboard(payload, bn, mystats)

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
		url     = 'https://stat.ink/api/v2/battle'
		auth    = {'Authorization': 'Bearer ' + API_KEY, 'Content-Type': 'application/json'}

		if payload["agent"] != os.path.splitext(sys.argv[0])[0]:
			print "Could not upload. Please contact @frozenpandaman on Twitter/GitHub for assistance."
			exit(1)
		r2 = requests.post(url, headers=auth, json=payload)

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
				if cont in ['n', 'N', 'no', 'No', 'NO']:
					exit(1)

if __name__=="__main__":
	n, results, is_p, is_t = get_num_battles()
	for i in reversed(xrange(n)):
		post_battle(i, results, payload, is_p, is_t, debug)
	if debug:
		print ""