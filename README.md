# splatnet2statink

A script that uploads battle data from the SplatNet 2 app ("Nintendo Switch Online," for use with *Splatoon 2*) to [https://stat.ink/](https://stat.ink/), a site for recording, visualizing, and aggregating statistics from *Splatoon* and *Splatoon 2*.

(ja) 日本語版セットアップ手順は[こちら](https://archive.fo/td52p)。

(zh) 中文版的安装说明在[这里](https://cowlevel.net/article/1927016)。

## Usage

```
$ python splatnet2statink.py [-M [N]] [-r] [-s] [-t]
```

The `-M` flag runs the script in monitoring mode, uploading new battle results as you play matches. The script checks for new battles every `N` seconds; if no `N` is provided, the script defaults to 300 (5 minutes).

The `-r` flag uploads any recent battle records present on SplatNet 2 that haven't been uploaded to stat.ink.

The `-s` flag blacks out other players' names on the scoreboard result image and doesn't send them to stat.ink.

The `-t` flag sends the data to stat.ink as a dry run, without uploading, for testing/validation purposes.

Note: Executing the script via `./splatnet2statink.py` is also possible on macOS or Linux. If you've downloaded a .zip of this repository using the green "Clone or download" button above (instead of via `git clone`), the script must first be made executable by running `chmod +x splatnet2statink.py`.

### Example usage

Running `python splatnet2statink.py -M 900` from the command line launches the script in monitoring mode, checking for and uploading battles every 15 minutes.

## Features

- [x] Complete battle stats
  - [x] Lobby/mode, stage, weapon
  - [x] Result, final count/percent, turf inked
  - [x] Kills, deaths, assists, specials
  - [x] Rank & rank after, level & level after, star levels (&#9733;)
  - [x] Battle start & end times
  - [x] Ranked power level & league power
  - [x] Splatfest title, EXP & power
- [x] Gear + ability recognition
  - [x] New Ver. 2.0.0 gear
  - [x] Gear & user profile image upload
- [x] Monitoring for new battle results in real-time
- [x] Scoreboard stats, player ranking & battle result image upload
- [x] ~~Full automation of SplatNet cookie generation/acquisition via user log-in~~ ([more info](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions))
- [x] Non-English language game support

## Setup instructions

1. Download and install [Python](https://www.python.org/downloads/). The script supports both 2.7.x and 3.x.

    If you're on macOS, Python 2.7 comes pre-installed. However, we recommend installing an updated version via [Homebrew](https://brew.sh/). Install Homebrew by running the command listed on the website, and then run `brew install python`.

2. From the command line (macOS: Terminal; Windows: Command Prompt/PowerShell), install the required Python libraries:
    ```
    pip install requests
    pip install msgpack-python
    pip install future
    ```
    Python 2.7.9+ and 3.4+ automatically include pip. If you installed Python via Homebrew, you also already have pip. If you're on a lower version (check via `python --version`), install it from the [website](https://pip.pypa.io/en/stable/installing/), or by simply running `sudo easy_install pip` on macOS.

    If you'll be running splatnet2statink with the `-s` flag (to black out scoreboard names), run `pip install pillow` as well.

3. Download the script by running `git clone https://github.com/frozenpandaman/splatnet2statink.git` (requires [Git](https://git-scm.com/download), pre-installed on macOS), or use the green "Clone or download" button above.

4. Running the script for the first time will prompt you to enter your stat.ink API key, which can be found in your [profile settings](https://stat.ink/profile). If you're using the app in a language other than English, you may enter your [language code](https://github.com/frozenpandaman/splatnet2statink/wiki/languages) (locale) as well.

5. You will then be asked to enter your `iksm_session` token. To obtain it, follow the mitmproxy instructions [here](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions). This token (used to access your SplatNet battle results) along with your stat.ink API key and language will automatically be saved into `config.txt` for you. You're now ready to upload battles!

Have any questions, issues, or suggestions? Feel free to message me on [Twitter](https://twitter.com/frozenpandaman) or [Reddit](https://www.reddit.com/user/frozenpandaman).

質問があれば、ツイッター([@frozenpandaman](https://twitter.com/frozenpandaman))で連絡してください。日本語OK。

### Accessing SplatNet 2 from your browser

If you wish to access the SplatNet site from your computer rather than via the phone app, navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor (such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome) to change `iksm_session` to the value you obtained [previously](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions) (stored as  `cookie` in `config.txt`), and refresh the page. If you only wish to access SplatNet 2 and don't have a stat.ink API key, simply enter "skip" for this step during setup.

*Splatoon 2* stage rotation information (including Salmon Run) and current SplatNet gear are viewable at [https://splatoon2.ink/](https://splatoon2.ink/).

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
