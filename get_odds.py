import json
import requests
from datetime import datetime


today = datetime.now().strftime("%Y-%m-%d")
today = "2022-11-25"

zh2en = {
    "卡塔尔": "Qatar",
    "德国": "Germany",
    "丹麦": "Denmark",
    "巴西": "Brazil",
    "法国": "France",
    "比利时": "Belgium",
    "克罗地亚": "Croatia",
    "西班牙": "Spain",
    "塞尔维亚": "Serbia",
    "英格兰": "England",
    "瑞士": "Switzerland",
    "荷兰": "Netherlands",
    "阿根廷": "Argentina",
    "伊朗": "IR Iran",
    "韩国": "Korea Republic",
    "日本": "Japan",
    "沙特阿拉伯": "Saudi Arabia",
    "厄瓜多尔": "Ecuador",
    "乌拉圭": "Uruguay",
    "加拿大": "Canada",
    "加纳": "Ghana",
    "塞内加尔": "Senegal",
    "葡萄牙": "Portugal",
    "波兰": "Poland",
    "突尼斯": "Tunisia",
    "摩洛哥": "Morocco",
    "喀麦隆": "Cameroon",
    "美国": "USA",
    "墨西哥": "Mexico",
    "威尔士": "Wales",
    "澳大利亚": "Australia",
    "哥斯达黎加": "Costa Rica",
}

match_type = "世界杯"

url = "https://webapi.sporttery.cn/gateway/jc/football/getMatchCalculatorV1.qry?poolCode=hhad,had&channel=c%20Request%20Method:%20GET"


match_info_list = requests.get(url).json()["value"]["matchInfoList"]

today_matches = [data for data in match_info_list if data["businessDate"]
                 == today][0]['subMatchList']

today_world_cup_matches = [
    match for match in today_matches if match["leagueAbbName"] == match_type]


datas = []


for today_world_cup_match in today_world_cup_matches:
    home_team_zh = today_world_cup_match["homeTeamAbbName"]
    away_team_zh = today_world_cup_match["awayTeamAbbName"]
    had = today_world_cup_match["had"]
    if not had:
        continue
    win_odds = had['h']
    lose_odds = had['a']
    draw_odds = had['d']

    home_team = zh2en[home_team_zh]
    away_team = zh2en[away_team_zh]

    data = {
        "Team1": home_team,
        "Team2": away_team,
        "win_odds": win_odds,
        "draw_odds": draw_odds,
        "lose_odds": lose_odds,
    }
    print(data)
    datas.append(data)


json.dump(datas, open("data/odds.json", "w"), indent=4)
