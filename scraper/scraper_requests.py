# import json
import os, sys

# Add vendor directory to module search path, to import from local source
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)
import requests


# returns list of challenge dictionaries, ready to pass to a SQL query to insert into the challenges table
def get_challenges(days_ago):

  print("Scraping challenges...")

  community_data = requests.get(
      "https://dirtrally2.dirtgame.com/api/Challenge/Community"
  ).json()

  daily_data = community_data[0]
  # weekly_data = community_data[1]
  # monthly_data = community_data[2]

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

def get_leaderboards(list_of_challenges):
  session = requests.Session()
  begin_session = session.get(
    "https://dirtrally2.dirtgame.com/api/ClientStore/GetInitialState"
  )
  
  token = begin_session.json()["identity"]["token"] # good
  
  print(begin_session.cookies.keys()) # TODO: this cookie is not getting passed in the requests down below
  print(begin_session)
  print(begin_session.cookies)

  print("Scraping leaderboards...")

  # returns JSON object of 100 entries
  def get_one_leaderboard(c, page):
    print(c) # good
    print(page) # good

    url = "https://dirtrally2.dirtgame.com/api/Leaderboard"

    data = {
      "challengeId": c["id"], # these vars refer to ones created in the each_challenge for loop
      "eventId": c["event_id"],
      "stageId": c["stage_id"],
      "orderByTotalTime": True,
      "page": page,
      "pageSize": 100,
    }

    headers = {
      "RaceNet.XSRFH": token,
      "Connection": "keep-alive",
      "Content-Type": "application/json",
      "User-Agent": "python-requests/1.0.0",
      "Accept-Encoding": "gzip, deflate"
    }

    cookies = begin_session.cookies


    res = session.post(
      url,
      data=data,
      headers=headers,
      cookies=cookies
    )
    print("res.request.headers:",res.request.headers)
    print("res:",res)
    print("res.headers:",res.headers)

    return res.json()
  
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



get_leaderboards(get_challenges(1))