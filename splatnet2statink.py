# eli fessler
import requests, json

A_NAME = "splatnet2statink"
A_VERSION = "0.0.3"

# auth app.splatoon2.nintendo.net
# grab data from https://app.splatoon2.nintendo.net/api/results
# ...


# I/O
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

filename = "results.json" # for now
with open(filename) as data_file:
	data = json.load(data_file)
results = data["results"] # all we care about

# Weapon database
translate_weapons = {
	'.52 Gal': '52gal',
	'.96 Gal': '96gal',
	'Clash Blaster': 'clashblaster',
	'Dualie Squelchers': 'dualsweeper', #check
	'H-3 Nozzlenose': 'h3reelgun',
	'Custom Blaster': 'hotblaster_custom',
	'Blaster': 'hotblaster',
	'Jet Squelcher': 'jetsweeper',
	'L-3 Nozzlenose': 'l3reelgun',
	'Enperry Splat Dualies': 'manueuver_collabo',
	'Splat Dualies': 'manueuver',
	'Luna Blaster': 'nova',
	'N-ZAP \'85': 'nzap85',
	'Splattershot Pro': 'prime',
	'Aerospray MG': 'promodeler_mg',
	'Aerospray RG': 'promodeler_rg',
	'Rapid Blaster': 'rapid',
	'Splash-o-matic': 'sharp',
	'Dapple Dualies': 'sputtery',
	'Tentatek Splattershot': 'sshooter_collabo',
	'Splattershot': 'sshooter',
	'Splattershot Jr.': 'wakaba',
	'Carbon Roller': 'carbon',
	'Dynamo Roller': 'dynamo',
	'Octobrush': 'hokusai',
	'Inkbrush': 'pablo',
	'Krak-On Splat Roller': 'splatroller_collabo',
	'Splat Roller': 'splatroller',
	'Flingza Roller': 'variableroller',
	'E-liter 4K Scope': 'liter4k_scope', # check capitalization, en_GB spelling
	'E-litre 4K Scope': 'liter4k_scope',
	'E-liter 4K ': 'liter4k',
	'E-litre 4K ': 'liter4k',
	'Goo Tuber': 'soytuber',
	'Firefin Splat Charger': 'splatcharger_collabo',
	'Splat Charger': 'splatcharger',
	'Firefin Splatterscope': 'splatscope_collabo',
	'Splatterscope': 'splatscope',
	'Slosher': 'bucketslosher',
	'Tri-Slosher': 'hissen',
	'Heavy Splatling': 'barrelspinner',
	'Mini Splatling': 'splatspinner'
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
	6: 'hokke', # Port Mackerel
	7:  'tachiuo' # Moray Towers
}

#Prepare to POST to stat.ink
url     = 'https://stat.ink/api/v2/battle'
auth    = {'Authorization': 'Bearer emITHTtDtIaCjdtPQ0s78qGWfxzj3JogYZqXhRnoIF4'} # testing account API key

for i in range (0, n):
	lobby     = results[i]["game_mode"]["key"]      # regular, league_team, league_pair, ???
	mode      = results[i]["type"]                  # regular, league, ???
	rule      = results[i]["rule"]["key"]           # turf_war, rainmaker, splat_zones, tower_control
	stage     = results[i]["stage"]["id"]           # string (see above)
	weapon    = results[i]["player_result"]["player"]["weapon"]["name"] # string (see above)
	result    = results[i]["my_team_result"]["key"]             # victory, defeat
	turfinked = results[i]["player_result"]["game_paint_point"] # integer (WITHOUT bonus)
	kill           = results[i]["player_result"]["kill_count"]          # integer
	kill_or_assist = kill + results[i]["player_result"]["assist_count"] # integer
	special        = results[i]["player_result"]["special_count"]       # integer
	death          = results[i]["player_result"]["death_count"]         # integer
	# rank       = results[i]["player"]["udemae"]["name"]       # e.g. C+
	# rank_after = ...

	# lobby
	if lobby == "regular":
		payload["lobby"] = "standard"
	elif lobby == "league_pair":
		payload["lobby"] = "squad_2"
	elif lobby == "league_team":
		payload["lobby"] = "squad_4"
	#elif lobby = private battle:
	#	payload["lobby"] = "private"

	# mode
	if mode == "regular":
		payload["mode"] = "regular"
	elif mode == "league":
		payload["mode"] = "gachi"
	# elif mode = solo ranked:
	# 	payload["mode"] = "gachi"
	# elif mode = splatfest: - may be the same as regular, since splatfests are turf wars
	# 	payload["mode"] = "fest"
	# elif mode = private:
	# 	payload["mode"] = "private"

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

	# my_point
	if result == "victory":
		payload["my_point"] = turfinked + 1000 # win bonus
	else:
		payload["my_point"] = turfinked

	# kills, etc.
	payload["kill"] = kill
	payload["kill_or_assist"] = kill_or_assist
	payload["special"] = special
	payload["death"] = death

	# debugging
	# print payload

	# POST request
	r = requests.post(url, headers=auth, data=payload)

	# Response (assuming success for now)
	print "Battle uploaded to " + r.headers.get('location') # url of uploaded battle