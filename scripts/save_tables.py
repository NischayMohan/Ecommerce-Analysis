import pandas as pd
import os

orders = pd.read_csv(r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\data\df_Orders.csv")
customers = pd.read_csv(r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\data\df_Customers.csv")
products = pd.read_csv(r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\data\df_Products.csv")


# --- DIM CUSTOMERS ---
dim_customers = customers[['customer_id', 'customer_city', 'customer_state']]
dim_customers = dim_customers.copy()
dim_customers.drop_duplicates(inplace=True)

# --- DIM PRODUCTS ---
dim_products = products[['product_id', 'product_category_name',
                         'product_weight_g', 'product_length_cm',
                         'product_height_cm', 'product_width_cm']]
dim_products.drop_duplicates(inplace=True)

# --- DIM DATE ---
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
dim_date = orders[['order_id', 'order_purchase_timestamp']].copy()
dim_date['year'] = dim_date['order_purchase_timestamp'].dt.year
dim_date['month'] = dim_date['order_purchase_timestamp'].dt.month
dim_date['day'] = dim_date['order_purchase_timestamp'].dt.day
dim_date['weekday'] = dim_date['order_purchase_timestamp'].dt.day_name()
dim_date['date_id'] = dim_date.index



# FACT TABLE (sales)
fact_sales = orders[['order_id', 'customer_id', 'order_purchase_timestamp']].copy()

# Link with dim_date
fact_sales = fact_sales.merge(dim_date[['order_id', 'date_id']], on='order_id')

# Keep final useful columns
fact_sales = fact_sales[['order_id', 'customer_id', 'date_id']]



# Create folder 
os.makedirs("transformed", exist_ok=True)

# save tables
fact_sales.to_csv("transformed/fact_sales.csv", index=False)
dim_customers.to_csv("transformed/dim_customers.csv", index=False)
dim_products.to_csv("transformed/dim_products.csv", index=False)
dim_date.to_csv("transformed/dim_dates.csv", index=False)
