import numpy as np
import pandas as pd
import random

df = np.random.randint(0, 50, (10, 10)) / 10
for i in range(40):
    r1 = random.randint(0, 9)
    r2 = random.randint(0, 9)
    df[r1, r2] = np.nan

count = 0
for i in df:
    for j in i:
        if np.isnan(j):
            count += 1
index = ["Movie 1", "Movie 2", "Movie 3", "Movie 4", "Movie 5",
           "Movie 6", "Movie 7", "Movie 8", "Movie 9", "Movie 10"]
columns = ["Person 1", "Person 2", "Person 3", "Person 4", "Person 5",
         "Person 6", "Person 7", "Person 8", "Person 9", "Person 10"]
df = pd.DataFrame(df, columns=columns, index=index)
print(df)
df.to_csv("random_matrix.csv")
print(count)
print(count / 100)
