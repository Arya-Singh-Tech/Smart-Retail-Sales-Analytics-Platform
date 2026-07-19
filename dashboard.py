import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from database import create_database, run_query

# ---------------------------
# Page Configuration
# ---------------------------

st.set_page_config(
    page_title="Smart Retail Sales Analytics Platform",
    layout="wide"
)

# ---------------------------
# Load Dataset
# ---------------------------

file_path = "dataset/Sample - Superstore.csv"

df = pd.read_csv(file_path, encoding="cp1252")

# Convert Date

df["Order Date"] = pd.to_datetime(df["Order Date"])

# Create New Columns

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
create_database(df)
# ---------------------------
# Dashboard Title
# ---------------------------

st.title("📊 Smart Retail Sales Analytics Platform")
st.markdown("---")



# ---------------------------
# Sidebar Filters
# ---------------------------

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)


filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region)) &
    (df["Segment"].isin(segment))
]
query = """
SELECT Category,
       SUM(Sales) AS Sales
FROM sales
WHERE 1=1
"""

params = []

if category:
    placeholders = ",".join(["?"] * len(category))
    query += f" AND Category IN ({placeholders})"
    params.extend(category)

if region:
    placeholders = ",".join(["?"] * len(region))
    query += f" AND Region IN ({placeholders})"
    params.extend(region)

if segment:
    placeholders = ",".join(["?"] * len(segment))
    query += f" AND Segment IN ({placeholders})"
    params.extend(segment)

query += """
GROUP BY Category
"""

category_sales = run_query(query, params)

# -----------------------------
# SQL KPI Query
# -----------------------------

query = """
SELECT
    SUM(Sales) AS TotalSales,
    SUM(Profit) AS TotalProfit,
    COUNT(*) AS TotalOrders
FROM sales
WHERE 1=1
"""

params = []

if category:
    placeholders = ",".join(["?"] * len(category))
    query += f" AND Category IN ({placeholders})"
    params.extend(category)

if region:
    placeholders = ",".join(["?"] * len(region))
    query += f" AND Region IN ({placeholders})"
    params.extend(region)

if segment:
    placeholders = ",".join(["?"] * len(segment))
    query += f" AND Segment IN ({placeholders})"
    params.extend(segment)

kpi = run_query(query, params)

total_sales = kpi.loc[0, "TotalSales"]
total_profit = kpi.loc[0, "TotalProfit"]
total_orders = kpi.loc[0, "TotalOrders"]
profit_margin = (total_profit / total_sales) * 100

# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${total_sales:,.2f}")
c2.metric("🧾 Total Profit", f"${total_profit:,.2f}")
c3.metric("📦 Total Orders", f"{total_orders:,}")
c4.metric("📈 Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")
# ---------------------------
# Charts
# ---------------------------

col1, col2 = st.columns(2)

# Chart 1 - Sales by Category
with col1:

    st.subheader("📊 Sales by Category")

    query = """
    SELECT Category,
       SUM(Sales) AS Sales
    FROM sales
    WHERE 1=1
    """

    params = []

    if category:
     placeholders = ",".join(["?"] * len(category))
     query += f" AND Category IN ({placeholders})"
     params.extend(category)

    if region:
     placeholders = ",".join(["?"] * len(region))
     query += f" AND Region IN ({placeholders})"
     params.extend(region)

    if segment:
     placeholders = ",".join(["?"] * len(segment))
     query += f" AND Segment IN ({placeholders})"
     params.extend(segment)

    query += """
    GROUP BY Category
    """

    category_sales = run_query(query, params)
    fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
     )
    
    st.plotly_chart(fig, use_container_width=True)


# Chart 2 - Sales by Region
with col2:

    st.subheader("🌍 Sales by Region")

    query = """
    SELECT Region,
       SUM(Sales) AS Sales
    FROM sales
    WHERE 1=1
    """

    params = []

    if category:
      placeholders = ",".join(["?"] * len(category))
      query += f" AND Category IN ({placeholders})"
      params.extend(category)

    if region:
      placeholders = ",".join(["?"] * len(region))
      query += f" AND Region IN ({placeholders})"
      params.extend(region)

    if segment:
      placeholders = ",".join(["?"] * len(segment))
      query += f" AND Segment IN ({placeholders})"
      params.extend(segment)

    query += """
    GROUP BY Region
    """

    region_sales = run_query(query, params)

    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
     )
    
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

