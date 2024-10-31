import requests
import bs4
import re
import json
import pandas as pd

scores = []

for i in range(1990,2024):
    print(f"Parsing year {i}...")
    res = requests.get(f"https://lab24.ilsole24ore.com/qualita-della-vita/tabelle/{str(i)}/classifica-finale")
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    script_tag = soup.find_all("script")[18].string
    raw_data = re.findall("datiTabella.*?}]};", script_tag)[0].strip("datiTabella=").strip(";")
    data = json.loads(raw_data)["righe"]
    
    for provincia in data:
        temp_dict = {
            "name": provincia["nome"],
            "score": provincia["punti"],
            "year" : i
        }
        scores.append(temp_dict)

dataframe = pd.DataFrame(scores)
dataframe.sort_values(by=["name", "year"], inplace=True)
dataframe.to_csv("data.csv", index=False)
