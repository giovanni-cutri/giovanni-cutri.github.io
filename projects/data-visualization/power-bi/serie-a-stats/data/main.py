import pandas as pd

df = pd.read_html("https://it.wikipedia.org/wiki/Serie_A_2021-2022")[4]
df.drop("Unnamed: 0", axis=1, inplace=True)
df["Pos."] = df["Pos."].astype("int")
df.to_csv("data.csv", index=False)