# Chart 3 - Monthly Sales Trend
with col3:
    st.markdown("---")
    st.subheader("📈 Monthly Sales Trend")

    query = """
    SELECT [Month],
       SUM(Sales) AS Sales
    FROM sales
    WHERE 1=1
    """

    params = []

    if category:
     placeholders = ",".join(["?"] * len(category))
     query += f" AND Category IN ({placeholders})"
     params.extend(category)

    if region:
     placeholders = ",".join(["?"] * len(region))
     query += f" AND Region IN ({placeholders})"
     params.extend(region)

    if segment:
     placeholders = ",".join(["?"] * len(segment))
     query += f" AND Segment IN ({placeholders})"
     params.extend(segment)

    query += """
    GROUP BY [Month]
    """

    monthly_sales = run_query(query, params)
    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
       )
    
    st.plotly_chart(fig, use_container_width=True)


# Chart 4 - Top 10 Products
with col4:
    st.markdown("---")
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products"
    )
   
    st.plotly_chart(fig, use_container_width=True)

col5,col6=st.columns(2)
# Chart 5 - Profit vs Discount
with col5:
  st.markdown("---")
  st.subheader("💰 Profit vs Discount")

  fig = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    title="Profit vs Discount"
  )

  st.plotly_chart(fig, use_container_width=True)

#Chart6-Sales by Segment
with col6:
  st.markdown("---")
  st.subheader("🥧 Sales by Segment")

  segment_sales = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
  )

  fig = px.pie(
    segment_sales,
    names="Segment",
    values="Sales",
    title="Sales Distribution by Segment",
    hole=0.4
   )

  st.plotly_chart(fig, use_container_width=True)

 #Chart 7-Year-wise Sales
st.markdown("---")
st.subheader("📅 Year-wise Sales")

year_sales = run_query("""
SELECT
    Year,
    SUM(Sales) AS Sales
FROM sales
GROUP BY Year
ORDER BY Year
""")

fig = px.bar(
    year_sales,
    x="Year",
    y="Sales",
    color="Year",
    title="Year-wise Sales"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MACHINE LEARNING
# =========================

st.markdown("---")
# Machine Learning

ml_df = filtered_df[[
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
    "Year",
    "Month"
]]

X = ml_df[[
    "Quantity",
    "Discount",
    "Profit",
    "Year",
    "Month"
]]

y = ml_df["Sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

mae = mean_absolute_error(y_test, prediction)
r2 = r2_score(y_test, prediction)

st.subheader("🤖 Machine Learning Performance")

col1, col2 = st.columns(2)

col1.metric("MAE", round(mae, 2))
col2.metric("R² Score", round(r2, 2))

# =========================
# FILTERED DATASET
# =========================

st.markdown("---")
st.subheader("📄 Filtered Dataset")

st.dataframe(filtered_df)

st.markdown("---")
st.subheader("📥 Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# =========================
# SALES PREDICTION
# =========================

st.markdown("---")
st.subheader("🔮 Predict Future Sales")

quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=2
)

discount = st.slider(
    "Discount",
    0.0,
    1.0,
    0.0
)

profit = st.number_input(
    "Profit",
    value=100.0
)

year = st.selectbox(
    "Year",
    sorted(df["Year"].unique())
)

month = st.selectbox(
    "Month",
    sorted(df["Month"].unique())
)

if st.button("Predict Sales"):

    input_data = [[
        quantity,
        discount,
        profit,
        year,
        month
    ]]

    predicted_sales = model.predict(input_data)[0]

    st.success(f"💰 Predicted Sales: ${predicted_sales:.2f}")

    st.markdown("---")
st.subheader("📌 Dashboard Summary")

st.info(f"""
Total Sales : ${filtered_df['Sales'].sum():,.2f}

Total Profit : ${filtered_df['Profit'].sum():,.2f}

Total Orders : {len(filtered_df)}

Average Discount : {filtered_df['Discount'].mean():.2f}
""")
st.markdown("---")
st.markdown(
    """
    <center>
    <h4>📊 Smart Retail Sales Analytics Platform</h4>
    <p>Developed using Python | SQL | Pandas | Plotly | Streamlit | Scikit-learn</p>
    <p>📈 Includes a Power BI dashboard for Business Intelligence Reporting</p>
    </center>
    """,
    unsafe_allow_html=True
)
