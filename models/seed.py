from werkzeug.security import generate_password_hash
from models.user import User
from models.db import db

def create_admin():
    existing = User.query.filter_by(email="admin@inventory.com").first()

    if not existing:
        admin = User(
            name="Admin",
            email="admin@inventory.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        