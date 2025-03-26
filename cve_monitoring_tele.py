import telebot
import requests
import json
import os

# Config
bot = telebot.TeleBot("[bot-id-here]")
url = "https://cvedb.shodan.io/"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'}
cves_file = "cves.json"
no_param = "No params you silly..."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Usage: /command\n\nCommands:\n /cves \n /known \n /cve <CVE_ID> \n /product <PRODUCT_NAME>")

@bot.message_handler(commands=['cve'])
def get_cve(message):
    # Get the cve ID
    user_input = message.text
    command, _, params = user_input.partition(' ')
    if(params):
        cve_url = url + "/cve/" + params
        r = requests.get(cve_url, headers=headers)
        cve_data = "No data found"
        if(r.status_code == 200):
            cve_json = json.loads(r.text)
            cve_data = ""
            cve_data += "CVE ID: " + cve_json['cve_id'] + "\n"
            cve_data += "Date: " + cve_json['published_time'] + "\n"
            cve_data += "CVSS: " + str(cve_json['cvss']) + "\n\n"
            cve_data += "Summary: " + cve_json['summary'] + "\n\n"
            cve_data += "References:\n"
            for ref in cve_json['references']:
                cve_data += ref + "\n"
        bot.reply_to(message, cve_data)
    else:
        bot.reply_to(message, no_param)

@bot.message_handler(commands=['cves'])
def get_cves(message):
    # Get the cve ID
    user_input = message.text
    cve_url = url + "/cves"
    r = requests.get(cve_url, headers=headers)
    data = "No data found"
    if(r.status_code == 200):
        data = r.text
        bot.reply_to(message, "List of last 1000 CVEs, enjoy!")
        with open(cves_file, "w") as f:
            f.write(data)
        with open(cves_file, "rb") as f:
            bot.send_document(message.chat.id, f)
        os.remove(cves_file)
    else:
        bot.reply_to(message, data)

@bot.message_handler(commands=['known'])
def get_cves(message):
    # Get the cve ID
    user_input = message.text
    cve_url = url + "/cves?is_kev=true"
    r = requests.get(cve_url, headers=headers)
    data = "No data found"
    if(r.status_code == 200):
        data = r.text
        bot.reply_to(message, "List of know exploited vulns, that could be fun :)")
        with open(cves_file, "w") as f:
            f.write(data)
        with open(cves_file, "rb") as f:
            bot.send_document(message.chat.id, f)
        os.remove(cves_file)
    else:
        bot.reply_to(message, data)

@bot.message_handler(commands=['product'])
def get_cve(message):
    # Get the cve ID
    user_input = message.text
    command, _, params = user_input.partition(' ')
    if(params):
        cve_url = url + "/cves?product=" + params
        r = requests.get(cve_url, headers=headers)
        data = "No data found"
        if(r.status_code == 200):
            bot.reply_to(message, "List of CVEs by product, are you looking for something in particular?\nYou naughty...")
            data = r.text
            with open(cves_file, "w") as f:
                f.write(data)
            with open(cves_file, "rb") as f:
                bot.send_document(message.chat.id, f)
            os.remove(cves_file)
        else:
            bot.reply_to(message, data)
    else:
        bot.reply_to(message, no_param)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()

