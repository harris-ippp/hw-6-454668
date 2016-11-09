import requests
from bs4 import BeautifulSoup as bs

for line in open("ELECTION_ID"):
    l = line.split()
    files = "http://historical.elections.virginia.gov/elections/download/{}/precincts_include:0/".format(l[1])
    resp = requests.get(files)
    soup = bs(resp.content , "html.parser")
    file_name = l[0] + ".csv"
    with open(file_name, "w") as out:
        out.write(resp.text)
