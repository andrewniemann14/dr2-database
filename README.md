DR2.0 Dashboard - data generator
=
This program automatically populates a database with DiRT Rally 2.0 daily challenge information. Will be used in a future project.

main.py runs on CPanel as a cron job  
Python is used to scrape https://dirtrally2.dirtgame.com/community-events for challenge and leaderboard data.
> Today's challenges are sent to my phone (not currently working, vwtext blocks as spam probably).  
> Yesterday's challenge and leaderboard data is saved as JSON.  

PHP is then used to read the JSON files and insert them into a MySQL database.

The only changes in the near future would be to get notifications working and then move them to a subscription model
