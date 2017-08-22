# splatnet2statink.py

A script that uploads JSON data from the SplatNet 2 app ("Nintendo Switch Online," for use with *Splatoon 2*) to [http://stat.ink/](http://stat.ink/), a site for visualizing and aggregating statistics from *Splatoon* and *Splatoon 2*.

## Usage
```
$ python splatnet2statink.py [-M] [-i path/to/results.json] [-t] [-p]
```

The `-M` flag runs the script in realtime monitoring mode, uploading new battle results as you play games.

The `-i` flag allows users to specify the path to a JSON file to be used as input. Without this, the file is pulled from [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results), given a valid cookie.

The `-t` flag sends the data to stat.ink as a dry run, without uploading, for testing/validation purposes.

The `-p` flag suppresses uploading the battle number as a private note.

## Working features
- [x] Lobby/Mode, Stage, Weapon
- [x] Result, final count/percent, turf inked
- [x] Kills, deaths, assists, specials
- [x] Rank & rank after, level & level after
- [x] Battle start & end times
- [x] Splatfest title & power
- [x] Scoreboard stats & player ranking
- [x] Monitoring for new battles/updates in real-time
- [x] Cookie generation using user's session token (must be manually acquired for now)
- [x] Non-English language game support

## To implement
- [ ] Gear + ability recognition (waiting on stat.ink API v2)
- [ ] Full automation of SplatNet cookie generation/acquisition, e.g. via user log-in

## Setup instructions

Download the script and change the `API_KEY`, and `SESSION_TOKEN` variables at the top.

### Obtaining your SplatNet cookie and session token

1. Run Login.py to generate your `SESSION_TOKEN`

### Obtaining your stat.ink API key

1. Viewable at [https://stat.ink/profile](https://stat.ink/profile) after [registering](https://stat.ink/register) and logging in.
