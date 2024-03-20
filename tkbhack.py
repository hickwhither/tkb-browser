import requests

from bs4 import BeautifulSoup
import json
from datetime import date

import time, os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
URL = 'http://thptchuyennguyentatthanh.kontum.edu.vn/TKB/tkb_block_0.html'

def get_data(dont_request: bool = False):
    """
    Requests to tkb home for the data
    
    Return tuple (result, error)
    - result: dict of data
    - error: requests.exceptions.RequestException, None if no error
    """
    if not os.path.exists('data.json'):
        data = {'date': None, 'classlist': [], 'tkb': {}}
    else:
        try:
            with open("data.json", "r") as f: data = json.load(f)
        except: data = {'date': None, 'classlist': [], 'tkb': {}}
    
    if dont_request: return data, None

    try: html = requests.get(URL,headers=HEADERS,timeout=1,verify=False,proxies={'http':'http://112.78.2.73'}).content.decode()
    except Exception as e: return data, e
    
    
    date = html[556:566]
    classlist = []
    tkb = {}

    table = BeautifulSoup(html, features="html.parser").find('table', class_='cls-tblTKB')
    rows = table.find_all('tr')
    
    # Initializing Classlist
    for i in rows[0].find_all('font', face="Tahoma", size="2pt"): 
        classlist.append(i.text)
        tkb[i.text] = ['']

    # Initializing Lesson
    for cl in classlist:
        tkb[cl] = [[],[],[],[],[],[]]
    
    for weekday in range(6):
        for period in range((weekday+1)*5-4, (weekday+1)*5+1):
            row = rows[period].find_all('font', face="Tahoma", size="2pt")
            for i in range(len(row)):
                tkb[classlist[i]][weekday].append(row[i].text)
        
    result = {
            'date': date,
            'classlist': classlist,
            'tkb': tkb
        }

    with open("data.json", "w") as f:
        json.dump(result, f, indent=4)
    
    return result, None
