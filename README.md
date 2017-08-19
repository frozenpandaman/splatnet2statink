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

Download the script and change the `API_KEY`, `YOUR_COOKIE`, and `SESSION_TOKEN` variables at the top.

### Obtaining your SplatNet cookie and session token

1. Install the Python 3 package `mitmproxy`. For me this is `pip3 install mitmproxy` in Terminal. (Python 3 can be installed via [Homebrew](https://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/).)

2. Run `mitmweb`. Keep this browser tab open for later.

3. Find your computer's internal IP address (`ifconfig`/`ipconfig`, or on Mac, System Prefs > Network > Wi-Fi > Advanced… > TCP/IP > IPv4 Address) and your phone's (on Android, Settings > About phone > Status > IP address).

4. (Android) Settings > Wi-Fi > long press to Modify network. Set Proxy to Manual under Advanced options. For proxy hostname, enter your computer's internal IP from before and enter the port as 8080.  
(iOS) Follow [this guide](https://www.howtogeek.com/293676/how-to-configure-a-proxy-server-on-an-iphone-or-ipad/).

5. Go to [http://mitm.it/](http://mitm.it/) on your phone and download/install the certificate.

6. Open [Nintendo Switch Online](https://play.google.com/store/apps/details?id=com.nintendo.znca&hl=en) on your phone and log in if you have not done so previously. Click on "Splatoon 2" under "Game-Specific Services."

7. In the mitmweb tab that opened before, look for the line that says `https://app.splatoon2.nintendo.net/?lang=en-US`. Grab the `cookie` value from the Request tab (should be something like `iksm_session=xxxxx` where `xxxxx` is your cookie). This cookie can be used to access SplatNet 2 from your browser.

8. Look for the `session_token` value under `https://accounts.nintendo.com/connect/1.0.0/api/token`. It should begin with `eyJhbGciOiJIUzI1NiJ9.`. This value is long; make sure to copy it all. The script uses `session_token` to generate new `iksm_session` cookies once previous ones expire, eliminating the need to use mitmproxy in the future.

9. If you wish to access SplatNet 2 from your [browser](https://i.imgur.com/UUoxEJS.png), navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (shows a forbidden error for now). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the `iksm_session` cookie to be `xxxxx` from before, and refresh. If at any time you wish to download the results JSON listing your past 50 battles, save the webpage at [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results) as a JSON.

### Obtaining your stat.ink API key

1. Viewable at [https://stat.ink/profile](https://stat.ink/profile) after [registering](https://stat.ink/register) and logging in.