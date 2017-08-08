# eli fessler
# clovervidia
import os.path, argparse
import requests, json
from operator import itemgetter

A_NAME = "splatnet2statink"
A_VERSION = "0.0.17"

API_KEY = "emITHTtDtIaCjdtPQ0s78qGWfxzj3JogYZqXhRnoIF4" # testing account API key. please replace with your own!

YOUR_COOKIE = "" # keep this secret!

# auth app.splatoon2.nintendo.net, generate cookie
# ???

# I/O
parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="filename", required=False,
					help="results JSON file", metavar="file.json")
parser.add_argument("-p", required=False, action="store_true",
					help="don't upload battle # as private note")
result = parser.parse_args()

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

if result.filename != None: # local file provided
	if not os.path.exists(result.filename):
		parser.error("File %s does not exist!" % result.filename) # exit
	with open(result.filename) as data_file:
		data = json.load(data_file)
else: # no argument
	print "Pulling data from online..." # grab data from SplatNet
	url = "https://app.splatoon2.nintendo.net/api/results"
	r = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
	data = json.loads(r.text)

try:
	results = data["results"] # all we care about
except KeyError: # no 'results' key, which means...
	print "Bad cookie."
	exit(1)

try:
	n = int(raw_input("Number of recent battles to upload (0-50)? "))
except ValueError, ex:
	print "Please enter an integer between 0 and 50."
	exit(1)
if n == 0:
	print "Exiting without uploading anything."
	exit(0)
elif n > 50:
	print "Cannot upload battle #" + str(n) + ". SplatNet 2 only stores the 50 most recent battles."
else:
	pass

# JSON parsing, fill out payload
# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md
payload = {'agent': A_NAME, 'agent_version': A_VERSION}

# Weapon database
# https://stat.ink/api-info/weapon2?_lang_=en-US
# https://stat.ink/api/v2/weapon
translate_weapons = {
	'.52 Gal': '52gal', # 50
	'.96 Gal': '96gal', # 80
	'Sploosh-o-matic': 'bold', # 0
	'H-3 Nozzlenose': 'h3reelgun', # 310
	'Hero Shot Replica': 'heroshooter_replica', # 45
	'Jet Squelcher': 'jetsweeper', # 90
	'L-3 Nozzlenose': 'l3reelgun', # 300
	'N-ZAP \'85': 'nzap85', # 60
	'Splattershot Pro': 'prime', # 70
	'Aerospray MG': 'promodeler_mg', # 30
	'Aerospray RG': 'promodeler_rg', # 31
	'Splash-o-matic': 'sharp', # 20
	'Splattershot': 'sshooter', # 40
	'Tentatek Splattershot': 'sshooter_collabo', # 41
	'Splattershot Jr.': 'wakaba', # 10
	'Clash Blaster': 'clashblaster', # 230
	'Hero Blaster Replica': 'heroblaster_replica',
	'Blaster': 'hotblaster', # 210
	'Custom Blaster': 'hotblaster_custom',
	'Luna Blaster': 'nova',
	'Rapid Blaster': 'rapid', # 240
	'Dualie Squelchers': 'dualsweeper', # 5030
	'Hero Dualie Replicas': 'heromaneuver_replica', # 5050
	'Splat Dualies': 'maneuver', # 5010
	'Enperry Splat Dualies': 'maneuver_collabo', #5051
	'Dapple Dualies': 'sputtery', # 5000
	'Carbon Roller': 'carbon', # 1000
	'Dynamo Roller': 'dynamo', # 1020
	'Hero Roller Replica': 'heroroller_replica', # 1015
	'Splat Roller': 'splatroller', # 1010
	'Krak-On Splat Roller': 'splatroller_collabo', # 1011
	'Flingza Roller': 'variableroller', # 1030
	'Herobrush Replica': 'herobrush_replica',
	'Octobrush': 'hokusai', # 1110
	'Inkbrush': 'pablo', # 1100
	'Hero Charger Replica': 'herocharger_replica',
	'E-liter 4K': 'liter4k',
	'E-liter 4K Scope': 'liter4k_scope',
	'Goo Tuber': 'soytuber',
	'Splat Charger': 'splatcharger',
	'Firefin Splat Charger': 'splatcharger_collabo',
	'Splatterscope': 'splatscope', # 2020
	'Firefin Splatterscope': 'splatscope_collabo', # 2021
	'Slosher': 'bucketslosher', # 3000
	'Hero Slosher Replica': 'heroslosher_replica',
	'Tri-Slosher': 'hissen', # 3010
	'Heavy Splatling': 'barrelspinner', # 4010
	'Hero Splatling Replica': 'herospinner_replica', # 4015
	'Mini Splatling': 'splatspinner' # 4000
}

