# eli fessler
import os.path, argparse
import requests, json

A_NAME = "splatnet2statink"
A_VERSION = "0.0.13"

API_KEY = "emITHTtDtIaCjdtPQ0s78qGWfxzj3JogYZqXhRnoIF4" # testing account API key. please replace with your own!

YOUR_COOKIE = "" # keep this secret!

# auth app.splatoon2.nintendo.net, generate cookie
# ???

# I/O
parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="filename", required=False,
					help="path to results JSON", metavar="/path/to/results.json")
result = parser.parse_args()

if result.filename != None: # local file provided
	if not os.path.exists(result.filename):
		parser.error("File %s does not exist!" % result.filename) # exit
	with open(result.filename) as data_file:
		data = json.load(data_file)
else: # no argument
	print "Pulling data from online..." # grab data from SplatNet
	url = "https://app.splatoon2.nintendo.net/api/results"
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
	'.52 Gal': '52gal',
	'.96 Gal': '96gal', # 50
	'Sploosh-o-matic': 'bold',
	'H-3 Nozzlenose': 'h3reelgun',
	'Hero Shot Replica': 'heroshooter_replica',
	'Jet Squelcher': 'jetsweeper',
	'L-3 Nozzlenose': 'l3reelgun', # 300
	'N-ZAP \'85': 'nzap85',
	'Splattershot Pro': 'prime', # 70
	'Aerospray MG': 'promodeler_mg', # 30
	'Aerospray RG': 'promodeler_rg',
	'Splash-o-matic': 'sharp',
	'Splattershot': 'sshooter',
	'Tentatek Splattershot': 'sshooter_collabo',
	'Splattershot Jr.': 'wakaba',
	'Clash Blaster': 'clashblaster', # 230
	'Hero Blaster Replica': 'heroblaster_replica',
	'Blaster': 'hotblaster', # 210
	'Custom Blaster': 'hotblaster_custom',
	'Luna Blaster': 'nova',
	'Rapid Blaster': 'rapid',
	'Dualie Squelchers': 'dualsweeper', # 5030
	'Hero Dualies Replica': 'heromaneuver_replica',
	'Splat Dualies': 'maneuver', # 5010
	'Enperry Splat Dualies': 'maneuver_collabo',
	'Dapple Dualies': 'sputtery',
	'Carbon Roller': 'carbon', # 1000
	'Dynamo Roller': 'dynamo',
	'Hero Roller Replica': 'heroroller_replica',
	'Splat Roller': 'splatroller',
	'Krak-On Splat Roller': 'splatroller_collabo',
	'Flingza Roller': 'variableroller',
	'Hero Brush Replica': 'herobrush_replica',
	'Octobrush': 'hokusai', # 1110
	'Inkbrush': 'pablo',
	'Hero Charger Replica': 'herocharger_replica',
	'E-liter 4K ': 'liter4k',
	'E-liter 4K Scope': 'liter4k_scope',
	'Goo Tuber': 'soytuber',
	'Splat Charger': 'splatcharger',
	'Firefin Splat Charger': 'splatcharger_collabo',
	'Splatterscope': 'splatscope',
	'Firefin Splatterscope': 'splatscope_collabo',
	'Slosher': 'bucketslosher', # 3000
	'Hero Slosher Replica': 'heroslosher_replica',
	'Tri-Slosher': 'hissen', # 3010
	'Heavy Splatling': 'barrelspinner',
	'Hero Splatling Replica': 'herospinner_replica',
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

# Prepare to POST to stat.ink
url     = 'https://stat.ink/api/v2/battle'
auth    = {'Authorization': 'Bearer ' + API_KEY}

for i in reversed(xrange(n)):
	# regular, league_team, league_pair, private
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
		rank_before = results[i]["player_result"]["player"]["udemae"]["name"]
		rank_after  = results[i]["udemae"]["name"]
	except:
		pass
	try:
		my_count      = results[i]["my_team_count"]
		their_count   = results[i]["other_team_count"]
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

	# headgear_id  = results[i]["player_result"]["player"]["head"]["id"]
	# clothing_id  = results[i]["player_result"]["player"]["clothes"]["id"]
	# shoes_id     = results[i]["player_result"]["player"]["shoes"]["id"]

	# headgear_main  = results[i]["player_result"]["player"]["head_skills"]["main"]["id"]
	# clothing_main  = results[i]["player_result"]["player"]["clothes_skills"]["main"]["id"]
	# shoes_main     = results[i]["player_result"]["player"]["shoes_skills"]["main"]["id"]

	# headgear_subs, clothing_subs, shoes_subs = ([-1,-1,-1] for i in range(3))
	# for j in range (0, 3):
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

	# lobby
	if lobby == "regular":
		payload["lobby"] = "standard"
	elif lobby == "league_pair":
		payload["lobby"] = "squad_2"
	elif lobby == "league_team":
		payload["lobby"] = "squad_4"
	elif lobby == "private":
		payload["lobby"] = "private"
		payload["mode"] = "private"

	# mode
	# stat.ink displays solo ranked or splatfest as ? currently
	if mode == "regular":
		payload["mode"] = "regular"
	elif mode == "gachi" or mode == "league":
		payload["mode"] = "gachi"
	if mode == "fes":
		payload["mode"] = "fest"
	# private handled above

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
	# private...?

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
		payload["rank"] = rank_before.lower()
		payload["rank_after"] = rank_after.lower()

	# battle times
	payload["start_at"] = start_time
	payload["end_at"] = start_time + elapsed_time

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

	# POST request
	r2 = requests.post(url, headers=auth, data=payload)

	# Response
	try:
		print "Battle #" + str(i+1) + " uploaded to " + r2.headers.get('location') # display url
	except TypeError: # r.headers.get is likely NoneType, i.e. we received an error
		print "Error uploading battle #" + str(i+1) + ". Message from server:"
		print r2.content