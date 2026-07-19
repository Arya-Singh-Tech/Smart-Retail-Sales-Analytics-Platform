from preprocessing import load_data
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

file_path = "dataset/Sample - Superstore.csv"

df = load_data(file_path)

# Sales by Category
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
category_sales.plot(kind="bar", color="skyblue")

plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.show()

# Top 10 Products by Sales

top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
top_products.plot(kind="bar", color="orange")

plt.title("Top 10 Products by Sales")
plt.xlabel("Product Name")
plt.ylabel("Sales")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()

# Sales by Region

region_sales = df.groupby("Region")["Sales"].sum()

plt.figure(figsize=(7,5))
region_sales.plot(kind="pie", autopct="%1.1f%%")

plt.title("Sales Distribution by Region")
plt.ylabel("")

plt.show()

fig = px.bar(
    df,
    x="Category",
    y="Sales",
    color="Category",
    title="Interactive Sales by Category"
)

fig.show()

#Sales Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["Sales"], bins=30, kde=True)
plt.title("Sales Distribution")
plt.show()

#Correlation Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(
    df[["Sales","Profit","Quantity","Discount"]].corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.show()