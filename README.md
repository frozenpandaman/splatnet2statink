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
- [x] Cookie generation using user's session token
- [x] Non-English language game support
- [x] Full automation of SplatNet cookie generation/acquisition via user log-in

## To implement
- [ ] Gear + ability recognition (waiting on stat.ink API v2)

## Setup instructions

Change the `API_KEY` variable at the top of `splatnet2statink.py` to your stat.ink API key. You can also change `USER_LANG` to match your game's language.

When you run the script for the first time, it will prompt you to log in to your Nintendo Account to obtain your `session_token`. You may need to try logging in a few times if it doesn't work the first time. After the script returns your `session_token`, put it into `SESSION_TOKEN`, and run the script again to generate a cookie. Put the cookie into `YOUR_COOKIE`.

Once both of those values are set, you will be able to run the script normally and upload battle results to stat.ink.

### Using SplatNet 2 from your browser

If you want to access SplatNet 2 from your [browser](https://i.imgur.com/UUoxEJS.png), navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the `iksm_session` cookie to be the same value as `YOUR_COOKIE` from before, and refresh. If you wish to download the results JSON detailing your past 50 battles, save the webpage at [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results) as a JSON.

### Obtaining your stat.ink API key

Go to [https://stat.ink/profile](https://stat.ink/profile) after [registering](https://stat.ink/register) and logging in.
