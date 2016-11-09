import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

elections = []

for line in open("ELECTION_ID"):
    l = line.split()
    year = l[0]+".csv"

    header = pd.read_csv(year, nrows = 1).dropna(axis = 1)
    d = header.iloc[0].to_dict()

    df = pd.read_csv(year, index_col = 0, thousands = ",", skiprows = [1])

    df.rename(inplace = True, columns = d)
    df.dropna(inplace = True, axis = 1)
    df["Year"] = l[0]
    elections.append(df[["Democratic", "Republican", "Total Votes Cast", "Year"]])

total = pd.concat(elections)
total["Republican Share"] = total["Republican"]/total["Total Votes Cast"]
accomack = total.loc['Accomack County'].sort_values(by = 'Year', ascending = True)

print(accomack)

graph = accomack.plot(kind = "line", x = "Year", y = "Republican Share")
graph.get_figure().savefig('accomack.png')
