import pandas as pd

predict_results = pd.read_csv('/tmp/fifa/today_result.csv')


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

columns = ['home_team', 'away_team', 'ratio', 'buy', 'win_odds', 'draw_odds', 'lose_odds', 'win_proba',
           'lose_proba', 'draw_proba']

predict_results = predict_results[columns]

print()

print(predict_results.to_string())

predict_results = predict_results[predict_results['ratio'] > 0]

predict_results['ratio'] /= predict_results['ratio'].sum()
predict_results['ratio'] = predict_results['ratio'].round(2)


if len(predict_results) > 0:
    print(predict_results.to_string())
    print()
    mean = 0
    print("betting strategy:")
    for _, data in predict_results.iterrows():
        mean += data[data['buy']+"_odds"] * data['ratio']
        print(f"{data['home_team']} vs {data['away_team']}: {data['buy']} {data['ratio']}")

    print("The possible payoff is : ", mean)

else:
    print("No bet today!")
