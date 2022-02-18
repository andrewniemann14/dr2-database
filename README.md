# scraper:
Python program scrapes official website for challenge and leaderboard data, saves results to JSON files

'requests' library not allowed on Hostgator, so it has to be done locally and the JSON files FTP'd to the inserter
currently working on getting requests 1.0 (compat with Python 3.2) running, but unsuccessful so far
plan B is to use urllib, but session cookies will take some time to figure out


# inserter:
PHP program inserts JSON data into a MySQL database
