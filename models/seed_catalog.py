"""
seed_catalog.py — populates categories, subcategories, suppliers, and products tables
from the archive CSV files.

Usage (run once after migrations):
    from models.seed_catalog import seed_catalog
    seed_catalog()
"""

import os
import csv
from datetime import datetime
from models.db import db
from models.records import Category, Subcategory, Supplier, Product


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'archive')


def _csv_path(name):
    return os.path.join(DATA_DIR, name)


def seed_categories_suppliers():
    """Seed Category, Subcategory and Supplier tables from Product_Information.csv."""

    # ── Categories & Subcategories ────────────────────────
    cat_map = {}   # category_name -> Category instance
    with open(_csv_path('Product_Information.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat_name = row['Category'].strip()
            sub_name = row['Subcategory'].strip()

            if cat_name not in cat_map:
                existing = Category.query.filter_by(category_name=cat_name).first()
                if not existing:
                    existing = Category(category_name=cat_name)
                    db.session.add(existing)
                    db.session.flush()
                cat_map[cat_name] = existing

            cat_obj = cat_map[cat_name]
            already = Subcategory.query.filter_by(
                category_id=cat_obj.id, subcategory_name=sub_name
            ).first()
            if not already:
                db.session.add(Subcategory(category_id=cat_obj.id, subcategory_name=sub_name))

    db.session.commit()
    print("✓ Categories & Subcategories seeded. (Suppliers are user-managed — not auto-seeded.)")


def seed_products():
    """Load products from Product_Information.csv into the products table."""
    if Product.query.count() > 0:
        print("⚠ Products table already has data — skipping product seed.")
        return

    with open(_csv_path('Product_Information.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            batch.append(Product(
                product_id   = row['Product ID'].strip(),
                product_name = row['Product Name'].strip(),
                category     = row['Category'].strip(),
                subcategory  = row['Subcategory'].strip(),
                unit_cost    = float(row['Unit Cost']) if row['Unit Cost'] else 0,
                unit_price   = float(row['Unit Price']) if row['Unit Price'] else 0,
                supplier     = row['Supplier'].strip(),
                shelf_life   = int(row['Shelf Life']) if row['Shelf Life'] else 0,
            ))
        db.session.bulk_save_objects(batch)
        db.session.commit()
    print(f"✓ Products seeded ({len(batch)} rows).")


def seed_catalog():
    seed_categories_suppliers()
    seed_products()
