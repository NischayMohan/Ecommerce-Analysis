import pandas as pd
import os 
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

orders = pd.read_csv(r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\data\df_Orders.csv")
customers = pd.read_csv(r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\data\df_Customers.csv")
products = pd.read_csv(r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\data\df_Products.csv")

# Remove duplicates
orders.drop_duplicates(inplace=True)
customers.drop_duplicates(inplace=True)
products.drop_duplicates(inplace=True)

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'], errors='coerce')



#

# Step 3: Basic Overview
# ----------------------------
print("Orders Info:")
print(orders.info())
print(orders.describe())
print("\nCustomers Info:")
print(customers.info())
print(customers.describe())
print("\nProducts Info:")
print(products.info())
print(products.describe())

print("\nMissing values in Orders:\n", orders.isna().sum())
print("\nMissing values in Customers:\n", customers.isna().sum())
print("\nMissing values in Products:\n", products.isna().sum())

# ----------------------------
# Step 4: Univariate Analysis
# ----------------------------
# Orders over time
orders.set_index('order_purchase_timestamp', inplace=True)
orders['order_id'].resample('M').count().plot(title="Orders Over Time")
plt.ylabel("Number of Orders")
plt.show()

# Top 10 product categories
top_categories = products['product_category_name'].value_counts().head(10)
sns.barplot(x=top_categories.values, y=top_categories.index, color="mediumslateblue")
plt.title("Top 10 Product Categories")
plt.show()

# Top 10 customer states
top_states = customers['customer_state'].value_counts().head(10)
sns.barplot(x=top_states.values, y=top_states.index, color="mediumseagreen")
plt.title("Top 10 Customer States")
plt.show()

# ----------------------------
# Step 5: Merge Datasets
# ----------------------------
orders_customers = orders.reset_index().merge(customers, on="customer_id", how="left")

# ----------------------------
# Step 6: Numeric Analysis & Plots
# ----------------------------

# Box plot: product weight
sns.boxplot(x='product_category_name', y='product_weight_g', data=products)
plt.xticks(rotation=45)
plt.title("Box Plot of Product Weights by Category")
plt.show()

# Scatter plot: product dimensions
sns.scatterplot(x='product_length_cm', y='product_width_cm', size='product_weight_g',
                hue='product_category_name', data=products, alpha=0.7)
plt.title("Scatter Plot of Product Length vs Width (Size = Weight)")
plt.show()

# Parallel coordinates plot: compare numeric features by category
# Select top 5 categories for clarity
top5_categories = products['product_category_name'].value_counts().head(5).index
products_top5 = products[products['product_category_name'].isin(top5_categories)]

plt.figure(figsize=(12,6))
parallel_coordinates(products_top5[['product_category_name', 'product_weight_g',
                                   'product_length_cm','product_height_cm','product_width_cm']],
                     class_column='product_category_name', colormap=plt.get_cmap("Set1"))
plt.title("Parallel Coordinates Plot of Product Features by Category")
plt.show()

# Step 7: Correlation Heatmap
# ----------------------------
sns.heatmap(products.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm")
plt.title("Correlation between numeric product features")
plt.show()

# ----------------------------
# Step 8: Save cleaned/EDA datasets
# ----------------------------
eda_dir = r"C:\Users\nisch\Downloads\Mini project\Ecommerce-Analysis\eda"
os.makedirs(eda_dir, exist_ok=True)

orders_customers.to_csv(os.path.join(eda_dir, "orders_customers.csv"), index=False)
products.to_csv(os.path.join(eda_dir, "products_clean.csv"), index=False)
customers.to_csv(os.path.join(eda_dir, "customers_clean.csv"), index=False)

print("EDA-ready datasets saved successfully!")


