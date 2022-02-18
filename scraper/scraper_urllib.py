
import json
from pprint import pprint
from http import cookiejar
import urllib.request, urllib.parse


def get_challenges(days_ago):
  print("Scraping challenges...")
  res = urllib.request.urlopen("https://dirtrally2.dirtgame.com/api/Challenge/Community")
  print(res)
  decoded = res.read().decode()
  daily_data = json.loads(decoded)[0]
  print(daily_data["typeName"])

  list_of_challenges = []

  for each_challenge in daily_data['challengeGroups'][days_ago]["challenges"]:
    if (each_challenge["events"][0]["discipline"] == "eRally"):
      c = {
        # these values go to the database
        "id": each_challenge["id"],
        "start": each_challenge["entryWindow"]["start"],
        "end": each_challenge["entryWindow"]["end"],
        # "discipline": each_challenge["events"][0]["discipline"],
        "stage": each_challenge["events"][0]["stages"][0]["name"] if (each_challenge["events"][0]["discipline"] == "eRally") else each_challenge["events"][0]["stages"][0]["location"],
        "vehicle_class": each_challenge["vehicleClass"],
        # these values go to the leaderboard query
        "event_id": each_challenge["events"][0]["id"],
        "stage_id": each_challenge["events"][0]["stages"][0]["id"]
      }
      list_of_challenges.append(c)

  return list_of_challenges

list_of_challenges = get_challenges(1)


cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders.pop(0)
urllib.request.install_opener(opener) # this opener will be used for all further calls to urlopen()



# session = requests.Session()
with urllib.request.urlopen("https://dirtrally2.dirtgame.com/api/ClientStore/GetInitialState") as res:
  decoded = res.read().decode()
  token = json.loads(decoded)["identity"]["token"]



for c in list_of_challenges:
  print(c["id"])

  url = "https://dirtrally2.dirtgame.com/api/Leaderboard"

  # this URL query string needs to be BYTES
  data = urllib.parse.urlencode({"challengeId": c["id"],
    "eventId": c["event_id"],
    "stageId": c["stage_id"],
    "orderByTotalTime": True,
    "page": 1, # change to parameter once function is working
    "pageSize": 10 # change to 100 "
    })
  
  headers = {"RaceNet.XSRFH": token}

  request = urllib.request.Request(
    url,
    data=data.encode(),
    headers=headers
    )

  urllib.request.urlopen(request)


  # with urllib.request.urlopen("https://dirtrally2.dirtgame.com/api/Leaderboard",
  #   json={ # TODO: error here, not expecting 'json'
  #       # 'c' properties refer to ones created in the each_challenge for loop
  #       "challengeId": c["id"],
  #       "eventId": c["event_id"],
  #       "stageId": c["stage_id"],
  #       "orderByTotalTime": True,
  #       "page": 1, # change to parameter once function is working
  #       "pageSize": 10, # change to 100 "
  #   },
  #   headers={"RaceNet.XSRFH": token}) as res:



  # req = urllib.request.Request(
  #   "https://dirtrally2.dirtgame.com/api/Leaderboard",
  #   json.dumps(json_post).encode(),
  #   headers={"RaceNet.XSRFH": token}
  #   )



def get_leaderboards(list_of_challenges):
  # TODO: another GET=>JSON request, this time with a session
  session = requests.Session()
  token = session.get(
      "https://dirtrally2.dirtgame.com/api/ClientStore/GetInitialState"
  ).json()["identity"]["token"]

  print("Scraping leaderboards...")

  # returns JSON object of 100 entries
  def get_one_leaderboard(c, page):
    # TODO: a POST request with a JSON parameter
    return session.post(
        "https://dirtrally2.dirtgame.com/api/Leaderboard",
        json={
            "challengeId": c["id"], # these vars refer to ones created in the each_challenge for loop
            "eventId": c["event_id"],
            "stageId": c["stage_id"],
            "orderByTotalTime": True,
            "page": page,
            "pageSize": 100,
        },
        headers={"RaceNet.XSRFH": token},
    ).json()
  
  list_of_entries = []

  for c in list_of_challenges:

    # scrape page 1
    first_leaderboard = get_one_leaderboard(c, 1)
    for entry in first_leaderboard["entries"]:
      entry_details = (c["id"], entry["rank"], entry["name"], entry["nationality"], entry["vehicleName"], entry["stageTime"], entry["stageDiff"], entry["isDnfEntry"])
      list_of_entries.append(entry_details)

    # now we know how many pages there are
    pages = first_leaderboard['pageCount']

    # run it again for each page
    for i in range(2, pages+1): # +1 to include max
      print("Reading page {} of {}".format(i, pages))
      leaderboard = get_one_leaderboard(c, i)
      for entry in leaderboard["entries"]:
        entry_details = (c["id"], entry["rank"], entry["name"], entry["nationality"], entry["vehicleName"], entry["stageTime"], entry["stageDiff"], entry["isDnfEntry"])
        list_of_entries.append(entry_details)
  
  print("{} entries created".format(len(list_of_entries)))
  return list_of_entries