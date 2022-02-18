import json, sys
import scraper


days_ago = int(sys.argv[1]) # 0 would be 'main.py'
# days_ago = 1


# scrape the source website
challenges = scraper.get_challenges(days_ago)
leaderboards = scraper.get_leaderboards(challenges)


# generate .json files
date = challenges[0]["start"][0:10] # slice the date part of DateTime

# this works, though they don't seem to show up in the FTP
with open("public_html/dr2insert/challenges_{}.json".format(date), "w") as f:
  json.dump(challenges, f)

with open("public_html/dr2insert/leaderboards_{}.json".format(date), "w") as f:
  json.dump(leaderboards, f)
