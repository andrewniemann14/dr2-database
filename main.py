import json, subprocess, sys
import scraper, notify


days_ago = int(sys.argv[1]) # 0 would be 'main.py'
# days_ago = 1

notify.notify(scraper.get_today())


# scrape the source website
challenges = scraper.get_challenges(days_ago)
leaderboards = scraper.get_leaderboards(challenges)


# generate .json files
date = challenges[0]["start"][0:10] # slice the date part of DateTime

with open("dr2-data/challenges_{}.json".format(date), "w") as f:
  json.dump(challenges, f)

with open("dr2-data/leaderboards_{}.json".format(date), "w") as f:
  json.dump(leaderboards, f)


# call the PHP script to insert data into database
subprocess.call('php /home2/niemann8/dr2-data/insert.php', shell=True)