import pandas as pd

data_path = 'data/international_matches.csv'
training_data_path = 'data/training.csv'
last_match_data_path = 'data/last_match.csv'

list_2022 = ['Qatar', 'Germany', 'Denmark', 'Brazil', 'France', 'Belgium', 'Croatia', 'Spain', 'Serbia', 'England', 'Switzerland', 'Netherlands', 'Argentina', 'IR Iran', 'Korea Republic',
             'Japan', 'Saudi Arabia', 'Ecuador', 'Uruguay', 'Canada', 'Ghana', 'Senegal', 'Portugal', 'Poland', 'Tunisia', 'Morocco', 'Cameroon', 'USA', 'Mexico', 'Wales', 'Australia', 'Costa Rica']

df = pd.read_csv(data_path, parse_dates=['date'])


df['home_team_goalkeeper_score'] = round(df.groupby("home_team")[
                                         "home_team_goalkeeper_score"].transform(lambda x: x.fillna(x.mean())))
df['away_team_goalkeeper_score'] = round(df.groupby("away_team")[
                                         "away_team_goalkeeper_score"].transform(lambda x: x.fillna(x.mean())))

df['home_team_mean_defense_score'] = round(df.groupby('home_team')[
                                           'home_team_mean_defense_score'].transform(lambda x: x.fillna(x.mean())))
df['away_team_mean_defense_score'] = round(df.groupby('away_team')[
                                           'away_team_mean_defense_score'].transform(lambda x: x.fillna(x.mean())))


df['home_team_mean_offense_score'] = round(df.groupby('home_team')[
                                           'home_team_mean_offense_score'].transform(lambda x: x.fillna(x.mean())))
df['away_team_mean_offense_score'] = round(df.groupby('away_team')[
                                           'away_team_mean_offense_score'].transform(lambda x: x.fillna(x.mean())))


df['home_team_mean_midfield_score'] = round(df.groupby('home_team')[
                                            'home_team_mean_midfield_score'].transform(lambda x: x.fillna(x.mean())))
df['away_team_mean_midfield_score'] = round(df.groupby('away_team')[
                                            'away_team_mean_midfield_score'].transform(lambda x: x.fillna(x.mean())))
df.fillna(50, inplace=True)


final_df = df[(df["home_team"].apply(lambda x: x in list_2022))
              | (df["away_team"].apply(lambda x: x in list_2022))]


# Mapping numeric values for home_team_result to find the correleations
final_df['home_team_result'] = final_df['home_team_result'].map(
    {'Win': 1, 'Draw': 2, 'Lose': 0})


final_df = final_df.drop(['home_team_continent', 'away_team_continent', 'home_team_total_fifa_points', 'away_team_total_fifa_points',
                         'home_team_score', 'away_team_score', 'tournament', 'city', 'country', 'neutral_location', 'shoot_out'], axis=1)


# Change column names
final_df.rename(columns={"home_team": "Team1", "away_team": "Team2", "home_team_fifa_rank": "Team1_FIFA_RANK",
                         "away_team_fifa_rank": "Team2_FIFA_RANK", "home_team_result": "Team1_Result", "home_team_goalkeeper_score": "Team1_Goalkeeper_Score",
                         "away_team_goalkeeper_score": "Team2_Goalkeeper_Score", "home_team_mean_defense_score": "Team1_Defense",
                         "home_team_mean_offense_score": "Team1_Offense", "home_team_mean_midfield_score": "Team1_Midfield",
                         "away_team_mean_defense_score": "Team2_Defense", "away_team_mean_offense_score": "Team2_Offense",
                         "away_team_mean_midfield_score": "Team2_Midfield"}, inplace=True)

#
# final_df['Team1_FIFA_RANK_best'] = final_df['Team1_FIFA_RANK'] > final_df['Team2_FIFA_RANK']
#
# final_df['Team1_Offense_ratio'] = final_df['Team1_Offense'] / final_df['Team2_Offense']
# final_df['Team1_Defense_ratio'] = final_df['Team1_Defense'] / final_df['Team2_Defense']
#
# final_df['Team1_Midfield_ratio'] = final_df['Team1_Midfield'] / final_df['Team2_Midfield']


last_match_datas = []
for team in list_2022:
    team_data_1 = final_df[final_df['Team1'] ==
                           team].sort_values(by='date').iloc[-1]
    team_data_2 = final_df[final_df['Team2'] ==
                           team].sort_values(by='date').iloc[-1]

    if team_data_2.date >= team_data_1.date:
        team_data = team_data_2.copy()
        team_data = team_data[[
            key for key in team_data.keys() if not key.startswith("Team1")]]
        team_data['Team'] = team_data.pop("Team2")
    else:
        team_data = team_data_1.copy()
        team_data = team_data[[
            key for key in team_data.keys() if not key.startswith("Team2")]]
        team_data['Team'] = team_data.pop("Team1")

    team_data.rename({key: key.replace("Team1_", "").replace("Team2_", "")
                     for key in team_data.keys()}, inplace=True)
    last_match_datas.append(team_data)


last_match_datas_df = pd.DataFrame(last_match_datas)
last_match_datas_df.drop('Result', axis=1, inplace=True)


final_df.drop(['date'], axis=1, inplace=True)
final_df.to_csv(training_data_path, index=False)

last_match_datas_df.to_csv(last_match_data_path, index=False)
