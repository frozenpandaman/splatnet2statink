splatnet2statink
================

splatnet2statink is a script that uploads battle data from the SplatNet 2 app ("Nintendo Switch Online") to [stat.ink](https://stat.ink/), a site for recording, visualizing, and aggregating statistics from *Splatoon* and *Splatoon 2*.

(ja) 日本語版セットアップ手順は[こちら](https://vanillasalt.net/2019/03/06/how-to-use-splatnet2statink/)。

(zh) 中文版的安装说明在[这里](https://cowlevel.net/article/1927016)。

## Usage

```
$ python splatnet2statink.py [-M [N]] [-r] [-s] [-t] [--x] [-e] [--de] [--salmon]
```

The `-M` flag runs the script in monitoring mode, uploading new battle results as you play matches. The script checks for new battles every `N` seconds; if no `N` is provided, the script defaults to 300 (5 minutes).

The `-r` flag uploads any recent battle records present on SplatNet 2 that haven't been uploaded to stat.ink.

The `-s` flag blacks out other players' names on the scoreboard result image and doesn't send them to stat.ink.

The `-t` flag sends battle data to stat.ink as a dry run, without uploading, for testing/validation purposes.

The `--x` flag can be combined with the above flags to export battle data to an excel file. Currently, for column consistancy, each team from battles on the same day should contain the same four members. Therefore, this flag is useful for exporting data during/ after a single league or private session.

The optional '-e' flag should only be combined with the '--x' flag to set the absolute folder path to which the results export to. For example: -e C:\Users\johnsmith

The optional `--de` flag should only be combined with the '--x' flag to set the export language to German.

The `--salmon` flag updates your Salmon Run profile and allows you to upload jobs (shifts) worked.

Note: You can also execute the script via `./splatnet2statink.py` on macOS and Linux. On Windows, use a backslash.

### Example usage

Running `python splatnet2statink.py -M 900` from the command line launches the script in monitoring mode, checking for and uploading battles every 15 minutes.

Running `python splatnet2statink.py --salmon -r` uploads all recent Salmon Run jobs not already present on stat.ink.

Running `python splatnet2statink.py -t --x -e C:\test -ct AA·' exports the battles to an Excel file under the given folder 'test'. It removes all name prefixes that match 'AA·' from the player names in the column headers.

## Features

- [x] Full automation of SplatNet cookie generation/acquisition via user log-in
- [x] Complete battle stats
  - [x] Gamemode, stage, weapon
  - [x] Result, final count/percent, turf inked
  - [x] Kills, deaths, assists, specials
  - [x] Rank, level & star emblems (&#9733;), X Rank & Power, weapon freshness
  - [x] Battle start & end times
  - [x] Ranked power level & League Power
  - [x] Splatfest support: Title, EXP, Power, Clout, Synergy Bonus, team nickname, win streak
  - [x] Species (Inkling or Octoling)
- [x] Gear/ability recognition, gear & user profile image upload
- [x] Monitoring for new battle results in real-time
- [x] Scoreboard stats, player ranking & battle result image upload
- [x] Salmon Run support – job details/stats & Grizzco Point Card
- [x] Full support for all available game languages
- [x] Limited export to excel files


## Setup instructions

*These instructions are meant to be accesssible and easy-to-follow for all users, and this is the recommended way to run the script. If you run into trouble, please reach out! However, an alternative [simple version](https://github.com/frozenpandaman/splatnet2statink/wiki/simple-setup-instructions) is also available.*

1. Download and install Python. On Windows, download the installer from the [official website](https://www.python.org/downloads/) and check the option during setup to add it to your PATH. On macOS, install [Homebrew](https://brew.sh/) and then run `brew install python`.

2. If you're on Windows, install [Git](https://git-scm.com/download) (pre-installed on macOS).

3. Download the script from the command line (macOS: Terminal; Windows: Command Prompt/PowerShell) by running `git clone https://github.com/radsutton/splatnet2statink.git`.

4. Navigate to the newly-created directory (`cd splatnet2statink/`) and install the required Python libraries by running `pip install -r requirements.txt`. On Windows, you may have to use `python -m pip` instead.

5. Running the script for the first time will prompt you to enter your stat.ink API key, which can be found in your [profile settings](https://stat.ink/profile). If you're using the app in a language other than English, you may enter your [language code](https://github.com/frozenpandaman/splatnet2statink/wiki/languages) (locale) as well.

**NOTE: Read the "Cookie generation" section below before proceeding. [→](#cookie-generation)**

6. You will then be asked to navigate to a specific URL on Nintendo.com, log in, and follow simple instructions to obtain your `session_token`; this will be used to generate an `iksm_session` cookie. If you are opting against automatic cookie generation, enter "skip" for this step, at which point you will be asked to manually input your `iksm_session` cookie instead (see the [mitmproxy instructions](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions)).

    This cookie (used to access your SplatNet battle results) along with your stat.ink API key and language will automatically be saved into `config.txt` for you. You're now ready to upload battles!
    
7. For easy Excel exports on Windows, copy the .cmd files to somewhere convenient like your desktop and replace USER with your Windows user.

Have any questions, issues, or suggestions? Feel free to message me on [Twitter](https://twitter.com/frozenpandaman) or create an [issue](https://github.com/frozenpandaman/splatnet2statink/issues) here.

質問があれば、ツイッター([@frozenpandaman](https://twitter.com/frozenpandaman))で連絡してください。日本語OK。

### Accessing SplatNet 2 from your browser

If you wish to access SplatNet 2 from your computer rather than via the phone app, navigate to [https://app.splatoon2.nintendo.net/home](https://app.splatoon2.nintendo.net/home) (it should show a forbidden error). Use a cookie editor – such as [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) for Chrome – to change `iksm_session` to the value you obtained previously (automatically or via [mitmproxy](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions), stored as  `cookie` in `config.txt`), and refresh the page. If you only want to access SplatNet and don't have a stat.ink API key, simply enter "skip" for this step during setup.

*Splatoon 2* stage rotation information (including Salmon Run) and current SplatNet gear are viewable at [splatoon2.ink](https://splatoon2.ink/).

---

## Cookie generation

For splatnet2statink to work, a cookie known as `iksm_session` is required to access SplatNet. This cookie may be obtained automatically, using the script, or manually via the app. Please read the following sections carefully to decide whether or not you want to use automatic cookie generation.

### Automatic

Automatic cookie generation involves making a *secure request to two non-Nintendo servers with minimal, non-identifying information*. We aim to be 100% transparent about this and provide in-depth information on security and privacy below. Users who feel uncomfortable with this may opt to manually acquire their cookie instead.

The v1.1.0 update to the Nintendo Switch Online app, released in September 2017, introduced the requirement of a [message authentication code](https://en.wikipedia.org/wiki/Message_authentication_code) (known as `f`), thereby complicating the ability to generate cookies within the script. After figuring out the [key](https://en.wikipedia.org/wiki/Key_\(cryptography\)) previously used to generate `f` tokens, the calculation method was changed in September 2018's v1.4.1 update, heavily obfuscating the new process. As a workaround, an Android server was set up to emulate the app, specifically to generate `f` tokens.

Generation now requires a [hash value](https://en.wikipedia.org/wiki/Hash_function) to further verify the authenticity of the request. The algorithm to calculate this, originally done within the app, is sensitive; to prevent sharing it publicly (i.e. distributing it in the script's source code), I've created a small [API](https://en.wikipedia.org/wiki/Application_programming_interface) which generates a hash value given a valid input. This can be passed to the Android server to generate the corresponding `f` token, which is then used to retrieve an `iksm_session` cookie.

**Privacy statement:** No identifying information is ever sent to the API server. Usernames and passwords are far removed from where the API comes into play and are never readable by anyone but you. Returned hash values are never logged or stored and do not contain meaningful information. It is not possible to use either sent or stored data to identify which account/user performed a request, to view any identifying information about a user, or to gain access to an account.

See the **[API documentation wiki page](https://github.com/frozenpandaman/splatnet2statink/wiki/api-docs)** for more information.

### Manual

Users who decide against automatic cookie generation via their computer may instead generate/retrieve `iksm_session` cookies from the SplatNet app.

In this case, users must obtain their cookie from their phone by intercepting their device's web traffic and inputting it into splatnet2statink when prompted (or manually adding it to `config.txt`). Follow the [mitmproxy instructions](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions) to obtain and configure your cookie manually. To opt to manually acquire your cookie, enter "skip" when prompted to enter the "Select this account" URL.

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