# Stage database
# codes @ https://app.splatoon2.nintendo.net/api/data/stages (needs auth)
translate_stages = {
	0: 'battera', # The Reef
	1: 'fujitsubo', # Musselforge Fitness
	2: 'gangaze', # Starfish Mainstage
	3: 'chozame', # Sturgeon Shipyard
	4: 'ama', # Inkblot Art Academy
	5: 'combu', # Humpback Pump Track
	# wtf nintendo
	7: 'hokke', # Port Mackerel
	8: 'tachiuo', # Moray Towers
	9999: 'mystery' # Shifty Station (Splatfest only)
}

# # Gear database
# translate_headgear = {
# 	5000: 'Studio Headphones'
# }
# translate_clothing = {
# 	5018: 'Takoroka Windcrusher'
# }
# translate_shoes = {
# 	4009: 'Snow Delta Straps'
# }

# Ability database
translate_ability = {
	-1:  'Locked', # locked ("?") or does not exist
	0:   'Ink Saver (Main)',
	1:   'Ink Saver (Sub)',
	2:   'Ink Recovery Up',
	3:   'Run Speed Up',
	4:   'Swim Speed Up',
	5:   'Special Charge Up',
	6:   'Special Saver',
	7:   'Special Power Up',
	8:   'Quick Respawn',
	9:   'Quick Super Jump',
	10:  'Sub Power Up',
	11:  'Ink Resistance Up',
	12:  'Bomb Defense Up',
	13:  'Cold-Blooded',
	100: 'Opening Gambit',
	101: 'UNKNOWN', # Last-Ditch Effort?
	102: 'Tenacity',
	103: 'UNKNOWN', # Comeback?
	104: 'Ninja Squid',
	105: 'UNKNOWN', # Haunt?
	106: 'Thermal Ink',
	107: 'UNKNOWN', # Respawn Punisher?
	108: 'Ability Doubler',
	109: 'UNKNOWN', # Stealth Jump?
	110: 'UNKNOWN', # Object Shredder?
	111: 'UNKNOWN' # Drop Roller?
}

