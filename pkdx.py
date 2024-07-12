import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

request = requests.get("https://pokemondb.net/pokedex/all")
soup = BeautifulSoup(request.content, 'html5lib')
table = soup.find('table', attrs={'id':'pokedex'})

headers = [i.text for i in table.findAll('div')]

pokedex_list = []
selector = "td:nth-child"
baseURL = "https://pokemondb.net"

# apply transformation to header list - to accommodate additional data within the table
headers[0] = 'Number'
headers.insert(1,"AVIF Icon Link")
headers.insert(2,"PNG Icon Link")
headers.insert(4,"Pokemon Page Link")
headers.insert(6,"Type Page Links")

for row in table.select('tbody > tr'):    
    pokedex_list.append([
        row.select(selector+'(1) > span')[0].text,                                  # Number(#)
        row.select(selector+'(1) > picture > source')[0]['srcset'],                 # AVIF Icon Link
        row.select(selector+'(1) > picture > img')[0]['src'],                       # PNG Icon Link
        row.select(selector+'(2) > a')[0].text,                                     # Pokemon Name
        baseURL + row.select(selector+'(2) > a')[0]['href'],                        # Pokemon Page LInk        
        ", ".join([i.text for i in row.select(selector+'(3) > a')]),                # Type Name
        ", ".join([baseURL + i["href"] for i in row.select(selector+'(3) > a')]),   # Type Page Link
        row.select(selector+'(4)')[0].text,                                         # Total
        row.select(selector+'(5)')[0].text,                                         # HP
        row.select(selector+'(6)')[0].text,                                         # Attack
        row.select(selector+'(7)')[0].text,                                         # Defense
        row.select(selector+'(8)')[0].text,                                         # Sp. Attack
        row.select(selector+'(9)')[0].text,                                         # Sp. Def
        row.select(selector+'(10)')[0].text                                         # Speed
    ])

pokedex_df = pd.DataFrame(pokedex_list, columns=headers)

with sqlite3.connect("pokemondb.db") as conn:
    pokedex_df.to_sql(name="pokedex", con=conn, index=False, if_exists="replace")