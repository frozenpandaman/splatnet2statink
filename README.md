# splatnet2statink.py

A script that works to upload JSON data from the SplatNet 2 app ("Nintendo Switch Online", for use with *Splatoon 2*) to [http://stat.ink/](http://stat.ink/), a site for visualizing and aggregating statistics from *Splatoon* and *Splatoon 2*.

## Usage
```
python splatnet2statink.py [-i /path/to/results.json]
```

If no input file is provided, the JSON is pulled from [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results), given your cookie.

## Working features
- [x] Lobby/Mode
- [x] Stage
- [x] Weapon
- [x] Result, final count/percent, turf inked
- [x] Kills, deaths, assists, specials
- [x] Rank + rank after, level + level after
- [x] Battle start & end times

## To implement
- [ ] Gear + ability recognition (waiting on stat.ink API v2)
- [ ] Splatfest support
- [ ] Private battles (partially)
- [ ] Automating SplatNet cookie generation/acquisition + JSON download
- [ ] Support for non-en_NA regions

## Setup instructions

### Getting your SplatNet cookie (manual – this process will hopefully be automated in the future)

1. Install the Python 3 package `mitmproxy`. For me this is `pip3 install mitmproxy` in Terminal.

2. Run `mitmweb`. Keep this browser tab open for later.

3. Find your computer's internal IP address (`ifconfig`/`ipconfig`, or on Mac, System Prefs > Network > Wi-Fi > Advanced… > TCP/IP > IPv4 Address) and your phone's (on Android, Settings > About phone > Status > IP address).

4. (Android) Settings > Wi-Fi > Long press to Modify network. Set Proxy to Manual under Advanced options. For proxy hostname, enter your computer's internal IP from before and enter the port as 8080.
(iOS) Follow [this guide](https://www.howtogeek.com/293676/how-to-configure-a-proxy-server-on-an-iphone-or-ipad/).

5. Go to [http://mitm.it/](http://mitm.it/) on your phone and download/install the certificate.

6. Open/log in to [SplatNet](https://play.google.com/store/apps/details?id=com.nintendo.znca&hl=en) on your phone. In the mitmweb tab that opened before, look for the line that says `https://app.splatoon2.nintendo.net/?lang=en-US`. Grab the `cookie` value (should be something like `iksm_session=xxxxx` where `xxxxx` is your cookie).

7. Navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) in your browser (shows a forbidden error for now). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the cookie/iksm_session cookie to be `xxxxx` from before. Refresh, and [ta-da](https://i.imgur.com/UUoxEJS.png)!

### Downloading the JSON

1. Save the webpage at [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results) as a JSON file after following the steps above.

### Getting your stat.ink API key

1. Viewable at [https://stat.ink/profile](https://stat.ink/profile) after [registering](https://stat.ink/register) and logging in.
