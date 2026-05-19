from models.db import db

class Manager(db.Model):
    __tablename__ = 'managers'

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    site_id = db.Column(db.String, db.ForeignKey('sites.site_id'), nullable=True)

    user = db.relationship('User', backref=db.backref('manager', uselist=False))

    def to_dict(self):
        return {
            "id":      self.id,
            "user_id": self.user_id,
            "name":    self.user.name  if self.user else "",
            "email":   self.user.email if self.user else "",
            "site_id": self.site_id
        }
