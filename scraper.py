

import json
from http import cookiejar
import urllib.request, urllib.parse

def get_today():
  res = urllib.request.urlopen("https://dirtrally2.dirtgame.com/api/Challenge/Community")
  decoded = res.read().decode()
  daily_data = json.loads(decoded)[0]

  todays_challenges = []

  for each_challenge in daily_data['challengeGroups'][0]["challenges"]:
    if (each_challenge["events"][0]["discipline"] == "eRally"):
      c = {
        "vehicle_class": each_challenge["vehicleClass"],
        "country": each_challenge["events"][0]["stages"][0]["country"],
        "stage": each_challenge["events"][0]["stages"][0]["name"] if (each_challenge["events"][0]["discipline"] == "eRally") else each_challenge["events"][0]["stages"][0]["location"],
      }
      todays_challenges.append(c)

  return todays_challenges
  # end of get_today()

def get_challenges(days_ago):
  res = urllib.request.urlopen("https://dirtrally2.dirtgame.com/api/Challenge/Community")
  # print(res)
  decoded = res.read().decode()
  daily_data = json.loads(decoded)[0]

  list_of_challenges = []

  for each_challenge in daily_data['challengeGroups'][days_ago]["challenges"]:
    if (each_challenge["events"][0]["discipline"] == "eRally"):
      c = {
        # these values go to the database
        "id": each_challenge["id"],
        "start": each_challenge["entryWindow"]["start"],
        "end": each_challenge["entryWindow"]["end"],
        # "discipline": each_challenge["events"][0]["discipline"],
        "country": each_challenge["events"][0]["stages"][0]["country"],
        "stage": each_challenge["events"][0]["stages"][0]["name"] if (each_challenge["events"][0]["discipline"] == "eRally") else each_challenge["events"][0]["stages"][0]["location"],
        "vehicle_class": each_challenge["vehicleClass"],
        # these values go to the leaderboard query
        "event_id": each_challenge["events"][0]["id"],
        "stage_id": each_challenge["events"][0]["stages"][0]["id"]
      }
      list_of_challenges.append(c)

  return list_of_challenges
  # end of get_challenges()

def get_score(entry):
  time = entry["stageTime"]
  time_split = time.split(":")
  time = float(time_split[0]) * 60 + float(time_split[1])

  diff = entry["stageDiff"]
  if diff == "--":
    diff = 0
  else:
    diff_split = diff.strip("+").split(":")
    diff = float(diff_split[0]) * 60 + float(diff_split[1])
  
  score = float(int((1-(diff/(time-diff))) * 10000)/100)
  return score

def get_leaderboards(list_of_challenges):
  def get_page(c, page):

    data = json.dumps({"challengeId": c["id"],
      "eventId": c["event_id"],
      "stageId": c["stage_id"],
      "orderByTotalTime": True,
      "page": page,
      "pageSize": 100
    })

    request = urllib.request.Request(
      "https://dirtrally2.dirtgame.com/api/Leaderboard",
      data = data.encode(),
      headers = headers
    )

    res = urllib.request.urlopen(request)
    return json.loads(res.read().decode())
    # end of get_page()

  # set up CookieJar for the session
  cj = cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  opener.addheaders.pop(0)
  urllib.request.install_opener(opener) # this opener will be used for all further calls to urlopen()

  # get the Token to pass in the header
  with urllib.request.urlopen("https://dirtrally2.dirtgame.com/api/ClientStore/GetInitialState") as res:
    decoded = res.read().decode()
    token = json.loads(decoded)["identity"]["token"]
    
  headers = {
    "RaceNet.XSRFH": token,
    "Content-Type": "application/json"
    }

  # prepare empty end product
  list_of_entries = []

  for c in list_of_challenges:

    # do page 1 and get number of pages
    first_leaderboard = get_page(c, 1)
    for entry in first_leaderboard["entries"]:
      score = get_score(entry)
      entry_details = (c["id"], entry["rank"], entry["name"], entry["nationality"], entry["vehicleName"], entry["stageTime"], entry["stageDiff"], entry["isDnfEntry"], score)
      list_of_entries.append(entry_details)

    pages = first_leaderboard['pageCount']
    # print("Challenge #{}: Reading {} pages...".format(c["id"], pages))

    # run it again for each page
    for i in range(2, pages+1): # +1 to include max
      leaderboard = get_page(c, i)
      for entry in leaderboard["entries"]:
        score = get_score(entry)
        entry_details = (c["id"], entry["rank"], entry["name"], entry["nationality"], entry["vehicleName"], entry["stageTime"], entry["stageDiff"], entry["isDnfEntry"], score)
        list_of_entries.append(entry_details)
  
  # print("{} entries created".format(len(list_of_entries)))
  return list_of_entries
  # end of get_leaderboards()