import pandas as pd
import pickle
import json
from collections import Counter, defaultdict
import os
import numpy as np

schedule_df = pd.read_csv('/tmp/fifa/schedule.csv')
schedule_df['winner'] = None
random_seed = -1  # $PARAM:

base_groups = schedule_df['group'].copy()


last_match_data = pd.read_csv('/tmp/fifa/last_match.csv')

model = pickle.load(open('/tmp/fifa/model.pkl', 'rb'))


def predict(home_team, away_team, no_draw=True):
    home_team_data = last_match_data.loc[last_match_data['team']
                                         == home_team].iloc[0]
    away_team_data = last_match_data.loc[last_match_data['team']
                                         == away_team].iloc[0]
    data = {}

    data['rank_diff'] = 1.0 * \
        (home_team_data['fifa_rank'] -
         away_team_data['fifa_rank'])
    data['total_fifa_points'] = 1.0 * \
        (home_team_data['total_fifa_points'] -
         away_team_data['total_fifa_points'])
    data['goalkeeper_score_diff'] = home_team_data['goalkeeper_score'] - \
        away_team_data['goalkeeper_score']
    data['mean_defense_score_diff'] = home_team_data['mean_defense_score'] - \
        away_team_data['mean_defense_score']
    data['mean_offense_score_diff'] = home_team_data['mean_offense_score'] - \
        away_team_data['mean_offense_score']
    data['mean_midfield_score_diff'] = home_team_data['mean_midfield_score'] - \
        away_team_data['mean_midfield_score']

    predict_data = pd.DataFrame([data], index=[0])
    # [home team win prob, away team win prob]
    predict_proba = model.predict_proba(predict_data)[0].tolist()

    # [home team win prob, away team win prob, draw_proba]
    predict_proba.append(0)
    max_pro = max(predict_proba)

    result = {}
    # if win_pro < 0.55, we think it is draw
    if max_pro < 0.55 and not no_draw:
        result['win_team'] = 'draw'
        predict_proba[2] = 1

        # [home team win prob, away team win prob , draw prob]
        predict_proba = [x / sum(predict_proba) for x in predict_proba]
        result['draw_proba'] = round(predict_proba[2], 3)

    elif predict_proba.index(max_pro) == 1:
        result['win_team'] = home_team
    else:
        result['win_team'] = away_team

    result['win_proba'] = round(predict_proba[1], 3)
    result['lose_proba'] = round(predict_proba[0], 3)
    result['draw_proba'] = round(predict_proba[2], 3)

    if random_seed >= 0 and no_draw:
        predict_proba = [x / sum(predict_proba) for x in predict_proba]
        # np.random.seed(random_seed)
        win_team = np.random.choice(
            [away_team, home_team], p=predict_proba[:2])
        result['win_team'] = win_team

    result['home_team'] = home_team
    result['away_team'] = away_team

    print("\n" + "O" * 70, "\n")
    print(f"{home_team} vs {away_team}\n")
    print(home_team.ljust(15), "-" * 20, result['win_proba'])
    print("".ljust(35), "|")
    print("".ljust(35), "|", "-" * 10, result['win_team'])
    print("".ljust(35), "|")
    print(away_team.ljust(15), "-" * 20, result['lose_proba'])

    return result


def predict_group():
    results = []
    match_df = schedule_df[schedule_df["type"] == "group"]
    all_group_counter = defaultdict(Counter)
    for index, row in match_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        group_name = row['group']
        group_counter = all_group_counter[group_name]
        result = predict(home_team, away_team, no_draw=False)
        result['group'] = group_name
        results.append(result)
        if result['win_team'] == 'draw':
            group_counter[home_team] += 1
            group_counter[away_team] += 1
        else:
            group_counter[result['win_team']] += 3
        schedule_df['winner'].iloc[index] = result['win_team']

    results = pd.DataFrame(results)
    next_teams = []
    for group_name, group_counter in all_group_counter.items():
        first = group_counter.most_common(1)[0][0]
        second = group_counter.most_common(2)[1][0]

        schedule_df.replace("1"+group_name, first, inplace=True)
        schedule_df.replace("2"+group_name, second, inplace=True)
        next_teams.append(("1"+group_name, first))
        next_teams.append(("2"+group_name, second))

    schedule_df['group'] = base_groups

    return next_teams


def predict_knockout(knockout_tag):
    print()
    print("|"*100)
    print("match: ", knockout_tag)
    print()
    results = []
    match_df = schedule_df[schedule_df["type"] == knockout_tag]
    set_z1 = False
    next_teams = []
    for index, row in match_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        key = row['group']
        result = predict(home_team, away_team)
        result['group'] = key
        results.append(result)
        schedule_df['winner'].iloc[index] = result['win_team']
        schedule_df.replace(key, result['win_team'], inplace=True)
        next_teams.append((knockout_tag, result['win_team']))

        if knockout_tag == "semi-final":
            lose_team = home_team if result['win_team'] == away_team else away_team
            if not set_z1:
                schedule_df.replace("z1", lose_team, inplace=True)
                set_z1 = True
            else:
                schedule_df.replace("z2", lose_team, inplace=True)

    schedule_df['group'] = base_groups
    return next_teams


results_group = predict_group()
print("group results:")
print(results_group)

results_1_8 = predict_knockout("1/8")
print("1/8 results:")
print(results_1_8)

results_1_4 = predict_knockout("1/4")
print("1/4 results:")
print(results_1_4)

results_semi_final = predict_knockout("semi-final")
print("semi-final results:")
print(results_semi_final)

results_third_place = predict_knockout("play-off-for-third-place")
print("play-off-for-third-place results:")
print(results_third_place)


results_final = predict_knockout("final")
print("final results:")
print(results_final)


final_data = schedule_df[schedule_df["type"] == "final"].iloc[0]
third_place_data = schedule_df[schedule_df["type"]
                               == "play-off-for-third-place"].iloc[0]

no1 = final_data['winner']
list_final = [final_data['home_team'], final_data['away_team']]
list_final.remove(no1)
no2 = list_final[0]


no3 = third_place_data['winner']
list_third_place = [third_place_data['home_team'],
                    third_place_data['away_team']]
list_third_place.remove(no3)
no4 = list_third_place[0]


top4_result = {
    "no.1": no1,
    "no.2": no2,
    "no.3": no3,
    "no.4": no4
}

print(top4_result)


os.makedirs("/tmp/fifa/simulation/", exist_ok=True)

json.dump(top4_result, open(
    f'/tmp/fifa/simulation/top4_result_{random_seed}.json', "w"))

print()
print("The results of all the games")
print(schedule_df.to_string())
schedule_df.to_csv("/tmp/fifa/results.csv")
