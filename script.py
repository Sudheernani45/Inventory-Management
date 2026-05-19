import pandas as pd
from sqlalchemy import create_engine
from config import config

# IMPORT MODELS ONLY FOR TABLE NAMES
from models.records import (
    Product, Customer, Site, Inventory,
    Logistics, Sale, Promotion, SeasonalPlan,States
)


# DB CONNECTION
# -------------------------------
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)


# COMMON FUNCTIONS
# -------------------------------
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def to_date(series):
    return pd.to_datetime(series, errors="coerce").dt.date


# -------------------------------
# LOAD FUNCTIONS
# -------------------------------

def load_products():
    df = clean_columns(pd.read_csv("archive/Product_Information.csv"))

    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["shelf_life"] = pd.to_numeric(df["shelf_life"], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["product_id"], inplace=True)

    df.to_sql(Product.__tablename__, engine, if_exists="append", index=False)
    print(f" Products loaded ({len(df)} rows)")


def load_customers():
    import numpy as np
    df = clean_columns(pd.read_csv("archive/Customer_Demographics.csv"))

    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["purchase_frequency"] = pd.to_numeric(df["purchase_frequency"], errors="coerce")
    df["average_spend"] = pd.to_numeric(df["average_spend"], errors="coerce")

    # Generate extended fields if not present in CSV
    n = len(df)
    cats = ["Electronics", "Clothing", "Food", "Home", "Sports", "Books", "Beauty"]
    if "preferred_categories" not in df.columns:
        df["preferred_categories"] = [np.random.choice(cats, size=np.random.randint(1,4), replace=False).tolist() for _ in range(n)]
        df["preferred_categories"] = df["preferred_categories"].apply(lambda x: ", ".join(x))
    if "last_purchase_date" not in df.columns:
        dates = pd.date_range("2023-01-01", "2024-12-31", periods=n)
        df["last_purchase_date"] = np.random.choice(dates, n, replace=True)
        df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"]).dt.date
    if "total_spend" not in df.columns:
        df["total_spend"] = (df["average_spend"] * df["purchase_frequency"] * np.random.uniform(1.5, 3.5, n)).round(2)
    if "clv" not in df.columns:
        df["clv"] = (df["total_spend"] * np.random.uniform(2.0, 5.0, n)).round(2)
    if "csat" not in df.columns:
        df["csat"] = np.round(np.random.uniform(2.5, 5.0, n), 1)
    if "nps" not in df.columns:
        df["nps"] = np.random.randint(0, 11, n)

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["customer_id"], inplace=True)

    df.to_sql(Customer.__tablename__, engine, if_exists="append", index=False)
    print(f" Customers loaded ({len(df)} rows)")


def load_sites():
    df = clean_columns(pd.read_csv("archive/Site_Details.csv"))

    df["store_size"] = pd.to_numeric(df["store_size"], errors="coerce")
    df["open_date"] = to_date(df["open_date"])

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["site_id"], inplace=True)

    df.to_sql(Site.__tablename__, engine, if_exists="append", index=False)
    print(f" Sites loaded ({len(df)} rows)")


def load_inventory():
    df = clean_columns(pd.read_csv("archive/Inventory_Data.csv"))

    df["beginning_inventory"] = pd.to_numeric(df["beginning_inventory"], errors="coerce")
    df["ending_inventory"] = pd.to_numeric(df["ending_inventory"], errors="coerce")
    df["replenishment"] = pd.to_numeric(df["replenishment"], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["site_id", "product_id"], inplace=True)

    df.to_sql(Inventory.__tablename__, engine, if_exists="append", index=False)
    print(f" Inventory loaded ({len(df)} rows)")


def load_logistics():
    df = clean_columns(pd.read_csv("archive/Logistics_Data.csv"))

    df["shipment_date"] = to_date(df["shipment_date"])
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["shipment_id"], inplace=True)

    df.to_sql(Logistics.__tablename__, engine, if_exists="append", index=False)
    print(f" Logistics loaded ({len(df)} rows)")


def load_sales():
    df = clean_columns(pd.read_csv("archive/Sales_Data.csv"))

    df["date"] = to_date(df["date"])
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["discounts"] = pd.to_numeric(df["discounts"], errors="coerce")
    df["returns"] = pd.to_numeric(df["returns"], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["date", "site_id", "product_id"], inplace=True)

    df.to_sql(Sale.__tablename__, engine, if_exists="append", index=False)
    print(f" Sales loaded ({len(df)} rows)")


def load_promotions():
    df = clean_columns(pd.read_csv("archive/Promotions_and_Discounts.csv"))

    df["start_date"] = to_date(df["start_date"])
    df["end_date"] = to_date(df["end_date"])
    df["discount_amount"] = pd.to_numeric(df["discount_amount"], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["promotion_id"], inplace=True)

    df.to_sql(Promotion.__tablename__, engine, if_exists="append", index=False)
    print(f" Promotions loaded ({len(df)} rows)")


def load_seasonal_planning():
    df = clean_columns(pd.read_csv("archive/Monthly_Seasonal_Planning.csv"))

    df["forecasted_sales"] = pd.to_numeric(df["forecasted_sales"], errors="coerce")
    df["actual_sales"] = pd.to_numeric(df["actual_sales"], errors="coerce")
    df["seasonal_adjustments"] = pd.to_numeric(df["seasonal_adjustments"], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["month", "site_id"], inplace=True)

    df.to_sql(SeasonalPlan.__tablename__, engine, if_exists="append", index=False)
    print(f" Seasonal Planning loaded ({len(df)} rows)")

def load_states():
    df = clean_columns(pd.read_csv("archive/States.csv"))
    df["state_id"] = pd.to_numeric(df["state_id"], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["state_id"], inplace=True)
    df.to_sql(States.__tablename__, engine, if_exists="append", index=False)
    print(f" States loaded ({len(df)} rows)")

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print(" Loading Data...\n")

    load_products()
    load_customers()
    load_sites()
    load_inventory()
    load_logistics()
    load_sales()
    load_promotions()
    load_seasonal_planning()
    load_states()

    print("\n ALL DATA LOADED SUCCESSFULLY!")