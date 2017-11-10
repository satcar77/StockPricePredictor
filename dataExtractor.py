import requests
import csv 
from bs4 import BeautifulSoup
#look up the company id from this ajax JSON request http://www.sharesansar.com/wp-admin/admin-ajax.php?action=get_company_quotes
company_id="493"
from_date="2001-01-01"
to_date="2017-10-30"
# Price index ref: Open=1	High=2	Low=2	Close=3	
price_index=3

url="http://www.sharesansar.com/wp-admin/admin-ajax.php?price_company_id={}&from_date={}&end_date={}&row_id=500&action=get_price_history_data".format(company_id,from_date,to_date)
txt=requests.get(url)
text=txt.text
bs=BeautifulSoup(text)
rows=bs.select("tr")
with open('sharedata.csv','w') as csvfile: 
    writer=csv.writer(csvfile)
    for r in rows : 
        content=[i.string for i in r.select("td")]
        if(not content):
            continue
        writer.writerow([content[price_index]])
print("Done")
