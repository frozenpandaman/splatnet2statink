# splatnet2statink.py

A script that uploads battle data from the SplatNet 2 app ("Nintendo Switch Online," for use with *Splatoon 2*) to [http://stat.ink/](http://stat.ink/), a site for visualizing and aggregating statistics from *Splatoon* and *Splatoon 2*.

## Usage

```
$ python splatnet2statink.py [-M [N]] [-r] [-s] [-t]
```

The `-M` flag runs the script in monitoring mode, uploading new battle results as you play games. The script checks for new battles every `N` seconds; if no `N` is provided, the script defaults to 300 (5 minutes).

The `-r` flag, for use with monitoring mode, checks to see if there are recent battle records present on SplatNet 2 that haven't been uploaded to stat.ink and, if so, posts them. 

The `-s` flag suppresses uploading the scoreboard result image.

The `-t` flag sends the data to stat.ink as a dry run, without uploading, for testing/validation purposes.

Note: Executing the script via `./splatnet2statink.py` is also possible on macOS or Linux. If you've downloaded this repository using the "Clone or download" button above (instead of via `git clone`), the script must first be made executable by running `chmod +x splatnet2statink.py`.

## Working features

- [x] Complete battle stats
  - [x] Lobby/mode, stage, weapon
  - [x] Result, final count/percent, turf inked
  - [x] Kills, deaths, assists, specials
  - [x] Rank & rank after, level & level after
  - [x] Battle start & end times
  - [x] Splatfest title & power
  - [x] Ranked power level & league power
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
    If you're on Windows with multiple versions of Python installed, you'll have to use `py -2 -m pip` instead. If the `py` command is not recognized, use `\Python27\python.exe \Python27\Scripts\pip.exe` (given you've installed Python 2.7 in the default directory).

3. Running the script for the first time will prompt you to enter your stat.ink API key, which can be found in your [profile settings](https://stat.ink/profile). If you're using the app in a language other than English, you may choose choose to enter your [language code](https://github.com/frozenpandaman/splatnet2statink/wiki/languages) (locale) as well.

4. ~~You will then be asked to navigate to a specific URL on Nintendo.com, log in, and follow simple instructions to obtain your `session_token`. This token, along with your stat.ink API key and language, will automatically be saved into `config.txt` for you, and a cookie (used to access your SplatNet battle results) will be generated. You're now ready to upload battles!~~

**UPDATE: The authentication process has changed in the 1.1.0 update to the Nintendo Switch Online app. Existing, non-expired cookies can still be used to run the script and access the site, but trying to generate a new cookie will now produce the message "Invalid token." We're working on a fix ASAP. For now, follow the mitmproxy instructions [here](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions).**

Have any questions, issues, or suggestions? Feel free to message me on [Twitter](https://twitter.com/frozenpandaman) or [Reddit](https://www.reddit.com/user/frozenpandaman).

日本語のセットアップ手順は[こちら](https://aqraf.com/archives/327)。質問があれば、ツイッター([@frozenpandaman](https://twitter.com/frozenpandaman))で連絡してください。日本語OK。

### Accessing SplatNet 2 from your browser

If you wish to access the SplatNet site from your computer rather than via the phone app, navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to edit the `iksm_session` cookie to be the same value as `cookie` in `config.txt` (generated after running the script for the first time), and refresh the page. If you only wish to access SplatNet 2 and don't have a stat.ink API key, simply enter "skip" for this step during setup.

*Splatoon 2* stage rotation information (including Salmon Run) and current SplatNet gear are viewable at [https://splatoon2.ink/](https://splatoon2.ink/).

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