for i in reversed(xrange(n)):
	# regular, league_team, league_pair, private, fes_solo, fes_team
	lobby  = results[i]["game_mode"]["key"]
	# regular, gachi, league, fes
	mode   = results[i]["type"]
	# turf_war, rainmaker, splat_zones, tower_control
	rule   = results[i]["rule"]["key"]
	stage  = results[i]["stage"]["id"]                               # string (see above)
	weapon = results[i]["player_result"]["player"]["weapon"]["name"] # string (see above)

	# victory, defeat
	result    = results[i]["my_team_result"]["key"]
	turfinked = results[i]["player_result"]["game_paint_point"]         # WITHOUT bonus
	kill      = results[i]["player_result"]["kill_count"]
	k_or_a    = results[i]["player_result"]["assist_count"] + kill
	special   = results[i]["player_result"]["special_count"]
	death     = results[i]["player_result"]["death_count"]

	level_after  = results[i]["player_rank"]
	level_before = results[i]["player_result"]["player"]["player_rank"]

	start_time = results[i]["start_time"]

	try: # only occur in either TW xor ranked
		rank_before = results[i]["player_result"]["player"]["udemae"]["name"].lower()
		rank_after  = results[i]["udemae"]["name"].lower()
		if rank_before == None: # in case of private battles where a player has never played ranked before
			rank_before = "c-"
			rank_after = "c-"
	except:
		pass
	try:
		my_count    = results[i]["my_team_count"]
		their_count = results[i]["other_team_count"]
	except:
		pass
	try:
		my_percent    = results[i]["my_team_percentage"]
		their_percent = results[i]["other_team_percentage"]
	except KeyError:
		pass # don't need to handle - won't be put into the payload unless relevant

	try:
		elapsed_time = results[i]["elapsed_time"] # apparently only a thing in ranked
	except KeyError:
		elapsed_time = 180 # turf war - 3 minutes in seconds

	# scoreboard stats and player ranking
	if YOUR_COOKIE != "": # in case using local file/no cookie set
		battle_number = results[i]["battle_number"]
		url = "https://app.splatoon2.nintendo.net/api/results/" + battle_number
		battle = requests.get(url, headers=app_head, cookies=dict(iksm_session=YOUR_COOKIE))
		battledata = json.loads(battle.text)

		try:
			battledata["battle_number"]
		except KeyError:
			print "Problem retrieving battle."
			exit(1) # in future, should return (without setting scoreboard data)

		ally_scoreboard = []
		for n in xrange(len(battledata["my_team_members"])):
			ally_stats = []
			ally_stats.append(battledata["my_team_members"][n]["sort_score"])
			ally_stats.append(battledata["my_team_members"][n]["kill_count"] + battledata["my_team_members"][n]["assist_count"])
			ally_stats.append(battledata["my_team_members"][n]["assist_count"])
			ally_stats.append(battledata["my_team_members"][n]["death_count"])
			ally_stats.append(battledata["my_team_members"][n]["special_count"])
			ally_stats.append(translate_weapons[battledata["my_team_members"][n]["player"]["weapon"]["name"]])
			ally_stats.append(battledata["my_team_members"][n]["player"]["player_rank"])
			if mode == "gachi":
				ally_stats.append(battledata["my_team_members"][n]["player"]["udemae"]["name"].lower())
				ally_stats.append(None) # points of turf inked is null if ranked battle
			elif mode == "regular" or mode == "fest":
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
		my_stats.append(translate_weapons[weapon])
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

		# scoreboard sorted by sort_score, then kills + assists, assists, deaths (reverse order), & finally specials
		sorted_ally_scoreboard = sorted(ally_scoreboard, key=itemgetter(0, 1, 2), reverse=True)
		sorted_ally_scoreboard.sort(ally_scoreboard, key=itemgetter(3))
		sorted_ally_scoreboard.sort(ally_scoreboard, key=itemgetter(4), reverse=True)

		enemy_scoreboard = []
		for n in xrange(len(battledata["other_team_members"])):
			enemy_stats = []
			enemy_stats.append(battledata["other_team_members"][n]["sort_score"])
			enemy_stats.append(battledata["other_team_members"][n]["kill_count"] +
							   battledata["other_team_members"][n]["assist_count"])
			enemy_stats.append(battledata["other_team_members"][n]["assist_count"])
			enemy_stats.append(battledata["other_team_members"][n]["death_count"])
			enemy_stats.append(battledata["other_team_members"][n]["special_count"])
			enemy_stats.append(translate_weapons[battledata["other_team_members"][n]["player"]["weapon"]["name"]])
			enemy_stats.append(battledata["other_team_members"][n]["player"]["player_rank"])
			if mode == "gachi":
				enemy_stats.append(battledata["other_team_members"][n]["player"]["udemae"]["name"].lower())
				enemy_stats.append(None)
			elif mode == "regular" or mode == "fest":
				enemy_stats.append(None)
				if result == "defeat":
					enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"] + 1000)
				else:
					enemy_stats.append(battledata["other_team_members"][n]["game_paint_point"])
			enemy_stats.append(0) # my team? (no)
			enemy_stats.append(0) # is me? (no)
			enemy_scoreboard.append(enemy_stats)

		sorted_enemy_scoreboard = sorted(enemy_scoreboard, key=itemgetter(0, 1, 2), reverse=True)
		sorted_enemy_scoreboard.sort(enemy_scoreboard, key=itemgetter(3))
		sorted_enemy_scoreboard.sort(enemy_scoreboard, key=itemgetter(4), reverse=True)

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

	# headgear_id  = results[i]["player_result"]["player"]["head"]["id"]
	# clothing_id  = results[i]["player_result"]["player"]["clothes"]["id"]
	# shoes_id     = results[i]["player_result"]["player"]["shoes"]["id"]

	# headgear_main  = results[i]["player_result"]["player"]["head_skills"]["main"]["id"]
	# clothing_main  = results[i]["player_result"]["player"]["clothes_skills"]["main"]["id"]
	# shoes_main     = results[i]["player_result"]["player"]["shoes_skills"]["main"]["id"]

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

	# lobby + mode
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

	# rule
	if rule == "turf_war":
		payload["rule"] = "nawabari"
	elif rule == "splat_zones":
		payload["rule"] = "area"
	elif rule == "tower_control":
		payload["rule"] = "yagura"
	elif rule == "rainmaker":
		payload["rule"] = "hoko"

	# stage
	payload["stage"] = translate_stages[int(stage)]

	# weapon
	payload["weapon"] = translate_weapons[weapon]

	# result
	if result == "victory":
		payload["result"] = "win"
	elif result == "defeat":
		payload["result"] = "lose"

	# team percents/counts
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

	# turf inked
	if rule == "turf_war": # only upload if TW
		if result == "victory":
			payload["my_point"] = turfinked + 1000 # win bonus
		else:
			payload["my_point"] = turfinked

	# kills, etc.
	payload["kill"] = kill
	payload["kill_or_assist"] = k_or_a
	payload["special"] = special
	payload["death"] = death

	# level
	payload["level"] = level_before
	payload["level_after"] = level_after

	# rank
	if rule != "turf_war": # only upload if Ranked
		payload["rank"] = rank_before
		payload["rank_after"] = rank_after

	# splatfest titles/power - only in API v1 for now
	# https://github.com/fetus-hina/stat.ink/blob/master/API.md
	if mode == "fes":
		title = results[i]["fes_grade"]["rank"]
		payload["fest_power"] = results[i]["fes_power"]
		payload["my_team_power"] = results[i]["my_estimate_fes_power"]
		payload["his_team_power"] = results[i]["other_estimate_fes_power"]
		if title == 0: # ___ fangirl/boy
			payload["fest_title"] = "fanboy"
		elif title == 1: # ___ fiend
			payload["fest_title"] = "fiend"
		elif title == 2: # ___ defender
			payload["fest_title"] = "defender"
		elif title == 3: # ___ champion
			payload["fest_title"] = "champion"
		elif title == 4: # ___ queen/king
			payload["fest_title"] = "king"

	# battle times
	payload["start_at"] = start_time
	payload["end_at"] = start_time + elapsed_time

	# battle number
	if not result.p: # -p not provided
		payload["private_note"] = "Battle #" + battle_number

	# gear - not implemented in stat.ink API v2 yet
	# API v1: https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/gear.md
	#         https://github.com/fetus-hina/stat.ink/blob/master/API.md#gears
	# payload["headgear"] = translate_headgear[int(headgear_id)]
	# payload["clothing"] = translate_clothing[int(clothing_id)]
	# payload["shoes"] = translate_shoes[int(shoes_id)]

	# abilities - not implemented in stat.ink API v2 yet
	# API v1: https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/ability.md
	# payload["headgear_main"] = translate_ability[int(headgear_main)]
	# payload["clothing_main"] = translate_ability[int(clothing_main)]
	# payload["shoes_main_name"] = translate_ability[int(shoes_main)]
	# payload["headgear_sub1"] = translate_ability[int(headgear_subs[0])]
	# payload["headgear_sub2"] = translate_ability[int(headgear_subs[1])]
	# payload["headgear_sub3"] = translate_ability[int(headgear_subs[2])]
	# payload["clothing_sub1"] = translate_ability[int(clothing_subs[0])]
	# payload["clothing_sub2"] = translate_ability[int(clothing_subs[1])]
	# payload["clothing_sub3"] = translate_ability[int(clothing_subs[2])]
	# payload["shoes_sub1"] = translate_ability[int(shoes_subs[0])]
	# payload["shoes_sub2"] = translate_ability[int(shoes_subs[1])]
	# payload["shoes_sub3"] = translate_ability[int(shoes_subs[2])]

	# debugging
	# print payload

	# POST to stat.ink
	url     = 'https://stat.ink/api/v2/battle'
	auth    = {'Authorization': 'Bearer ' + API_KEY, 'Content-Type': 'application/json'}

	r2 = requests.post(url, headers=auth, data=json.dumps(payload))

	# Response
	try:
		print "Battle #" + str(i+1) + " uploaded to " + r2.headers.get('location') # display url
	except TypeError: # r.headers.get is likely NoneType, i.e. we received an error
		print "Error uploading battle #" + str(i+1) + ". Message from server:"
		print r2.content
		cont = raw_input('Continue (y/n)? ')
		if cont in ['n', 'N', 'no', 'No', 'NO']:
			exit(1)