import requests
from bs4 import BeautifulSoup as bs
address = "http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2015/office_id:1/stage:General"
resp = requests.get(address)
soup = bs(resp.content , "html.parser")
R = soup.find_all("tr", "election_item")
with open("ELECTION_ID", "w") as out:
    for row in R:
        v1 = row.find("td", "year first").contents[0]
        v2 = row.get("id").replace("election-id-", "")
        out.write("{} {}\n".format(v1, v2))
