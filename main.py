# /usr/bin/python3 /home2/niemann8/dr2-data/main.py 1

import json, subprocess, sys
import scraper, notify

days_ago = int(sys.argv[1]) # 0 would be 'main.py'
# days_ago = 1

try:
  today = scraper.get_challenges(0)
except:
  print("scraping today didn't work")

# try:
#   notify.notify(today)
# except:
#   print("notify didn't work")

# days_ago gives us a backdoor in case the source site is down one day
try:
  yesterday = scraper.get_challenges(days_ago)
  leaderboards = scraper.get_leaderboards(yesterday)
except:
  print("scraping yesterday didn't work")

try:
  # today's challenges
  with open("dr2-data/challenges_{}.json".format(today[0]["start"][0:10]), "w") as f:
    json.dump(today, f)
  # yesterday's results
  with open("dr2-data/leaderboards_{}.json".format(yesterday[0]["start"][0:10]), "w") as f:
    json.dump(leaderboards, f)
except:
  print("json dumping didn't work")

try:
  # call the PHP script to insert data into database
  subprocess.call('php /home2/niemann8/dr2-data/insert.php', shell=True)
except:
  print("calling PHP insert script didn't work")

try:
  # call the player update script
  subprocess.call('php /home2/niemann8/dr2-data/update_players.php', shell=True)
except:
  print("calling PHP player update script didn't work")