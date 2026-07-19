import pandas as pd

def load_data(file_path):
 # Load Dataset
    df = pd.read_csv(file_path , encoding="cp1252")

    df.columns= df.columns.str.strip()
    # Convert Date Columns
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Date Features
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()
    df["Quarter"] = df["Order Date"].dt.quarter
    df["Weekday"] = df["Order Date"].dt.day_name()

# Business Features
    df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100
    df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df