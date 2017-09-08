# splatnet2statink.py

A script that uploads battle data from the SplatNet 2 app ("Nintendo Switch Online," for use with *Splatoon 2*) to [http://stat.ink/](http://stat.ink/), a site for visualizing and aggregating statistics from *Splatoon* and *Splatoon 2*.

## Usage
```
$ python splatnet2statink.py [-M] [-s] [-i path/to/results.json] [-t]
```

The `-M` flag runs the script in realtime monitoring mode, uploading new battle results as you play games.

The `-s` flag suppresses uploading the scoreboard result image.

The `-i` flag allows users to specify the path to a results JSON file to be used as input. Without this, the file is pulled from [https://app.splatoon2.nintendo.net/api/results](https://app.splatoon2.nintendo.net/api/results), given a valid cookie.

The `-t` flag sends the data to stat.ink as a dry run, without uploading, for testing/validation purposes.

## Working features
- [x] Complete battle stats
  - [x] Lobby/mode, stage, weapon
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

1. Download and install [Python 2.7](https://www.python.org/downloads/) (pre-installed on macOS) and the package manager [pip](https://pip.pypa.io/en/stable/installing/).

2. From the command line (macOS: Terminal; Windows: Command Prompt/PowerShell), install the required Python libraries:
    ```
    pip install requests
    pip install msgpack-python
    ```
    If you're on Windows with multiple versions of Python installed, you'll have to use `py -2 -m pip` instead.

3. Running the script for the first time will prompt you to enter your stat.ink API key, which can be found in your [profile settings](https://stat.ink/profile). If you're using the app in a language other than English, you may choose choose to enter your [language code](https://github.com/frozenpandaman/splatnet2statink/wiki/languages) (locale) as well.

4. You will then be asked to navigate to a specific URL on Nintendo.com, log in, and follow simple instructions to obtain your `session_token`. This token, along with your stat.ink API key and language, will automatically be saved into `config.txt` for you, and a cookie (used to access your SplatNet battle results) will be generated. You're now ready to upload battles!

Have any questions, issues, or suggestions? Feel free to message me on [Twitter](https://twitter.com/frozenpandaman) or [Reddit](https://www.reddit.com/user/frozenpandaman).

### Accessing SplatNet 2 from your browser

If you wish to access the SplatNet site from your computer rather than via the phone app, navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the `iksm_session` cookie to be the same value as `cookie` in `config.txt` (generated after running the script for the first time), and refresh the page.

*Splatoon 2* stage rotation information (including Salmon Run) and current SplatNet gear are viewable at [https://splatoon2.ink/](https://splatoon2.ink/).

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)