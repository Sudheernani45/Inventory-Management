from models.db import db

class User(db.Model):
    __tablename__ = 'users'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100))
    email          = db.Column(db.String(120), unique=True)
    password       = db.Column(db.String(255))
    role           = db.Column(db.String(20))   # admin / manager / analyst
    is_active      = db.Column(db.Boolean, default=True, nullable=False)
    is_first_login = db.Column(db.Boolean, default=True)
    # Enhanced profile fields
    phone          = db.Column(db.String(20))
    department     = db.Column(db.String(100))
    employee_id    = db.Column(db.String(50), unique=True)
    photo_url      = db.Column(db.String(500))
    created_at     = db.Column(db.DateTime, default=__import__('datetime').datetime.utcnow)

    def to_dict(self):
        return {
            "id":             self.id,
            "name":           self.name,
            "email":          self.email,
            "role":           self.role,
            "is_active":      self.is_active,
            "is_first_login": self.is_first_login,
            "phone":          self.phone,
            "department":     self.department,
            "employee_id":    self.employee_id,
            "photo_url":      self.photo_url,
            "created_at":     self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
        }
