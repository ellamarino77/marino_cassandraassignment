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

     INSERT INTO sales_data (
            Region, Country, Item_Type, Sales_Channel,
            Order_Priority, Order_Date, Order_ID, Ship_Date,
            Units_Sold, Unit_Price, Unit_Cost,
            Total_Revenue, Total_Cost, Total_Profit
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);




CREATE TABLE IF NOT EXISTS cassandradata.silver_sales (
    order_id uuid PRIMARY KEY,
    region text,
    country text,
    item_type text,
    sales_channel text,
    order_priority text,
    order_date text
);


INSERT INTO cassandradata.silver_sales (order_id, region, country, item_type, sales_channel, order_priority, order_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s);

	SELECT * FROM cassandradata.silver_sales;

CREATE TABLE IF NOT EXISTS cassandradata.gold_sales_by_country (
    country TEXT PRIMARY KEY,
    total_units_sold INT,
    total_revenue DECIMAL
);

  INSERT INTO cassandradata.gold_sales_by_country (country, total_units_sold, total_revenue)
        VALUES (%s, %s, %s);

SELECT * FROM cassandradata.gold_sales_by_country;



CREATE TABLE IF NOT EXISTS cassandradata.customer_sales (
    order_id TEXT PRIMARY KEY,
    total_revenue DECIMAL,
    total_purchases INT,
    most_purchased_product TEXT
);

INSERT INTO cassandradata.customer_sales (order_id, total_revenue, total_purchases, most_purchased_product)
        VALUES (%s, %s, %s, %s);


SELECT * FROM cassandradata.customer_sales;


CREATE TABLE IF NOT EXISTS cassandradata.gold_sales_by_product_type (
    item_type TEXT PRIMARY KEY,
    total_units_sold INT,
    total_revenue DOUBLE,
    total_cost DOUBLE,
    total_profit DOUBLE,
    avg_unit_price DOUBLE,
    avg_unit_cost DOUBLE
);



INSERT INTO cassandradata.gold_sales_by_product_type (
            item_type, total_units_sold, total_revenue, total_cost,
            total_profit, avg_unit_price, avg_unit_cost
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);


SELECT * FROM cassandradata.gold_sales_by_product_type;



































