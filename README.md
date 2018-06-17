splatnet2statink
================

splatnet2statink is a script that uploads battle data from the SplatNet 2 app ("Nintendo Switch Online") to [https://stat.ink/](https://stat.ink/), a site for recording, visualizing, and aggregating statistics from *Splatoon* and *Splatoon 2*.

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

- [x] Full automation of SplatNet cookie generation/acquisition via user log-in
- [x] Complete battle stats
  - [x] Lobby/mode, stage, weapon
  - [x] Result, final count/percent, turf inked
  - [x] Kills, deaths, assists, specials
  - [x] Rank & rank after, level & level after, star levels (&#9733;), X Rank & Power
  - [x] Battle start & end times
  - [x] Ranked power level & league power
  - [x] Splatfest title, EXP & power
- [x] Gear/ability recognition, gear & user profile image upload, new Ver. 3.0 & Octo Expansion gear
- [x] Monitoring for new battle results in real-time
- [x] Scoreboard stats, player ranking & battle result image upload
- [x] Non-English language game support

## Setup instructions

1. Download and install [Python](https://www.python.org/downloads/). The script supports both Python 3.x and 2.7.x.

    If you're on macOS, Python 2.7 comes pre-installed. However, we recommend installing an updated version via [Homebrew](https://brew.sh/). Install Homebrew by running the command listed on the website, and then run `brew install python`.

2. Download the script from the command line (macOS: Terminal; Windows: Command Prompt/PowerShell) by running `git clone https://github.com/frozenpandaman/splatnet2statink.git` (requires [Git](https://git-scm.com/download), pre-installed on macOS), or use the green "Clone or download" button above.

3. Navigate to the newly-created directory (`cd splatnet2statink/`) and install the required Python libraries by running `pip install -r requirements.txt`.

    Note: Python 3.4+ and 2.7.9+, along with all Homebrew versions, automatically include pip. If you're on a lower version (check via `python --version`) or the above command doesn't work, install it from the [website](https://pip.pypa.io/en/stable/installing/), or by running `sudo easy_install pip` on macOS.

4. Running the script for the first time will prompt you to enter your stat.ink API key, which can be found in your [profile settings](https://stat.ink/profile). If you're using the app in a language other than English, you may enter your [language code](https://github.com/frozenpandaman/splatnet2statink/wiki/languages) (locale) as well.

**READ THE ENTIRETY OF THE "COOKIE GENERATION" SECTION BELOW BEFORE PROCEEDING. [→](#cookie-generation-important)**

5. You will then be asked to navigate to a specific URL on Nintendo.com, log in, and follow simple instructions to obtain your `session_token`; this will be used to generate an `iksm_session` cookie. If you are opting against automatic cookie generation, enter "skip" for this step, at which point you will be asked for your `iksm_session` cookie instead (see the [mitmproxy instructions](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions)).

    This token (used to access your SplatNet battle results) along with your stat.ink API key and language will automatically be saved into `config.txt` for you. You're now ready to upload battles!

Have any questions, issues, or suggestions? Feel free to message me on [Twitter](https://twitter.com/frozenpandaman) or [Reddit](https://www.reddit.com/user/frozenpandaman).

質問があれば、ツイッター([@frozenpandaman](https://twitter.com/frozenpandaman))で連絡してください。日本語OK。

### Accessing SplatNet 2 from your browser

If you wish to access SplatNet 2 from your computer rather than via the phone app, navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor – such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome – to change `iksm_session` to the value you obtained previously (automatically or via [mitmproxy](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions) – stored as  `cookie` in `config.txt`), and refresh the page. If you only want to access SplatNet and don't have a stat.ink API key, simply enter "skip" for this step during setup.

*Splatoon 2* stage rotation information (including Salmon Run) and current SplatNet gear are viewable at [https://splatoon2.ink/](https://splatoon2.ink/).

## Cookie generation (IMPORTANT)

For splatnet2statink to work, a cookie known as `iksm_session` is required to access SplatNet. This cookie may be obtained automatically, using the script, or manually via the app. Please read the following sections carefully to decide whether or not you want to use automatic cookie generation.

### Automatic

Automatic cookie generation involves making a **secure request to a _non-Nintendo server_ with minimal, non-identifying information**. We aim to be 100% transparent about this and provide in-depth information on security and privacy below. Users who feel uncomfortable with this may opt to manually acquire their cookie instead.

The v1.1.0 update to the Nintendo Switch Online app, released in September 2017, changed the method used to log in to Nintendo accounts, complicating the ability to generate cookies within the script. The update introduced the requirement of a [message authentication code](https://en.wikipedia.org/wiki/Message_authentication_code), known as `f`, to verify the authenticity of the login request.

This code is only able to be generated using a [key](https://en.wikipedia.org/wiki/Key_\(cryptography\)) provided within the app. However, this key is sensitive and, if revealed, may assist users looking to use it for malicious purposes. To prevent sharing this key publicly (e.g. distributing it in the script's source code), I've created a small API which will generate an `f` token given a valid input.

**_Privacy statement:_ No identifying information is ever sent to the API server. Usernames and passwords are far removed from where the API comes into play and are never readable by anyone but you. Returned `f` tokens  are never logged or stored and do not contain meaningful information. It is not possible to use either sent or stored data to identify which account/user performed a request, to view any identifying information about a user, or to gain access to an account.**

Please read the **[API documentation wiki page](https://github.com/frozenpandaman/splatnet2statink/wiki/api-docs)** for more information.

### Manual

Users who decide against automatic cookie generation via their computer may instead generate/retrieve `iksm_session` cookies from the SplatNet app.

In this case, users must obtain their cookie from their phone by intercepting their device's web traffic and inputting it into splatnet2statink when prompted (or manually inputting it into `config.txt`). Follow the [mitmproxy instructions](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions) to obtain and configure your cookie manually. To opt to manually acquire your cookie, enter "skip" when prompted to enter the "use this account" URL.

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
