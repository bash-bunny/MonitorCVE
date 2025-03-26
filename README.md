# CVE Monitoring

The [Shodan](https://shodan.io/) people has some free URLs to monitor CVEs. This is particularly useful if you are continuously looking for potential vulnerabilities or trying to maintain your organization updated or safe out there.

You can use the `https://cvedb.shodan.io/` API to search for free for CVEs, vulnerabilities exploited in the wild, and look for the CVEs for a particular technology, awesome!

## Installation

Clone the repo first:

```bash
git clone https://github.com/bash-bunny/MonitorCVE.git
cd MonitorCVE
```

Install the requirements and you are good to go:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Configuration

This is a bot for Telegram, so you need to create a bot with [BotFather](https://telegram.me/BotFather).

Then copy the `bot_id` into the script part that says: `bot = telebot.TeleBot("[bot-id-here]")`, and you're good to go.

## Usage

The script runs indefinitely until stopped or the machine that run it stops. To avoid having to launch it manually you can create a `cronjob` with a bash script that runs in the background the telegram bot. Or you can adapt the script (is python, so it's easy to change it), and run it locally with out the need of telegram, that's up to you.

To run it as a bot:

- Inside the virtual environment run: `python3 cve_monitoring_tele.py`

The terminal hang on, and you can start to send commands to your bot.

### Commands

```bash
/cves - For a file with the last cves
/cve CVE-ID - For the data for a particular CVE
/known - For a file with the known CVEs that are exploiting right now
/product <Product_Name> - For a file with all the CVEs for a particular product
```

## Extra

To configure as a `cronjob`.

- Create the following script

```bash
#!/bin/bash
cd /path/to/your/python/script.py
. venv/bin/activate
nohup python cve_monitoring_tele.py &>/dev/null &
```

- Create the `cronjob` with `crontab -e`

```bash
@reboot /usr/bin/bash /path/to/your/bash/script.sh
```

- Execute the `cron` service, that depends on your init system.

```bash
# For systemctl
sudo systemctl enable cron
sudo systemctl start cron

# For openrc
sudo rc-update add cronie default
sudo rc-service cronie start
```