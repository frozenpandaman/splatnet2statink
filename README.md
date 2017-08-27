# splatnet2statink.py

A script that uploads battle data from the SplatNet 2 app ("Nintendo Switch Online," for use with *Splatoon 2*) to [http://stat.ink/](http://stat.ink/), a site for visualizing and aggregating statistics from *Splatoon* and *Splatoon 2*.

## Usage
```
$ python splatnet2statink.py [-M] [-s] [-i path/to/results.json] [-t]
```

The `-M` flag runs the script in realtime monitoring mode, uploading new battle results as you play games.

The `-s` flag suppresses uploading the scoreboard result image. (stat.ink does not support blacking out other players' names at this time.)

The `-i` flag allows users to specify the path to a JSON file to be used as input. Without this, the file is pulled from [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results), given a valid cookie.

The `-t` flag sends the data to stat.ink as a dry run, without uploading, for testing/validation purposes.

## Working features
- [x] Complete battle stats
  - [x] Lobby/Mode, Stage, Weapon
  - [x] Result, final count/percent, turf inked
  - [x] Kills, deaths, assists, specials
  - [x] Rank & rank after, level & level after
  - [x] Battle start & end times
  - [x] Splatfest title & power
- [x] Monitoring for new battle results in real-time
- [x] Scoreboard stats & player ranking
- [x] Scoreboard/battle result image upload
- [x] Full automation of SplatNet cookie generation/acquisition via user log-in
- [x] Non-English language game support

## To implement
- [ ] Gear + ability recognition (waiting on stat.ink API v2)

## Setup instructions

1. Download and install [Python 2.7](https://www.python.org/downloads/) and the package manager [`pip`](https://pip.pypa.io/en/stable/installing/).

2. Install the required Python libraries:
```
pip install requests
pip install msgpack-python
```

3. Find your stat.ink API key on your [profile page](https://stat.ink/profile) and enter it into the `api_key` variable at the top of `config.txt`. You can change `user_lang` to match your game's [language](https://github.com/frozenpandaman/splatnet2statink/wiki/languages) as well.

4. Running the script for the first time will prompt you to navigate to a specific URL on Nintendo.com, log in, and follow simple instructions to obtain your `session_token`. This token will automatically be entered into `config.txt` for you, and a cookie will be generated.

### Accessing SplatNet 2 from your browser

If you wish to access SplatNet 2 from your browser, navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the `iksm_session` cookie to be the same value as `cookie` in `config.txt` (generated after running the script for the first time), and refresh.

*Splatoon 2* stage rotation information and current SplatNet gear are viewable at [https://splatoon2.ink/](https://splatoon2.ink/).

If you wish to download the results JSON detailing your past 50 battles (for use with the `-i` flag), save the webpage at [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results).