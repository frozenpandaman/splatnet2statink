# eli fessler
# clovervidia

# Weapons database
# https://stat.ink/api-info/weapon2?_lang_=en-US
# https://stat.ink/api/v2/weapon
weapons = {
	0:    'bold',                 # Sploosh-o-matic
	10:   'wakaba',               # Splattershot Jr.
	20:   'sharp',                # Splash-o-matic
	30:   'promodeler_mg',        # Aerospray MG
	31:   'promodeler_rg',        # Aerospray RG
	40:   'sshooter',             # Splattershot
	41:   'sshooter_collabo',     # Tentatek Splattershot
	45:   'heroshooter_replica',  # Hero Shot Replica
	50:   '52gal',                # .52 Gal
	60:   'nzap85',               # N-ZAP '85
	70:   'prime',                # Splattershot Pro
	71:   'prime_collabo',        # Forge Splattershot Pro
	80:   '96gal',                # .96 Gal
	90:   'jetsweeper',           # Jet Squelcher
	200:  'nova',                 # Luna Blaster
	210:  'hotblaster',           # Blaster
	211:  'hotblaster_custom',    # Custom Blaster
	215:  'heroblaster_replica',  # Hero Blaster Replica
	230:  'clashblaster',         # Clash Blaster
	240:  'rapid',                # Rapid Blaster
	300:  'l3reelgun',            # L-3 Nozzlenose
	310:  'h3reelgun',            # H-3 Nozzlenose
	1000: 'carbon',               # Carbon Roller
	1010: 'splatroller',          # Splat Roller
	1011: 'splatroller_collabo',  # Krak-On Splat Roller
	1015: 'heroroller_replica',   # Hero Roller Replica
	1020: 'dynamo',               # Dynamo Roller
	1030: 'variableroller',       # Flingza Roller
	1100: 'pablo',                # Inkbrush
	1110: 'hokusai',              # Octobrush
	1115: 'herobrush_replica',    # Herobrush Replica
	2000: 'squiclean_a',          # Classic Squiffer
	2010: 'splatcharger',         # Splat Charger
	2011: 'splatcharger_collabo', # Firefin Splat Charger
	2015: 'herocharger_replica',  # Hero Charger Replica
	2020: 'splatscope',           # Splatterscope
	2021: 'splatscope_collabo',   # Firefin Splatterscope
	2030: 'liter4k',              # E-liter 4K
	2040: 'liter4k_scope',        # E-liter 4K Scope
	2060: 'soytuber',             # Goo Tuber
	3000: 'bucketslosher',        # Slosher
	3005: 'heroslosher_replica',  # Hero Slosher Replica
	3010: 'hissen',               # Tri-Slosher
	3020: 'screwslosher',         # Sloshing Machine
	4000: 'splatspinner',         # Mini Splatling
	4010: 'barrelspinner',        # Heavy Splatling
	4015: 'herospinner_replica',  # Hero Splatling Replica
	5000: 'sputtery',             # Dapple Dualies
	5010: 'maneuver',             # Splat Dualies
	5011: 'maneuver_collabo',     # Enperry Splat Dualies
	5015: 'heromaneuver_replica', # Hero Dualie Replicas
	5030: 'dualsweeper',          # Dualie Squelchers
	6000: 'parashelter',          # Splat Brella
	6005: 'heroshelter_replica'   # Hero Brella Replica
}

# Stage database
# https://app.splatoon2.nintendo.net/api/data/stages (needs auth)
stages = {
	0: 'battera',   # The Reef
	1: 'fujitsubo', # Musselforge Fitness
	2: 'gangaze',   # Starfish Mainstage
	3: 'chozame',   # Sturgeon Shipyard
	4: 'ama',       # Inkblot Art Academy
	5: 'combu',     # Humpback Pump Track
	6: 'manta',     # Manta Maria
	7: 'hokke',     # Port Mackerel
	8: 'tachiuo',   # Moray Towers
	9999: 'mystery' # Shifty Station (Splatfest only)
}

