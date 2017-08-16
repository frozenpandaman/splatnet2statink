# eli fessler

# Weapons database
# https://stat.ink/api-info/weapon2?_lang_=en-US
# https://stat.ink/api/v2/weapon
weapons = {
	0:    'bold', # Sploosh-o-matic
	10:   'wakaba', # Splattershot Jr.
	20:   'sharp', # Splash-o-matic
	30:   'promodeler_mg', # Aerospray MG
	31:   'promodeler_rg', # Aerospray RG
	40:   'sshooter', # Splattershot
	41:   'sshooter_collabo', # Tentatek Splattershot
	45:   'heroshooter_replica', # Hero Shot Replica
	50:   '52gal', # .52 Gal
	60:   'nzap85', # N-ZAP '85
	70:   'prime', # Splattershot Pro
	80:   '96gal', # .96 Gal
	90:   'jetsweeper', # Jet Squelcher
	200:  'nova', # Luna Blaster
	210:  'hotblaster', # Blaster
	211:  'hotblaster_custom', # Custom Blaster
	215:  'heroblaster_replica', # Hero Blaster Replica
	230:  'clashblaster', # Clash Blaster
	240:  'rapid', # Rapid Blaster
	300:  'l3reelgun', # L-3 Nozzlenose
	310:  'h3reelgun', # H-3 Nozzlenose
	1000: 'carbon', # Carbon Roller
	1010: 'splatroller', # Splat Roller
	1011: 'splatroller_collabo', # Krak-On Splat Roller
	1015: 'heroroller_replica', # Hero Roller Replica
	1020: 'dynamo', # Dynamo Roller
	1030: 'variableroller', # Flingza Roller
	1100: 'pablo', # Inkbrush
	1110: 'hokusai', # Octobrush
	1115: 'herobrush_replica', # Herobrush Replica
	2010: 'splatcharger', # Splat Charger
	2011: 'splatcharger_collabo', # Firefin Splat Charger
	2015: 'herocharger_replica', # Hero Charger Replica
	2020: 'splatscope', # Splatterscope
	2021: 'splatscope_collabo', # Firefin Splatterscope
	2030: 'liter4k', # E-liter 4K
	2040: 'liter4k_scope', # E-liter 4K Scope
	2060: 'soytuber', # Goo Tuber
	3000: 'bucketslosher', # Slosher
	3005: 'heroslosher_replica', # Hero Slosher Replica
	3010: 'hissen', # Tri-Slosher
	4000: 'splatspinner', # Mini Splatling
	4010: 'barrelspinner', # Heavy Splatling
	4015: 'herospinner_replica', # Hero Splatling Replica
	5000: 'sputtery', # Dapple Dualies
	5010: 'maneuver', # Splat Dualies
	5011: 'maneuver_collabo', # Enperry Splat Dualies
	5015: 'heromaneuver_replica', # Hero Dualie Replicas
	5030: 'dualsweeper', # Dualie SqBrellauelchers
	6000: 'parashelter', # Splat
	6005: 'heroshelter_replica' # Hero Brella Replica
}

# Stage database
# https://app.splatoon2.nintendo.net/api/data/stages (needs auth)
stages = {
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

# Gear database
# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/gear.md
headgears = {
	5000: 'studio_headphones'
}
clothes = {
	5018: 'takoroka_windcrusher'
}
shoes = {
	4009: 'snow_delta_straps'
}

# Ability database
# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/ability.md
abilities = {
	-1:  '', # locked ("?") or does not exist
	0:   'ink_saver_main',
	1:   'ink_saver_sub',
	2:   'ink_recovery_up',
	3:   'run_speed_up',
	4:   'swim_speed_up',
	5:   'special_charge_up',
	6:   'special_saver',
	7:   'special_power_up',
	8:   'quick_respawn',
	9:   'quick_super_jump',
	10:  'sub_power_up',
	11:  'ink_resistance_up',
	12:  'bomb_defense_up',
	13:  'cold_blooded',
	100: 'opening_gambit',
	101: 'last_ditch_effort',
	102: 'tenacity',
	103: 'comeback',
	104: 'ninja_squid',
	105: 'haunt',
	106: 'thermal_ink',
	107: 'respawn_punisher',
	108: 'ability_doubler',
	109: 'stealth_jump',
	110: 'object_shredder',
	111: 'drop_roller'
}