# (hopefully) temporary file to bridge gap now that i'm switching from inserting yesterdays challenges+results to inserting todays challenges + yesterdays results

import json, subprocess, sys
import scraper

today = scraper.get_challenges(0)

with open("dr2-data/challenges_{}.json".format(today[0]["start"][0:10]), "w") as f:
  json.dump(today, f)


subprocess.call('php /home2/niemann8/dr2-data/insert.php', shell=True)