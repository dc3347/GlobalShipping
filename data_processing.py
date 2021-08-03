"""
This script extracts the appropriate columns from a shipping database 
and each country's order database and calculate the average shiptimes
of orders per country.
"""

import pandas as pd
import os
import datetime 
import csv

shipping_df = pd.read_excel('./Shipping/ShippingDatabase.xlsx', 'Sheet1')
shipping_df.drop_duplicates(subset = ['OrderID'])
shipping_table = pd.DataFrame(shipping_df, columns = ['OrderID','Ship Date'])

shipping_dict = {}

for index, row in shipping_table.iterrows():
  shipping_order_id = str(row['OrderID']).split('#')[0].strip()
  
  d = str(row['Ship Date']).strip()
  ship_date = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date()
  
  # shipping_dict has id and ship date for all countries
  shipping_dict[shipping_order_id] = ship_date
  
  
average_shiptime = {}
for filename in os.listdir('/Downloads/GlobalShipping/Sales'):
  if filename.endswith('.csv'):
    filepath = os.path.join('/Downloads/GlobalShipping/Sales', filename)
    
    # read in csv
    df = pd.read_csv(filepath, encoding = 'ISO-8859-1')
    
    # get rid of duplicate orders
    df.drop_duplicates(subset = ['Order ID'])
    
    # create table with just order id and order date columns
    order_table = pd.DataFrame(df, columns = ['Order ID', 'Order Date'])
    
    order_dict = {}
    for index, row in order_table.iterrows():
      order_id = row['Order ID'].split('-')[2].strip()
      d = row['Order Date'].strip()
      
      # convert to datetime object
      order_date = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date()
      
      order_dict[order_id] = order_date
  
  # the calculated shipping times for all orders in one country
  shipping_time = []
  
  # accounts for orders that were actually shipping and not canceled
  for key in shipping_dict:
    # calculate number of days it took to ship and adds to shipping_time array
    if key in order_dict:
      shipping_time.append((shipping_dict[key] - order_dict[key]).days)
      
  # take average of shipping times
  shipping_average = sum(shipping_time)/len(shipping_time)
  
  # store average corresponding to country in average_shiptime
  filename = filename[:-4]
  average_shiptime[filename] = shipping_average
  
  # export data as csv
  with open('average_shiptime.csv', 'w') as f:
    for key in average_shiptime.keys():
      f.write("%s,%s\n"%(key,average_shiptime[key]))
    
