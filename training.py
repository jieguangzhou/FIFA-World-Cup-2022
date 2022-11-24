from sklearn.model_selection import train_test_split
import pandas as pd
from flaml import AutoML
from sklearn.metrics import classification_report
import pickle

train_time = 10  # $PARAM:

training_data_path = '/tmp/fifa/training.csv'
model_path = '/tmp/fifa/model.pkl'

datasets = pd.read_csv(training_data_path)

X = datasets.drop('label', axis=1)
y = datasets['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42)


automl = AutoML()
automl.fit(X_train, y_train, task="classification", time_budget=train_time)


y_pred = automl.predict(X_test)

print(classification_report(y_test, y_pred))


pickle.dump(automl, open(model_path, 'wb'))