# Gear database
# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/gear.md
headgears = {
	1:     'white_headband',
	1000:  'urchins_cap',
	1001:  'lightweight_cap',
	1002:  'takoroka_mesh',
	# 1003:  'streetstyle_cap',
	# 1004:  'squid_stitch_cap',
	1005:  'squidvader_cap',
	1006:  'camo_mesh',
	1007:  'five_panel_cap',
	# 1008:  'zekko_mesh',
	1009:  'backwards_cap',
	# 1010:  'two_stripe_mesh',
	1014:  'cycle_king_cap',
	1019:  'king_flip_mesh',
	1020:  'hickory_work_cap',
	1023:  'jellyvader_cap',
	2000:  'bobble_hat',
	# 2001:  'short_beanie',
	2002:  'striped_beanie',
	# 2003:  'sporty_bobble_hat',
	2004:  'special_forces_beret',
	# 2005:  'squid_nordic',
	2009:  'knitted_hat',
	2009:  'annaki_beret',
	3000:  'retro_specs',
	3002:  'pilot_goggles',
	3003:  'tinted_shades',
	3005:  'snorkel_mask',
	3007:  'fake_contacts',
	3008:  '18k_aviators',
	3011:  'half_rim_glasses',
	4000:  'safari_hat',
	# 4001:  'jungle_hat',
	4002:  'camping_hat',
	4003:  'blowfish_bell_hat',
	4004:  'bamboo_hat',
	4005:  'straw_boater',
	# 4006:  'classic_straw_boater',
	# 4007:  'treasure_hunter',
	4008:  'bucket_hat',
	4009:  'patched_hat',
	5000:  'studio_headphones',
	# 5001:  'designer_headphones',
	5002:  'noise_cancelers',
	5003:  'squidfin_hook_cans',
	# 6000:  'golf_visor',
	6001:  'fishfry_visor',
	6002:  'sun_visor',
	6003:  'takoroka_visor',
	7000:  'bike_helmet',
	# 7002:  'stealth_goggles',
	# 7003:  'tentacles_helmet',
	# 7004:  'skate_helmet',
	7005:  'visor_skate_helmet',
	7006:  'mtb_helmet',
	7007:  'hockey_helmet',
	# 8000:  'gas_mask',
	8001:  'paintball_mask',
	# 8002:  'paisley_bandana',
	8003:  'skull_bandana',
	8004:  'painters_mask',
	8005:  'annaki_mask',
	8007:  'squid_facemask',
	8008:  'firefin_facemask',
	8009:  'king_facemask',
	# 9001:  'b_ball_headband',
	9002:  'squash_headband',
	9003:  'tennis_headband',
	# 9004:  'jogging_headband',
	9005:  'soccer_headband',
	21000: 'headlamp_helmet',
	25000: 'squid_hairclip',
	25001: 'samurai_helmet',
	25002: 'power_mask',
	25003: 'squid_clip_ons',
	25004: 'squinja_mask',
	25005: 'power_mask_mk_i',
	27000: 'hero_headset_replica',
	27004: 'armor_helmet_replica',
	27101: 'hero_headphones_replica'
}
clothes = {
	2:     'basic_tee',
	1000:  'white_tee',
	1001:  'black_squideye',
	1006:  'black_tee',
	1007:  'sunny_day_tee',
	1010:  'fugu_tee',
	1011:  'mint_tee',
	1013:  'red_vector_tee',
	1015:  'blue_peaks_tee',
	1019:  'sailor_stripe_tee',
	1020:  'white_8_bit_fishfry',
	1022:  'white_anchor_tee',
	1030:  'black_v_neck_tee',
	1031:  'white_deca_logo_tee',
	1032:  'half_sleeve_sweater',
	1033:  'king_jersey',
	1034:  'gray_8_bit_fishfry',
	1035:  'white_v_neck_tee',
	1036:  'white_urchin_rock_tee',
	1037:  'black_urchin_rock_tee',
	1038:  'wet_floor_band_tee',
	1039:  'squid_squad_band_tee',
	1040:  'navy_deca_logo_tee',
	1041:  'mister_shrug_tee',
	1042:  'chirpy_chips_band_tee',
	1043:  'hightide_era_band_tee',
	1044:  'red_v_neck_limited_tee',
	1045:  'green_v_neck_limited_tee',
	2001:  'black_ls',
	2002:  'purple_camo_ls',
	2003:  'navy_striped_ls',
	2004:  'zekko_baseball_ls',
	2007:  'white_baseball_ls',
	2013:  'pink_easy_stripe_shirt',
	2014:  'inkopolis_squaps_jersey',
	2015:  'annaki_drive_tee',
	2016:  'lime_easy_stripe_shirt',
	2017:  'annaki_evolution_tee',
	3001:  'yellow_layered_ls',
	3004:  'zink_layered_ls',
	3005:  'layered_anchor_ls',
	3006:  'choco_layered_ls',
	3008:  'layered_vector_ls',
	3009:  'green_tee',
	3010:  'red_tentatek_tee',
	3011:  'blue_tentatek_tee',
	4000:  'shrimp_pink_polo',
	4006:  'cycle_king_jersey',
	4007:  'slipstream_united',
	4008:  'fc_albacore',
	5002:  'berry_ski_jacket',
	5003:  'varsity_jacket',
	5006:  'black_inky_rider',
	5007:  'white_inky_rider',
	5012:  'blue_sailor_suit',
	5014:  'squid_satin_jacket',
	5017:  'chilly_mountain_coat',
	5018:  'takoroka_windcrusher',
	5019:  'matcha_down_jacket',
	5020:  'fa_01_jacket',
	5021:  'fa_01_reversed',
	5022:  'pullover_coat',
	5024:  'birded_corduroy_jacket',
	5026:  'zekko_redleaf_coat',
	5027:  'eggplant_mountain_coat',
	5028:  'zekko_jade_coat',
	5030:  'brown_fa_11_bomber',
	5031:  'gray_fa_11_bomber',
	6001:  'b_ball_jersey_away',
	6003:  'white_king_tank',
	6004:  'slash_king_tank',
	6005:  'navy_king_tank',
	7002:  'retro_sweat',
	7005:  'reel_sweat',
	7006:  'anchor_sweat',
	7007:  'negative_longcuff_sweater',
	7008:  'short_knit_layers',
	7009:  'positive_longcuff_sweater',
	8002:  'green_check_shirt',
	8004:  'urchins_jersey',
	8007:  'baby_jelly_shirt',
	8010:  'vintage_check_shirt',
	8012:  'logo_aloha_shirt',
	8015:  'shirt_and_tie',
	8017:  'hula_punk_shirt',
	8018:  'octobowler_shirt',
	8019:  'inkfall_shirt',
	8020:  'crimson_parashooter',
	8021:  'baby_jelly_shirt_and_tie',
	8022:  'prune_parashooter',
	9002:  'dark_urban_vest',
	9003:  'yellow_urban_vest',
	10000: 'camo_zip_hoodie',
	10002: 'zekko_hoodie',
	10004: 'shirt_with_blue_hoodie',
	10005: 'grape_hoodie',
	10006: 'gray_hoodie',
	21000: 'squiddor_polo',
	21001: 'anchor_life_vest',
	# 21002: 'juice_parka',
	25000: 'school_uniform',
	25001: 'samurai_jacket',
	25002: 'power_armor',
	25003: 'school_cardigan',
	25004: 'squinja_suit',
	25005: 'power_armor_mk_i',
	26000: 'splatfest_tee',
	27000: 'hero_jacket_replica',
	27004: 'armor_jacket_replica',
	27101: 'hero_hoodie_replica'
	# octoling_armor
}
shoes = {
	1:     'cream_basics',
	1003:  'white_seahorses',
	1008:  'strapping_whites',
	1009:  'strapping_reds',
	1011:  'le_soccer_shoes',
	1012:  'sunny_climbing_shoes',
	1013:  'birch_climbing_shoes',
	2000:  'red_hi_horses',
	2003:  'purple_hi_horses',
	2004:  'hunter_hi_tops',
	2006:  'gold_hi_horses',
	2009:  'mawcasins',
	2011:  'mint_dakroniks',
	2012:  'black_dakroniks',
	2013:  'piranha_moccasins',
	2014:  'white_norimaki_750s',
	2015:  'black_norimaki_750s',
	2016:  'sunset_orca_hi_tops',
	2017:  'red_and_black_squidkid_iv',
	2018:  'blue_and_black_squidkid_iv',
	2019:  'gray_sea_slug_hi_tops',
	2020:  'orca_hi_tops',
	3000:  'pink_trainers',
	3001:  'orange_arrows',
	3002:  'neon_sea_slugs',
	3007:  'purple_sea_slugs',
	3008:  'crazy_arrows',
	3009:  'black_trainers',
	3011:  'canary_trainers',
	3012:  'yellow_mesh_sneakers',
	3013:  'arrow_pull_ons',
	3014:  'red_mesh_sneakers',
	4000:  'oyster_clogs',
	4001:  'choco_clogs',
	4002:  'blueberry_casuals',
	4003:  'plum_casuals',
	4007:  'neon_delta_straps',
	4008:  'black_flip_flops',
	4009:  'snow_delta_straps',
	5000:  'trail_boots',
	5002:  'pro_trail_boots',
	6000:  'moto_boots',
	6003:  'blue_moto_boots',
	6005:  'acerola_rain_boots',
	6006:  'punk_whites',
	6012:  'hunting_boots',
	6013:  'punk_blacks',
	7000:  'blue_slip_ons',
	8000:  'white_kicks',
	8001:  'cherry_kicks',
	8004:  'roasted_brogues',
	8005:  'kid_clams',
	8006:  'smoky_wingtips',
	25000: 'school_shoes',
	25001: 'samurai_shoes',
	25002: 'power_boots',
	25003: 'fringed_loafers',
	25004: 'squinja_boots',
	25005: 'power_boots_mk_i',
	27000: 'hero_runner_replicas',
	27004: 'armor_boot_replicas',
	27101: 'hero_snowboots_replicas'
	# octoling_boots
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

# Colors for the profile image's background
profile_colors = {
	0: 'pink',
	1: 'green',
	2: 'yellow',
	3: 'purple',
	4: 'blue',
	5: 'sun-yellow'
}

# Splatfest ranks
fest_ranks = {
	0: 'fanboy',
	1: 'fiend',
	2: 'defender',
	3: 'champion',
	4: 'king'
}