from sklearn.model_selection import train_test_split
import pandas as pd
from flaml import AutoML
from sklearn.metrics import classification_report
import pickle

training_data_path = 'data/training.csv'

datasets = pd.read_csv(training_data_path)

# datasets.drop(['Team1', 'Team2'], axis=1, inplace=True)

X = datasets.drop('Team1_Result', axis=1)
y = datasets['Team1_Result']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42)


automl = AutoML()
automl.fit(X_train, y_train, task="classification", time_budget=120)


y_pred = automl.predict(X_test)

print(classification_report(y_test, y_pred))


pickle.dump(automl, open('data/model.pkl', 'wb'))
