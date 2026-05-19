"""
populate_customer_spend.py — Calculate and populate total_spend and average_spend from sales data.
Run once to populate missing customer spend values from actual sales records.

Usage:
    from models.populate_customer_spend import populate_customer_metrics
    populate_customer_metrics()
"""

from models.db import db
from models.records import Customer, Sale
from sqlalchemy import func


def populate_customer_metrics():
    """Calculate total_spend and average_spend for all customers from sales data."""
    
    print("Calculating customer spend metrics from sales data...")
    
    # Get spending summary by customer_id from Sales table
    spend_data = db.session.query(
        Sale.customer_id,
        func.sum(Sale.revenue).label('total'),
        func.count(Sale.id).label('purchase_count'),
        func.avg(Sale.revenue).label('average')
    ).group_by(Sale.customer_id).all()
    
    updated_count = 0
    
    for record in spend_data:
        customer_id = record.customer_id
        total_spend = float(record.total or 0)
        purchase_frequency = int(record.purchase_count or 0)
        average_spend = float(record.average or 0)
        
        # Find customer and update
        customer = Customer.query.filter_by(customer_id=customer_id).first()
        if customer:
            customer.total_spend = total_spend
            customer.average_spend = average_spend
            customer.purchase_frequency = purchase_frequency
            updated_count += 1
    
    db.session.commit()
    print(f"✓ Updated {updated_count} customers with spend metrics from sales data")


if __name__ == "__main__":
    populate_customer_metrics()
