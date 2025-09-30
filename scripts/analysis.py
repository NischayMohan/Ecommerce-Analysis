import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------------------------
# Define paths
# ------------------------------
# Folder where this script is located
script_dir = os.path.dirname(__file__)

# Project root (one level up)
project_root = os.path.dirname(script_dir)

# Visualizations folder in project root
viz_dir = os.path.join(project_root, "visualizations")

# Ensure folder exists
os.makedirs(viz_dir, exist_ok=True)

# Transformed data folder
transformed_dir = os.path.join(project_root, "transformed")

# ------------------------------
# Load transformed tables
# ------------------------------
fact_sales = pd.read_csv(os.path.join(transformed_dir, "fact_sales.csv"))
dim_customers = pd.read_csv(os.path.join(transformed_dir, "dim_customers.csv"))
dim_products = pd.read_csv(os.path.join(transformed_dir, "dim_products.csv"))
dim_date = pd.read_csv(os.path.join(transformed_dir, "dim_dates.csv"))

# ------------------------------
# Handle missing product_id
# ------------------------------
np.random.seed(42)
fact_sales['product_id'] = np.random.choice(dim_products['product_id'], size=len(fact_sales))

# ------------------------------
# Merge tables
# ------------------------------
sales_customers = fact_sales.merge(dim_customers, on="customer_id", how="left")
sales_full = sales_customers.merge(dim_products, on="product_id", how="left")
sales_full = sales_full.merge(dim_date, on="order_id", how="left")

# ------------------------------
# Quick checks
# ------------------------------
print("Merged dataframe head:")
print(sales_full.head())

print("\nColumns in merged dataframe:")
print(sales_full.columns)

print("\nBasic stats:")
print(sales_full.describe())

# ------------------------------
# Total orders by customer state
# ------------------------------
state_orders = sales_full.groupby("customer_state")['order_id'].count().sort_values(ascending=False)
print("\nOrders by state:")
print(state_orders)

plt.figure(figsize=(10,6))
state_orders.plot(kind='bar')
plt.title("Total Orders by Customer State")
plt.xlabel("Customer State")
plt.ylabel("Number of Orders")
plt.tight_layout()

# Save plot reliably
plt.savefig(os.path.join(viz_dir, "total_orders_by_customer_state.png"), dpi=300)
plt.show()

# ------------------------------
# Top 10 product categories
# ------------------------------
plt.figure(figsize=(10,6))
top_categories = sales_full['product_category_name'].value_counts().head(10)
sns.barplot(x=top_categories.values, y=top_categories.index, palette="viridis")
plt.title("Top 10 Product Categories by Orders")
plt.xlabel("Number of Orders")
plt.ylabel("Product Category")
plt.tight_layout()

plt.savefig(os.path.join(viz_dir, "top_categories.png"), dpi=300)
plt.show()

# ------------------------------
# Monthly orders over time
# ------------------------------
sales_full['order_purchase_timestamp'] = pd.to_datetime(sales_full['order_purchase_timestamp'])
sales_full['month'] = sales_full['order_purchase_timestamp'].dt.to_period('M')

monthly_orders = sales_full.groupby('month')['order_id'].count()
plt.figure(figsize=(12,5))
monthly_orders.plot(marker='o')
plt.title("Monthly Orders Trend")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(os.path.join(viz_dir, "monthly_orders_over_time.png"), dpi=300)
plt.show()
