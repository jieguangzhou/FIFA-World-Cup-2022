import pandas as pd
import pickle
import json

data_path = 'data/international_matches.csv'
training_data_path = 'data/training.csv'
last_match_data_path = 'data/last_match.csv'

last_match_data = pd.read_csv(last_match_data_path)

model = pickle.load(open('data/model.pkl', 'rb'))
predict_list = json.load(open('data/odds.json', 'r'))


team_datas = []

for data in predict_list:
    team1 = data['Team1']
    team2 = data['Team2']

    team_1_data = last_match_data.loc[last_match_data['Team'] == team1].reset_index(
        drop=True)
    team_2_data = last_match_data.loc[last_match_data['Team'] == team2].reset_index(
        drop=True)
    team_1_data.drop(['Team', 'date'], axis=1, inplace=True)
    team_2_data.drop(['Team', 'date'], axis=1, inplace=True)
    team_1_data.rename(
        {key: 'Team1_' + key for key in team_1_data.keys()}, axis=1, inplace=True)
    team_2_data.rename(
        {key: 'Team2_' + key for key in team_2_data.keys()}, axis=1, inplace=True)
    team_data = team_1_data.merge(
        team_2_data, left_index=True, right_index=True)
    team_data['Team1'] = team1
    team_data['Team2'] = team2
    team_datas.append(team_data)

team_datas_df = pd.concat(team_datas, ignore_index=True)

predict_probas = model.predict_proba(team_datas_df)

for predict_proba, predict_data in zip(predict_probas, predict_list):
    predict_proba = predict_proba.tolist()
    predict_data['win_proba'] = round(predict_proba[0], 3)
    predict_data['lose_proba'] = round(predict_proba[1], 3)
    predict_data['draw_proba'] = round(predict_proba[2], 3)
    print(predict_data)


results = pd.DataFrame(predict_list)
print(results)
results.to_csv('data/results.csv', index=False)
