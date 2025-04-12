# -*- coding: utf-8 -*-
"""MarinoCassCodes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1q1ZBzgK7dm95e_JZvJL-sbC-YrB7WcBo
"""



!pip install cassandra-driver


from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

cloud_config= {
  'secure_connect_bundle': 'secure-connect-ellamarino-cassandra.zip'
}


with open("ellamarino_cassandra-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

if session:
  print('Connected!')
else:
  print("An error occurred.")

session = cluster.connect()

import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/gchandra10/filestorage/refs/heads/main/sales_100.csv')

session.execute("""
    CREATE TABLE IF NOT EXISTS cassandradata.sales_data (
    Region TEXT,
    Country TEXT,
    Item_Type TEXT,
    Sales_Channel TEXT,
    Order_Priority TEXT,
    Order_Date DATE,
    Order_ID BIGINT,
    Ship_Date DATE,
    Units_Sold INT,
    Unit_Price DECIMAL,
    Unit_Cost DECIMAL,
    Total_Revenue DECIMAL,
    Total_Cost DECIMAL,
    Total_Profit DECIMAL,
    PRIMARY KEY (Order_ID)
);
""")

print(df.columns)

import pandas as pd


file_path = 'https://raw.githubusercontent.com/gchandra10/filestorage/refs/heads/main/sales_100.csv'
df = pd.read_csv(file_path)

sorted_df = df.sort_values(by='Region')


sorted_df.to_csv('sorted_output.csv', index=False)

print(sorted_df)

session.set_keyspace('cassandradata')


df['Order Date'] = pd.to_datetime(df['Order Date']).dt.date
df['Ship Date'] = pd.to_datetime(df['Ship Date']).dt.date


for _, row in df.iterrows():
    session.execute("""
        INSERT INTO sales_data (
            Region, Country, Item_Type, Sales_Channel,
            Order_Priority, Order_Date, Order_ID, Ship_Date,
            Units_Sold, Unit_Price, Unit_Cost,
            Total_Revenue, Total_Cost, Total_Profit
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['Region'], row['Country'], row['Item Type'], row['Sales Channel'],
        row['Order Priority'], row['Order Date'], int(row['Order ID']), row['Ship Date'],
        int(row['UnitsSold']), float(row['UnitPrice']), float(row['UnitCost']),
        float(row['TotalRevenue']), float(row['TotalCost']), float(row['TotalProfit'])
    ))

import pandas as pd
from cassandra.cluster import Cluster
from uuid import uuid4
from datetime import datetime


file_path = 'https://raw.githubusercontent.com/gchandra10/filestorage/refs/heads/main/sales_100.csv'
df = pd.read_csv(file_path)


silver_df = df.drop_duplicates().dropna()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%Y")
    except:
        return None

silver_df['Order Date'] = silver_df['Order Date'].apply(parse_date)
silver_df['Ship Date'] = silver_df['Ship Date'].apply(parse_date)


silver_df = silver_df[silver_df['Order Date'].notnull() & silver_df['Ship Date'].notnull()]


cloud_config= {
  'secure_connect_bundle': 'secure-connect-ellamarino-cassandra.zip'
}


with open("ellamarino_cassandra-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

if session:
  print('Connected!')
else:
  print("An error occurred.")
session.set_keyspace('cassandradata') 


session.execute("""
    CREATE TABLE IF NOT EXISTS silver_sales (
        order_id uuid PRIMARY KEY,
        region text,
        country text,
        item_type text,
        sales_channel text,
        order_priority text,
        order_date date,
        ship_date date,
        units_sold int,
        unit_price float,
        unit_cost float,
        total_revenue float,
        total_cost float,
        total_profit float
    )
""")


for _, row in silver_df.iterrows():
    session.execute("""
        INSERT INTO silver_sales (
            order_id, region, country, item_type, sales_channel,
            order_priority, order_date, ship_date, units_sold,
            unit_price, unit_cost, total_revenue, total_cost, total_profit
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        uuid4(),
        row['Region'], row['Country'], row['Item Type'], row['Sales Channel'],
        row['Order Priority'],
        row['Order Date'].date(), row['Ship Date'].date(),
        int(row['UnitsSold']), float(row['UnitPrice']), float(row['UnitCost']),
        float(row['TotalRevenue']), float(row['TotalCost']), float(row['TotalProfit'])
    ))

rows = session.execute("SELECT * FROM silver_sales")

for row in rows:
    print(row)

session.execute("""
CREATE TABLE IF NOT EXISTS cassandradata.gold_sales_by_country (
    country TEXT PRIMARY KEY,
    total_units_sold INT,
    total_revenue DECIMAL
);
""")

sales_country = df.groupby('Country').agg({
    'UnitsSold': 'sum',
    'TotalRevenue': 'sum'
}).reset_index()

for _, row in sales_country.iterrows():
    session.execute("""
        INSERT INTO cassandradata.gold_sales_by_country (country, total_units_sold, total_revenue)
        VALUES (%s, %s, %s)
    """, (row['Country'], int(row['UnitsSold']), float(row['TotalRevenue'])))


rows = session.execute("SELECT * FROM cassandradata.gold_sales_by_country")

for row in rows:
    print(f"Country: {row.country}, Total Units Sold: {row.total_units_sold}, Total Revenue: {row.total_revenue}")

session.execute("DROP TABLE IF EXISTS cassandradata.customer_sales;")


session.execute("""
CREATE TABLE IF NOT EXISTS cassandradata.customer_sales (
    order_id TEXT PRIMARY KEY,
    total_revenue DECIMAL,
    total_purchases INT,
    most_purchased_product TEXT
);
""")


import uuid
from decimal import Decimal


customer_sales = df.groupby('Order ID').agg({
    'TotalRevenue': 'sum',
    'TotalProfit': 'sum',
    'UnitsSold': 'sum',
    'Item Type': 'first'
}).reset_index()


for _, row in customer_sales.iterrows():
    session.execute("""
        INSERT INTO cassandradata.customer_sales (order_id, total_revenue, total_purchases, most_purchased_product)
        VALUES (%s, %s, %s, %s)
    """, (str(row['Order ID']), float(row['TotalRevenue']), int(row['UnitsSold']), row['Item Type']))

rows = session.execute("SELECT * FROM cassandradata.customer_sales")


for row in rows:
    print(f"Order ID: {row.order_id}, Total Revenue: {row.total_revenue}, Total Purchases: {row.total_purchases}, Most Purchased Product: {row.most_purchased_product}")

session.execute("""
CREATE TABLE IF NOT EXISTS cassandradata.gold_sales_by_product_type (
    item_type TEXT PRIMARY KEY,
    total_units_sold INT,
    total_revenue DOUBLE,
    total_cost DOUBLE,
    total_profit DOUBLE,
    avg_unit_price DOUBLE,
    avg_unit_cost DOUBLE
);
""")

item_sales = df.groupby('Item Type').agg({
    'UnitsSold': 'sum',
    'TotalRevenue': 'sum',
    'TotalCost': 'sum',
    'TotalProfit': 'sum',
    'UnitPrice': 'mean',
    'UnitCost': 'mean'
}).reset_index()


for _, row in item_sales.iterrows():
    session.execute("""
        INSERT INTO cassandradata.gold_sales_by_product_type (
            item_type, total_units_sold, total_revenue, total_cost,
            total_profit, avg_unit_price, avg_unit_cost
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['Item Type'], int(row['UnitsSold']), float(row['TotalRevenue']),
        float(row['TotalCost']), float(row['TotalProfit']),
        float(row['UnitPrice']), float(row['UnitCost'])
    ))


rows = session.execute("SELECT * FROM cassandradata.gold_sales_by_product_type")
for row in rows:
    print(row)
