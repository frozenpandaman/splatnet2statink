# splatnet2statink.py

A script that uploads JSON data from the SplatNet 2 app ("Nintendo Switch Online", for use with *Splatoon 2*) to [http://stat.ink/](http://stat.ink/), a site for visualizing and aggregating statistics from *Splatoon* and *Splatoon 2*.

## Usage
```
$ python splatnet2statink.py [-i path/to/results.json] [-p]
```

If no input file (`-i`) is provided, the JSON is pulled from [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results), given your cookie.

The `-p` flag suppresses uploading the battle number as a private note.

## Working features
- [x] Lobby/Mode
- [x] Stage
- [x] Weapon
- [x] Result, final count/percent, turf inked
- [x] Kills, deaths, assists, specials
- [x] Rank & rank after, level & level after
- [x] Battle start & end times
- [x] Splatfest title & power
- [x] Scoreboard stats & player ranking
- [x] Non-English language game support

## To implement
- [ ] Gear + ability recognition (waiting on stat.ink API v2)
- [ ] Automating SplatNet cookie generation/acquisition, e.g. via user log-in (partially implemented using user's session token from app)
- [ ] Monitoring for new battles/updates in real-time

## Setup instructions

Download the script and put your stat.ink API key into the `API_KEY` variable at the top of splatnet2statink.py. In iksm.py, put your session token into the `SESSION_TOKEN` variable.

### Getting your SplatNet cookie and session token (manual – this process will hopefully be automated in the future)

1. Install the Python 3 package `mitmproxy`. For me this is `pip3 install mitmproxy` in Terminal. (Python 3 can be installed via [Homebrew](https://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/).)

2. Run `mitmweb`. Keep this browser tab open for later.

3. Find your computer's internal IP address (`ifconfig`/`ipconfig`, or on Mac, System Prefs > Network > Wi-Fi > Advanced… > TCP/IP > IPv4 Address) and your phone's (on Android, Settings > About phone > Status > IP address).

4. (Android) Settings > Wi-Fi > long press to Modify network. Set Proxy to Manual under Advanced options. For proxy hostname, enter your computer's internal IP from before and enter the port as 8080.  
(iOS) Follow [this guide](https://www.howtogeek.com/293676/how-to-configure-a-proxy-server-on-an-iphone-or-ipad/).

5. Go to [http://mitm.it/](http://mitm.it/) on your phone and download/install the certificate.

6. Open [SplatNet 2](https://play.google.com/store/apps/details?id=com.nintendo.znca&hl=en) on your phone. In the mitmweb tab that opened before, look for the line that says `https://app.splatoon2.nintendo.net/?lang=en-US`. Grab the `cookie` value from the Request tab (should be something like `iksm_session=xxxxx` where `xxxxx` is your cookie). This cookie can be used to access SplatNet 2 from your browser.  
For the session token, look for `https://accounts.nintendo.com/connect/1.0.0/api/token`, and there will be a `session_token` in the Request tab. It will start with `eyJhbGciOiJIUzI1NiJ9`, followed by a period `.`, then a long series of characters. This is used by the script to generate cookies without having to run the app through mitmproxy every time a cookie expires.

7. Navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) in your browser (shows a forbidden error for now). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the `iksm_session` cookie to be `xxxxx` from before. Refresh, and you should be able to access SplatNet 2 from your [browser](https://i.imgur.com/UUoxEJS.png).

### Getting your stat.ink API key

1. Viewable at [https://stat.ink/profile](https://stat.ink/profile) after [registering](https://stat.ink/register) and logging in.

### Downloading the JSON

1. Save the webpage at [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results) as a JSON file after following the steps above.