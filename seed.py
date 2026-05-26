import pandas as pd
from app import app, db
# import your models, e.g.:
# from models import Product, StockRecord, Site

def seed_from_excel():
    with app.app_context():
        db.create_all()
        df = pd.read_excel('INVO_Dataset.xlsx')
        
        # Example — adapt to your actual model/columns:
        # for _, row in df.iterrows():
        #     product = Product(name=row['ProductName'], ...)
        #     db.session.add(product)
        
        db.session.commit()
        print("Seeded successfully!")

if __name__ == '__main__':
    seed_from_excel()