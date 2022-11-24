import pandas as pd
import pickle
import json

predict_list = json.load(open('/tmp/fifa/odds.json', 'r'))

last_match_data = pd.read_csv('/tmp/fifa/last_match.csv')


model = pickle.load(open('/tmp/fifa/model.pkl', 'rb'))

random_seed = -1


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


results = []
for data in predict_list:
    home_team = data['home_team']
    away_team = data['away_team']
    result = predict(home_team, away_team, data['no_draw'])
    result.update(data)
    results.append(result)

result_df = pd.DataFrame(results)

print(result_df)
result_df.to_csv('/tmp/fifa/today_result.csv', index=False)
