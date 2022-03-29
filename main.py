import json, subprocess, sys
import scraper, notify


days_ago = int(sys.argv[1]) # 0 would be 'main.py'
# days_ago = 1

today = scraper.get_challenges(0)
notify.notify(today)

# days_ago gives us a backdoor in case the source site is down one day
yesterday = scraper.get_challenges(days_ago)
leaderboards = scraper.get_leaderboards(yesterday)


# generate .json files
# today's challenges
with open("dr2-data/challenges_{}.json".format(today[0]["start"][0:10]), "w") as f:
  json.dump(today, f)
# yesterday's results
with open("dr2-data/leaderboards_{}.json".format(yesterday[0]["start"][0:10]), "w") as f:
  json.dump(leaderboards, f)


# call the PHP script to insert data into database
subprocess.call('php /home2/niemann8/dr2-data/insert.php', shell=True)