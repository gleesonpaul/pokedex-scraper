import requests as rq
from bs4 import BeautifulSoup as b
import pandas as pd
import sqlite3 as db

c = db.connect("db.db")
r = rq.get("https://pokemondb.net/pokedex/all")
s = b(r.content, 'html5lib')
t = s.find('table', attrs={'id':'pokedex'})

h = [i.text for i in t.findAll('div')]

dta = []
cl = "td:nth-child"
bu = "https://pokemondb.net"

# apply apply transformation to header list - to accommodate additional data within the table
h[0] = 'Number'
h.insert(1,"AVIF Icon Link")
h.insert(2,"PNG Icon Link")
h.insert(4,"Pokemon Page Link")
h.insert(6,"Type Page Links")

for rw in t.select('tbody > tr'):    
    dta.append([rw.select(cl+'(1) > span')[0].text, rw.select(cl+'(1) > picture > source')[0]['srcset'], rw.select(cl+'(1) > picture > img')[0]['src'], rw.select(cl+'(2) > a')[0].text, bu + rw.select(cl+'(2) > a')[0]['href'], ", ".join([i.text for i in rw.select(cl+'(3) > a')]), ", ".join([bu + i["href"] for i in rw.select(cl+'(3) > a')]), rw.select(cl+'(4)')[0].text, rw.select(cl+'(5)')[0].text, rw.select(cl+'(6)')[0].text, rw.select(cl+'(7)')[0].text, rw.select(cl+'(8)')[0].text, rw.select(cl+'(9)')[0].text, rw.select(cl+'(10)')[0].text])

df = pd.DataFrame(dta, columns=h)
df.to_sql(name="tbl", con=c, index=False, if_exists="replace")
df2 = pd.read_sql('select * from tbl', c)
c.close()