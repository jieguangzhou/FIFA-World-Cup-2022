import os
import json
import pandas as pd

folder = "/tmp/fifa/simulation/"


files = os.listdir(folder)

results = []
for file in files:
    result = json.load(open(folder + file, "r"))
    results.append(result)

results_df = pd.DataFrame(results)


no1_count = results_df["no.1"].value_counts()
no1_prob = no1_count / len(results_df)

print("no.1 probability:")
print(no1_prob[:5])


no1 = no1_prob.index[0]


no2_df = results_df.loc[results_df["no.1"] == no1]
no2_count = no2_df["no.2"].value_counts()
no2 = no2_count.index[0]

no3_df = no2_df.loc[results_df["no.2"] == no2]
no3_count = no3_df["no.3"].value_counts()
no3 = no3_count.index[0]

no4_df = no3_df.loc[results_df["no.3"] == no3]
no4_count = no4_df["no.4"].value_counts()
no4 = no4_count.index[0]


print("no.1:", no1)
print("no.2:", no2)
print("no.3:", no3)
print("no.4:", no4)
