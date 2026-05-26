"""
seed.py — seeds all tables from INVO_Dataset.xlsx
Run automatically as part of Render build command:
    pip install -r requirements.txt && python seed.py
"""
 
import os
import pandas as pd
from datetime import datetime
from app import app, db
from models.records import (
    Category, Subcategory, Supplier, Product,
    Site, Inventory, Customer, Promotion, SeasonalPlan, Logistics, States
)
from models.user import User
from werkzeug.security import generate_password_hash
 
XLSX = os.path.join(os.path.dirname(__file__), 'INVO_Dataset.xlsx')
 
def safe_str(val):
    return str(val).strip() if pd.notna(val) else None
 
def safe_int(val):
    try:
        return int(val) if pd.notna(val) else None
    except:
        return None
 
def safe_float(val):
    try:
        return float(val) if pd.notna(val) else None
    except:
        return None
 
def safe_date(val):
    if pd.isna(val):
        return None
    try:
        return pd.to_datetime(val).date()
    except:
        return None
 
def seed_states(xl):
    if States.query.count() > 0:
        print("⚠ States already seeded — skipping.")
        return
    df = xl.parse('States')
    batch = []
    for _, row in df.iterrows():
        batch.append(States(state_name=safe_str(row['state_name'])))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ States seeded ({len(batch)} rows).")
 
def seed_categories(xl):
    if Category.query.count() > 0:
        print("⚠ Categories already seeded — skipping.")
        return
    df = xl.parse('Product_Information')
    cat_map = {}
    for _, row in df.iterrows():
        cat_name = safe_str(row['Category'])
        sub_name = safe_str(row['Subcategory'])
        if not cat_name:
            continue
        if cat_name not in cat_map:
            cat = Category(category_name=cat_name)
            db.session.add(cat)
            db.session.flush()
            cat_map[cat_name] = cat
        cat_obj = cat_map[cat_name]
        db.session.add(Subcategory(category_id=cat_obj.id, subcategory_name=sub_name))
    db.session.commit()
    print(f"✓ Categories & Subcategories seeded ({len(cat_map)} categories).")
 
