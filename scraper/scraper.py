# import json
import requests # can't run on Hostgator

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

# calls the above function
# list_of_challenges = get_challenges(3) # get challenges from three days ago, in form of Challenge objects


def get_leaderboards(list_of_challenges):
  session = requests.Session()
  token = session.get(
      "https://dirtrally2.dirtgame.com/api/ClientStore/GetInitialState"
  ).json()["identity"]["token"]

  print("Scraping leaderboards...")

  # returns JSON object of 100 entries
  def get_one_leaderboard(c, page):
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
      print(f"Reading page {i} of {pages}")
      leaderboard = get_one_leaderboard(c, i)
      for entry in leaderboard["entries"]:
        entry_details = (c["id"], entry["rank"], entry["name"], entry["nationality"], entry["vehicleName"], entry["stageTime"], entry["stageDiff"], entry["isDnfEntry"])
        list_of_entries.append(entry_details)
  
  print(f"{len(list_of_entries)} entries created")
  return list_of_entries