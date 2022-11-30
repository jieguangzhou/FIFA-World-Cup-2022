import json
import requests

bet_date = "2022-12-01"  # $PARAM:

url = f"http://198.18.16.239:18000/get_odds/{bet_date}"

datas = requests.get(url).json()

print(datas)

json.dump(datas, open("/tmp/fifa/odds.json", "w"), indent=4)