def seed_suppliers(xl):
    if Supplier.query.count() > 0:
        print("⚠ Suppliers already seeded — skipping.")
        return
    df = xl.parse('suppliers')
    batch = []
    for i, row in df.iterrows():
        batch.append(Supplier(
            supplier_id   = safe_str(row.get('supplier_pk', f'SUP{i:04d}')),
            supplier_name = safe_str(row['supplier_name']),
            email         = safe_str(row.get('email')),
            phone         = safe_str(row.get('phone')),
            status        = 'Active',
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Suppliers seeded ({len(batch)} rows).")
 
def seed_products(xl):
    if Product.query.count() > 0:
        print("⚠ Products already seeded — skipping.")
        return
    df = xl.parse('Product_Information')
    batch = []
    for _, row in df.iterrows():
        batch.append(Product(
            product_id   = safe_str(row['Product ID']),
            product_name = safe_str(row['Product Name']),
            category     = safe_str(row['Category']),
            subcategory  = safe_str(row['Subcategory']),
            unit_cost    = safe_float(row['Unit Cost']),
            unit_price   = safe_float(row['Unit Price']),
            supplier     = safe_str(row['Supplier']),
            shelf_life   = safe_int(row['Shelf Life']),
            status       = 'Active',
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Products seeded ({len(batch)} rows).")
 
def seed_sites(xl):
    if Site.query.count() > 0:
        print("⚠ Sites already seeded — skipping.")
        return
    df = xl.parse('Site_Details')
    batch = []
    for _, row in df.iterrows():
        batch.append(Site(
            site_id     = safe_str(row['Site ID']),
            site_name   = safe_str(row['Site Name']),
            site_format = safe_str(row['Site Format']),
            region      = safe_str(row['Region']),
            city        = safe_str(row['City']),
            state_id    = safe_int(row['State_id']),
            store_size  = safe_int(row['Store Size']),
            open_date   = safe_date(row['Open Date']),
            status      = safe_str(row['Status']),
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Sites seeded ({len(batch)} rows).")
 
def seed_customers(xl):
    if Customer.query.count() > 0:
        print("⚠ Customers already seeded — skipping.")
        return
    df = xl.parse('Customer_Demographics')
    batch = []
    for _, row in df.iterrows():
        batch.append(Customer(
            customer_id        = safe_str(row['Customer ID']),
            age                = safe_int(row['Age']),
            gender             = safe_str(row['Gender']),
            income_bracket     = safe_str(row['Income Bracket']),
            purchase_frequency = safe_int(row['Purchase Frequency']),
            average_spend      = safe_float(row['Average Spend']),
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Customers seeded ({len(batch)} rows).")
 
def seed_inventory(xl):
    if Inventory.query.count() > 0:
        print("⚠ Inventory already seeded — skipping.")
        return
    df = xl.parse('Inventory_Data')
    batch = []
    for _, row in df.iterrows():
        batch.append(Inventory(
            site_id             = safe_str(row['Site ID']),
            product_id          = safe_str(row['Product ID']),
            beginning_inventory = safe_int(row['Beginning Inventory']),
            ending_inventory    = safe_int(row['Ending Inventory']),
            replenishment       = safe_int(row['Replenishment']),
            stockout_flag       = safe_str(row['Stockout Flag']),
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Inventory seeded ({len(batch)} rows).")
 
def seed_promotions(xl):
    if Promotion.query.count() > 0:
        print("⚠ Promotions already seeded — skipping.")
        return
    df = xl.parse('Promotions_and_Discounts')
    batch = []
    for _, row in df.iterrows():
        batch.append(Promotion(
            promotion_id    = safe_str(row['Promotion ID']),
            product_id      = safe_str(row['Product ID']),
            site_id         = safe_str(row['Site ID']),
            start_date      = safe_date(row['Start Date']),
            end_date        = safe_date(row['End Date']),
            discount_type   = safe_str(row['Discount Type']),
            discount_amount = safe_float(row['Discount Amount']),
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Promotions seeded ({len(batch)} rows).")
 
def seed_logistics(xl):
    if Logistics.query.count() > 0:
        print("⚠ Logistics already seeded — skipping.")
        return
    df = xl.parse('Logistics_Data')
    batch = []
    for i, row in df.iterrows():
        batch.append(Logistics(
            shipment_id         = safe_str(row['Seament ID']),
            site_id             = safe_str(row['Site ID']),
            product_id          = safe_str(row['Product ID']),
            shipment_date       = safe_date(row['Seament Date']),
            quantity            = safe_int(row['Quantity']),
            delivery_status     = safe_str(row['Delivery Status']),
            transportation_type = safe_str(row['Transportation Type']),
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Logistics seeded ({len(batch)} rows).")
 
def seed_seasonal(xl):
    if SeasonalPlan.query.count() > 0:
        print("⚠ Seasonal plans already seeded — skipping.")
        return
    df = xl.parse('Monthly_Seasonal_Planning')
    batch = []
    for _, row in df.iterrows():
        batch.append(SeasonalPlan(
            month                = safe_str(row['Month']),
            site_id              = safe_str(row['Site ID']),
            product_category     = safe_str(row['Product Category']),
            forecasted_sales     = safe_float(row['Forecasted Sales']),
            actual_sales         = safe_float(row['Actual Sales']),
            seasonal_adjustments = safe_float(row['Seasonal Adjustments']),
        ))
    db.session.bulk_save_objects(batch)
    db.session.commit()
    print(f"✓ Seasonal plans seeded ({len(batch)} rows).")
 
def seed_admin():
    if User.query.filter_by(email="admin@invexa.com").first():
        print("⚠ Admin already exists — skipping.")
        return
    admin = User(
        name     = "Admin",
        email    = "admin@invexa.com",
        password = generate_password_hash("admin123"),
        role     = "admin"
    )
    db.session.add(admin)
    db.session.commit()
    print("✓ Admin user seeded (admin@invexa.com / admin123).")
 
def run():
    with app.app_context():
        db.create_all()
        print(f"\n📦 Loading {XLSX} ...")
        xl = pd.ExcelFile(XLSX)
 
        seed_states(xl)
        seed_categories(xl)
        seed_suppliers(xl)
        seed_products(xl)
        seed_sites(xl)
        seed_customers(xl)
        seed_inventory(xl)
        seed_promotions(xl)
        seed_logistics(xl)
        seed_seasonal(xl)
        seed_admin()
        print("\n✅ All seeding complete!\n")
 
if __name__ == '__main__':
    run()