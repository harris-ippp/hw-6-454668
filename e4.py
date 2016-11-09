import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def total_share(county_name):

    address = "http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2015/office_id:1/stage:General"
    resp = requests.get(address)
    soup = bs(resp.content , "html.parser")
    R = soup.find_all("tr", "election_item")
    with open("ELECTION_ID", "w") as out:
        for row in R:
            v1 = row.find("td", "year first").contents[0]
            v2 = row.get("id").replace("election-id-", "")
            out.write("{} {}\n".format(v1, v2))

    for line in open("ELECTION_ID"):
        l = line.split()
        files = "http://historical.elections.virginia.gov/elections/download/{}/precincts_include:0/".format(l[1])
        resp = requests.get(files)
        soup = bs(resp.content , "html.parser")
        file_name = l[0] + ".csv"
        with open(file_name, "w") as out1:
            out1.write(resp.text)

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
    county = total.loc[county_name+" County"].sort_values(by = 'Year', ascending = True)

    print(county)
    graph = county.plot(kind = "line", x = "Year", y = "Republican Share")
    graph.get_figure().savefig("{}.png".format(county_name))

county_name=input("What is the county?(Please Intial Caps)\n")

total_share(county_name)
