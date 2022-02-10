import json, sys
import scraper # can't run on Hostgator


days_ago = int(sys.argv[1]) # 0 would be 'main.py'
# days_ago = 1


# scrape the source website
challenges = scraper.get_challenges(days_ago)
leaderboards = scraper.get_leaderboards(challenges)


# generate .json files
date = challenges[0]["start"][0:10]

with open(f"challenges_{date}.json", "w") as f:
  json.dump(challenges, f)

with open(f"leaderboards_{date}.json", "w") as f:
  json.dump(leaderboards, f)