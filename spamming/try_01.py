import pandas as pd

df = pd.DataFrame({"value": [1600000]})
df["formatted"] = df["value"].apply(lambda n: "{:.1e}".format(n))
print(df)
