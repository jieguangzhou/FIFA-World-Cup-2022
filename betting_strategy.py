import pandas as pd

predict_results = pd.read_csv('data/results.csv')


def calc_ratio(data):
    wind_proba = data['win_proba']
    lose_proba = data['lose_proba']
    draw_proba = data['draw_proba']

    max_proba = max(wind_proba, lose_proba, draw_proba)

    if wind_proba == max_proba:
        p = wind_proba
        b = data['win_odds']
        buy = "win"
    elif lose_proba == max_proba:
        p = lose_proba
        b = data['lose_odds']
        buy = "lose"
    else:
        p = draw_proba
        b = data['draw_odds']
        buy = "draw"

    ratio = (p * b - 1) / p
    return ratio, buy


predict_results[['ratio', 'buy']] = predict_results.apply(
    calc_ratio, axis=1, result_type="expand")

predict_results['ratio'] /= predict_results['ratio'].sum()

columns = ['Team1', 'Team2', 'ratio', 'buy', 'win_odds', 'draw_odds', 'lose_odds', 'win_proba',
           'lose_proba', 'draw_proba']

print(predict_results[columns])
