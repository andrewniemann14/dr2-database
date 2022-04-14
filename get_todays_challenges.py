# /usr/bin/python3 /home2/niemann8/dr2-data/main.py 1

import json, subprocess, sys
import scraper, notify

try:
  today = scraper.get_challenges(0)
except:
  print("scraping today didn't work")

try:
  notify.notify(today)
except:
  print("notify didn't work")

try:
  # today's challenges
  with open("dr2-data/challenges_{}.json".format(today[0]["start"][0:10]), "w") as f:
    json.dump(today, f)
except:
  print("json dumping didn't work")

try:
  # call the PHP script to insert data into database
  subprocess.call('php /home2/niemann8/dr2-data/insert.php', shell=True)
except:
  print("calling PHP insert script didn't work")