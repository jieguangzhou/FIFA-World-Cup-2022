import pandas as pd

data_path = '/tmp/fifa/international_matches.csv'
team_path = '/tmp/fifa/Qatar2022-teams.csv'
training_data_path = '/tmp/fifa/training.csv'
last_match_data_path = '/tmp/fifa/last_match.csv'

schedule_df = pd.read_csv('/tmp/fifa/schedule.csv')
schedule_df = schedule_df[schedule_df['type'] == 'group']


teams_set = set(schedule_df['home_team'].tolist() +
                schedule_df['away_team'].tolist())


df = pd.read_csv(data_path, parse_dates=['date'])

df = df[df['date'] > "2012-01-01"]


# fill miss data
keys = ['home_team_total_fifa_points', 'away_team_total_fifa_points',
        'home_team_goalkeeper_score', 'away_team_goalkeeper_score',
        'home_team_mean_defense_score', 'away_team_mean_defense_score',
        'home_team_mean_offense_score', 'away_team_mean_offense_score',
        'home_team_mean_midfield_score', 'away_team_mean_midfield_score',
        ]

for key in keys:
    team_type = key.split('team')[0] + 'team'
    for team, team_df in df.groupby(team_type):
        df.loc[df[team_type] == team,
               key] = team_df[key].fillna(method='ffill')
        df.loc[df[team_type] == team,
               key] = team_df[key].fillna(50)


df = df[(df["home_team"].apply(lambda x: x in teams_set))
        | (df["away_team"].apply(lambda x: x in teams_set))]

base_df = df.copy()

df = df[df['home_team_result'] != "Draw"]

df['label'] = df['home_team_result'].map(
    {'Win': 1, 'Lose': 0})

df['rank_diff'] = 1.0 * (df['home_team_fifa_rank'] - df['away_team_fifa_rank'])
df['rank_mean'] = 0.5 * (df['home_team_fifa_rank'] + df['away_team_fifa_rank'])
df['total_fifa_points'] = 1.0 * (df['home_team_total_fifa_points'] -
                                 df['away_team_total_fifa_points'])
df['goalkeeper_score_diff'] = df['home_team_goalkeeper_score'] - \
    df['away_team_goalkeeper_score']
df['mean_defense_score_diff'] = df['home_team_mean_defense_score'] - \
    df['away_team_mean_defense_score']
df['mean_offense_score_diff'] = df['home_team_mean_offense_score'] - \
    df['away_team_mean_offense_score']
df['mean_midfield_score_diff'] = df['home_team_mean_midfield_score'] - \
    df['away_team_mean_midfield_score']

last_match_datas = []
for team in teams_set:
    team_data_1 = base_df[base_df['home_team'] ==
                          team].sort_values(by='date').iloc[-1]
    team_data_2 = base_df[base_df['away_team'] ==
                          team].sort_values(by='date').iloc[-1]

    # parse away team data
    if team_data_2.date >= team_data_1.date:
        team_data = team_data_2.copy()
        team_data = team_data[[
            key for key in team_data.keys() if not key.startswith("home_team")]]
        team_data['team'] = team_data.pop("away_team")
    # parse home team data
    else:
        team_data = team_data_1.copy()
        team_data = team_data[[
            key for key in team_data.keys() if not key.startswith("away_team")]]
        team_data['team'] = team_data.pop("home_team")

    team_data.rename({key: key.replace("away_team_", "").replace("home_team_", "")
                     for key in team_data.keys()}, inplace=True)
    last_match_datas.append(team_data)


last_match_datas_df = pd.DataFrame(last_match_datas)
dataset_df = df[['rank_diff', 'total_fifa_points', 'goalkeeper_score_diff',
                 'mean_defense_score_diff', 'mean_offense_score_diff', 'mean_midfield_score_diff', 'label']]
dataset_df.to_csv(training_data_path, index=False)

last_match_datas_df.to_csv(last_match_data_path, index=False)
print(last_match_datas_df)
