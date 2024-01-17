import requests
import gspread
import time
import random
import datetime

item_nameids = ['YOUR_NAMEIDS', 'YOUR_NAMEIDS', 'YOUR_NAMEIDS', 'YOUR_NAMEIDS', 'YOUR_NAMEIDS', 'YOUR_NAMEIDS']

# google sheets auth and open sheet
gs = gspread.service_account()
wks = gs.open('case_data').worksheet('inventory')

# requests header
header = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

i = 0

while i < 1:
    try:
        rand_num = random.randint(0, 1800)
        for idx, item_nameid in enumerate(item_nameids, start=2):
            # build the URL with the current item_nameid
            url = f'https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_nameid}&two_factor=0'
            
            # status code 200 for get request
            r = requests.get(url, headers=header)
            
            # json data from the request
            item_det = r.json()
            
            # gets the highest buyorder
            buy_order = item_det['buy_order_graph'][0][0]
            # gets the qty of orders with highest buy price
            buy_qty = item_det['buy_order_graph'][0][1]
            
            # gets the highest sellorder
            sell_order = item_det['sell_order_graph'][0][0]
            # gets the qty of orders with highest sell price
            sell_qty = item_det['sell_order_graph'][0][1]
            
            # update the corresponding rows in the Spreadsheet
            wks.update(f'B{idx}', sell_order)
            wks.update(f'C{idx}', sell_qty)
            wks.update(f'D{idx}', buy_order)
            wks.update(f'E{idx}', buy_qty)
            
            # update the last updated timestamp in row G for each item
            current = datetime.datetime.now()
            wks.update(f'F{idx}', 'Last Updated On: ' + current.strftime('%D') + ' At: ' + current.strftime('%H:%M:%S') + ' IST')

        time.sleep(30)

    except (gspread.exceptions.APIError, ValueError, KeyError, ConnectionResetError, requests.exceptions.RequestException) as e:
        print('Error: ' + str(e))
        time.sleep(30)
