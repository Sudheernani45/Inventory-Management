from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Text, Boolean, Index
from models.db import db
from datetime import datetime, timedelta


# ── Category & Subcategory ────────────────────────────────
class Category(db.Model):
    __tablename__ = "categories"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, unique=True, nullable=False)

    subcategories = db.relationship('Subcategory', backref='category', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "subcategories": [s.to_dict() for s in self.subcategories]
        }


class Subcategory(db.Model):
    __tablename__ = "subcategories"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    category_id      = Column(Integer, ForeignKey('categories.id'), nullable=False)
    subcategory_name = Column(String, nullable=False)

    def to_dict(self):
        return {"id": self.id, "subcategory_name": self.subcategory_name, "category_id": self.category_id}


# ── Supplier ──────────────────────────────────────────────
class Supplier(db.Model):
    __tablename__ = "suppliers"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id    = Column(String, unique=True, nullable=False)
    supplier_name  = Column(String, nullable=False)
    email          = Column(String)
    phone          = Column(String)
    address        = Column(Text)
    contact_person = Column(String)
    category       = Column(String)
    status         = Column(String, default='Active')   # Active | Inactive
    notes          = Column(Text)
    created_at     = Column(DateTime, default=datetime.utcnow)
    updated_at     = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":             self.id,
            "supplier_id":    self.supplier_id,
            "supplier_name":  self.supplier_name,
            "email":          self.email or "",
            "phone":          self.phone or "",
            "address":        self.address or "",
            "contact_person": self.contact_person or "",
            "category":       self.category or "",
            "status":         self.status or "Active",
            "notes":          self.notes or "",
            "created_at":     self.created_at.isoformat() if self.created_at else None,
            "updated_at":     self.updated_at.isoformat() if self.updated_at else None,
        }


#  Product_Information.csv 
class Product(db.Model):
    __tablename__ = "products"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    product_id        = Column(String, unique=True, nullable=False)
    product_name      = Column(String)
    category          = Column(String)
    subcategory       = Column(String)
    unit_cost         = Column(Float,   server_default='0')
    unit_price        = Column(Float,   server_default='0')
    supplier          = Column(String)
    shelf_life        = Column(Integer)
    # ── New fields ──────────────────────────────────────────
    uom               = Column(String(30),  server_default='Unit')
    reorder_point     = Column(Integer,     server_default='0')
    reorder_qty       = Column(Integer,     server_default='0')
    default_warehouse = Column(String(20))
    status            = Column(String(20),  server_default='Active')
    created_at        = Column(DateTime,    default=datetime.utcnow)
    updated_at        = Column(DateTime,    default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        unit_cost  = float(self.unit_cost  or 0)
        unit_price = float(self.unit_price or 0)
        margin = round((unit_price - unit_cost) / unit_price * 100, 2) if unit_price > 0 else 0.0
        return {
            "id":                self.id,
            "product_id":        self.product_id,
            "product_name":      self.product_name,
            "category":          self.category,
            "subcategory":       self.subcategory,
            "uom":               self.uom or 'Unit',
            "unit_cost":         round(unit_cost, 2),
            "unit_price":        round(unit_price, 2),
            "supplier":          self.supplier,
            "shelf_life":        self.shelf_life,
            "reorder_point":     self.reorder_point or 0,
            "reorder_qty":       self.reorder_qty   or 0,
            "default_warehouse": self.default_warehouse,
            "status":            self.status or 'Active',
            "margin":            margin,
            "created_at":        self.created_at.isoformat() if self.created_at else None,
        }

 
# Customer_Demographics.csv
class Customer(db.Model):
    __tablename__ = "customers"

    id                    = Column(Integer, primary_key=True, autoincrement=True)
    customer_id           = Column(String, unique=True, nullable=False)
    age                   = Column(Integer)
    gender                = Column(String)
    income_bracket        = Column(String)
    purchase_frequency    = Column(Integer)
    average_spend         = Column(Float)
    preferred_categories  = Column(String)
    last_purchase_date    = Column(Date)
    total_spend           = Column(Float)
    clv                   = Column(Float)   # Customer Lifetime Value
    csat                  = Column(Float)   # Customer Satisfaction Score
    nps                   = Column(Integer) # Net Promoter Score

    def to_dict(self):
        return {
            "id":                   self.id,
            "customer_id":          self.customer_id,
            "age":                  self.age,
            "gender":               self.gender,
            "income_bracket":       self.income_bracket,
            "purchase_frequency":   self.purchase_frequency,
            "average_spend":        float(self.average_spend or 0),
            "preferred_categories": self.preferred_categories,
            "last_purchase_date":   str(self.last_purchase_date) if self.last_purchase_date else None,
            "total_spend":          float(self.total_spend or 0),
            "clv":                  float(self.clv or 0),
            "csat":                 float(self.csat or 0),
            "nps":                  self.nps,
        }


# Site_Details.csv
class Site(db.Model):
    __tablename__ = "sites"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    site_id     = Column(String, unique=True, nullable=False)
    site_name   = Column(String)
    site_format = Column(String)
    region      = Column(String)
    city        = Column(String)
    state_id    = Column(Integer)
    store_size  = Column(Integer)
    open_date   = Column(Date)
    status      = Column(String)


# Inventory_Data.csv
class Inventory(db.Model):
    __tablename__ = "inventory"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    site_id              = Column(String, nullable=False)
    product_id           = Column(String, nullable=False)
    beginning_inventory  = Column(Integer)
    ending_inventory     = Column(Integer)
    replenishment        = Column(Integer)
    stockout_flag        = Column(String)   


# Logistics_Data.csv
class Logistics(db.Model):
    __tablename__ = "logistics"

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id             = Column(String, unique=True, nullable=False)
    site_id                 = Column(String, index=True)
    product_id              = Column(String, index=True)
    shipment_date           = Column(Date,   index=True)
    quantity                = Column(Integer)
    delivery_status         = Column(String, index=True)
    transportation_type     = Column(String, index=True)
    delivery_date           = Column(String, default='')
    # SO-link and tracking columns
    so_id                   = Column(Integer, ForeignKey('sales_orders.id'), nullable=True)
    so_number               = Column(String(50),  nullable=True)
    estimated_delivery      = Column(Date,         nullable=True)
    tracking_status_updated = Column(DateTime,     nullable=True)
    tracking_notes          = Column(Text,         nullable=True)

    __table_args__ = (
        Index('ix_logistics_status_date',   'delivery_status', 'shipment_date'),
        Index('ix_logistics_product_site',  'product_id',      'site_id'),
    )

    def to_dict(self):
        return {
            "id":                      self.id,
            "shipment_id":             self.shipment_id,
            "site_id":                 self.site_id,
            "product_id":              self.product_id,
            "shipment_date":           str(self.shipment_date) if self.shipment_date else None,
            "quantity":                self.quantity,
            "delivery_status":         self.delivery_status,
            "transportation_type":     self.transportation_type,
            "delivery_date":           self.delivery_date or '',
            "so_id":                   self.so_id,
            "so_number":               self.so_number,
            "estimated_delivery":      str(self.estimated_delivery) if self.estimated_delivery else None,
            "tracking_status_updated": self.tracking_status_updated.isoformat() if self.tracking_status_updated else None,
            "tracking_notes":          self.tracking_notes or '',
        }


# Sales_Data.csv
class Sale(db.Model):
    __tablename__ = "sales"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    date        = Column(Date)
    site_id     = Column(String)
    product_id  = Column(String)
    units_sold  = Column(Integer)
    revenue     = Column(Float)
    discounts   = Column(Float)
    returns     = Column(Integer)
    customer_id = Column(String)


# Promotions_and_Discounts.csv 
class Promotion(db.Model):
    __tablename__ = "promotions"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    promotion_id    = Column(String, unique=True, nullable=False)
    product_id      = Column(String)
    site_id         = Column(String)
    start_date      = Column(Date)
    end_date        = Column(Date)
    discount_type   = Column(String)
    discount_amount = Column(Float)


# Monthly_Seasonal_Planning.csv
class SeasonalPlan(db.Model):
    __tablename__ = "seasonal_planning"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    month                = Column(String)   
    site_id              = Column(String)
    product_category     = Column(String)
    forecasted_sales     = Column(Float)
    actual_sales         = Column(Float)
    seasonal_adjustments = Column(Float)

class States(db.Model):
    __tablename__ = "States"

    state_id             = Column(Integer, primary_key=True, autoincrement=True)
    state_name              = Column(String)

# ── AuditLog ──────────────────────────────────────────────
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    timestamp  = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    user       = Column(String, nullable=False, default='system')
    user_role  = Column(String, default='')
    action     = Column(String, nullable=False)   # CREATE, UPDATE, DELETE, LOGIN, LOGOUT, VIEW, EXPORT
    module     = Column(String, nullable=False)   # Users, Products, Shipments …
    resource   = Column(String, default='')       # e.g. "Product PRD10001"
    detail     = Column(Text, default='')
    ip_address = Column(String, default='')

    def to_dict(self):
        return {
            "id":         self.id,
            "timestamp":  (self.timestamp.replace(tzinfo=None) + timedelta(hours=5, minutes=30)).strftime('%d %b %Y, %I:%M %p IST') if self.timestamp else '',
            "user":       self.user,
            "user_role":  self.user_role,
            "action":     self.action,
            "module":     self.module,
            "resource":   self.resource,
            "detail":     self.detail,
            "ip_address": self.ip_address,
        }


# ── StockLevel ────────────────────────────────────────────
class StockLevel(db.Model):
    """Current stock on hand per product per warehouse (site)."""
    __tablename__ = "stock_levels"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    site_id       = Column(String(20), nullable=False)
    product_id    = Column(String(50), nullable=False)
    qty_on_hand   = Column(Integer, default=0, nullable=False)
    reorder_point = Column(Integer, default=0)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('site_id', 'product_id', name='uq_stock_site_product'),)

    def to_dict(self):
        return {
            "id":            self.id,
            "site_id":       self.site_id,
            "product_id":    self.product_id,
            "qty_on_hand":   self.qty_on_hand,
            "reorder_point": self.reorder_point,
            "updated_at":    self.updated_at.isoformat() if self.updated_at else None,
        }


# ── StockMovement ─────────────────────────────────────────
class StockMovement(db.Model):
    """Audit trail of every stock change (PurchaseIn, SaleOut, Adjustment)."""
    __tablename__ = "stock_movements"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    site_id       = Column(String(20), nullable=False)
    product_id    = Column(String(50), nullable=False)
    movement_type = Column(String(30), nullable=False)   # PurchaseIn | SaleOut | Adjustment
    qty_change    = Column(Integer, nullable=False)       # positive = in, negative = out
    reference_id  = Column(String(50))                   # PO# or SO# that triggered this
    remarks       = Column(Text)
    created_by    = Column(Integer, ForeignKey('users.id'))
    created_at    = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":            self.id,
            "site_id":       self.site_id,
            "product_id":    self.product_id,
            "movement_type": self.movement_type,
            "qty_change":    self.qty_change,
            "reference_id":  self.reference_id,
            "remarks":       self.remarks,
            "created_by":    self.created_by,
            "created_at":    self.created_at.isoformat() if self.created_at else None,
        }


# ── PurchaseOrder (DB-backed) ─────────────────────────────
class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    po_number         = Column(String, unique=True, nullable=False)
    supplier          = Column(String, default='')
    supplier_id       = Column(Integer, ForeignKey('suppliers.id'), nullable=True)
    product_name      = Column(String, default='')
    product_id        = Column(String, default='')
    quantity          = Column(Integer, default=0)
    unit_cost         = Column(Float, default=0)
    total_cost        = Column(Float, default=0)
    site              = Column(String, default='')
    notes             = Column(Text, default='')
    expected_delivery = Column(String, default='')
    created_at        = Column(String, default='')
    created_by        = Column(String, default='')
    # Status: Draft | Pending | Approved | Received | Cancelled
    status            = Column(String, default='Draft')
    approved_at       = Column(String, default='')
    approved_by       = Column(String, default='')
    rejection_reason  = Column(Text, default='')
    received_at       = Column(String, default='')
    cancelled_at      = Column(String, default='')
    cancel_reason     = Column(Text, default='')
    role              = Column(String, default='admin')    # admin or manager
    manager_user_id   = Column(Integer, default=0)
    # Supplier email approval token fields
    supplier_approval_token = Column(String(128), unique=True, nullable=True)
    supplier_token_expiry   = Column(DateTime, nullable=True)
    supplier_action         = Column(String(20), nullable=True)   # approved | rejected | pending
    supplier_actioned_at    = Column(DateTime, nullable=True)
    supplier_reject_reason  = Column(Text, nullable=True)

    supplier_rel = db.relationship('Supplier', foreign_keys=[supplier_id])

    def to_dict(self):
        # Safe supplier relationship access — FK may not exist in older DBs
        try:
            sup_name  = self.supplier_rel.supplier_name if self.supplier_rel else None
            sup_email = self.supplier_rel.email         if self.supplier_rel else None
        except Exception:
            sup_name  = None
            sup_email = None
        return {
            "po_number":         self.po_number,
            "supplier":          self.supplier,
            "supplier_id":       self.supplier_id,
            "supplier_name":     sup_name,
            "supplier_email":    sup_email,
            "product_name":      self.product_name,
            "product_id":        self.product_id,
            "quantity":          self.quantity,
            "unit_cost":         self.unit_cost,
            "total_cost":        self.total_cost,
            "status":            self.status,
            "site":              self.site,
            "notes":             getattr(self, 'notes', '') or '',
            "expected_delivery": self.expected_delivery,
            "created_at":        self.created_at,
            "created_by":        self.created_by,
            "approved_at":       self.approved_at,
            "approved_by":       getattr(self, 'approved_by', '') or '',
            "rejection_reason":  getattr(self, 'rejection_reason', '') or '',
            "received_at":       getattr(self, 'received_at', '') or '',
            "cancelled_at":      getattr(self, 'cancelled_at', '') or '',
            "cancel_reason":     getattr(self, 'cancel_reason', '') or '',
            "supplier_action":   getattr(self, 'supplier_action', None),
            "supplier_actioned_at": (self.supplier_actioned_at.isoformat()
                                     if getattr(self, 'supplier_actioned_at', None) else None),
        }


# ── SalesOrder (DB-backed) ────────────────────────────────
class SalesOrder(db.Model):
    __tablename__ = "sales_orders"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    so_number       = Column(String, unique=True, nullable=False)
    customer        = Column(String, default='')
    customer_id     = Column(String, default='')
    customer_email  = Column(String, default='')
    state           = Column(String, default='')
    site            = Column(String, default='')          # warehouse / site_id
    items_json      = Column(Text, default='[]')          # JSON string of items list
    total_amount    = Column(Float, default=0)
    notes           = Column(Text, default='')
    dispatch_type   = Column(String, default='Truck')
    # Status: Pending | Confirmed | Dispatched | Delivered | Cancelled
    status          = Column(String, default='Pending')
    created_at      = Column(String, default='')
    created_by      = Column(String, default='')
    confirmed_at    = Column(String, default='')
    dispatched_at   = Column(String, default='')
    cancelled_at    = Column(String, default='')
    cancel_reason   = Column(Text, default='')
    role            = Column(String, default='admin')
    manager_user_id = Column(Integer, default=0)

    def to_dict(self):
        import json as _json
        try:
            items = _json.loads(self.items_json or '[]')
        except Exception:
            items = []
        return {
            "so_number":      self.so_number,
            "customer":       self.customer,
            "customer_id":    self.customer_id,
            "customer_email": self.customer_email,
            "state":          self.state,
            "site":           self.site,
            "items":          items,
            "total_amount":   self.total_amount,
            "notes":          self.notes,
            "status":         self.status,
            "dispatch_type":  self.dispatch_type,
            "created_at":     self.created_at,
            "created_by":     self.created_by,
            "confirmed_at":   self.confirmed_at,
            "dispatched_at":  self.dispatched_at,
            "cancelled_at":   self.cancelled_at,
            "cancel_reason":  self.cancel_reason,
        }


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String, default='')
    email      = Column(String, default='')
    company    = Column(String, default='')
    subject    = Column(String, default='')
    message    = Column(Text, default='')
    is_read    = Column(db.Boolean, default=False)
    created_at = Column(String, default='')

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'email':      self.email,
            'company':    self.company,
            'subject':    self.subject,
            'message':    self.message,
            'is_read':    self.is_read,
            'created_at': self.created_at,
        }


# ── SalesReturn ────────────────────────────────────────────
class SalesReturn(db.Model):
    """Return of goods from a delivered Sales Order."""
    __tablename__ = "sales_returns"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    return_number   = Column(String(50), unique=True, nullable=False)
    so_number       = Column(String(50), nullable=False)          # reference to original SO
    customer        = Column(String(150), default='')
    site            = Column(String(50), default='')
    return_reason   = Column(Text, default='')
    items_json      = Column(Text, default='[]')                  # [{product_id, product_name, qty, unit_price}]
    total_refund    = Column(Float, default=0)
    status          = Column(String(30), default='Pending')       # Pending | Approved | Rejected | Processed
    notes           = Column(Text, default='')
    created_at      = Column(String(20), default='')
    created_by      = Column(String(80), default='')
    approved_at     = Column(String(20), default='')
    approved_by     = Column(String(80), default='')
    role            = Column(String(20), default='admin')
    manager_user_id = Column(Integer, default=0)

    def to_dict(self):
        import json as _j
        try:
            items = _j.loads(self.items_json or '[]')
        except Exception:
            items = []
        return {
            'id':             self.id,
            'return_number':  self.return_number,
            'so_number':      self.so_number,
            'customer':       self.customer,
            'site':           self.site,
            'return_reason':  self.return_reason,
            'items':          items,
            'total_refund':   self.total_refund,
            'status':         self.status,
            'notes':          self.notes,
            'created_at':     self.created_at,
            'created_by':     self.created_by,
            'approved_at':    self.approved_at,
            'approved_by':    self.approved_by,
        }


# ── PurchaseReturn ─────────────────────────────────────────
class PurchaseReturn(db.Model):
    """Return of goods back to a supplier from a received Purchase Order."""
    __tablename__ = "purchase_returns"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    return_number   = Column(String(50), unique=True, nullable=False)
    po_number       = Column(String(50), nullable=False)          # reference to original PO
    supplier        = Column(String(150), default='')
    site            = Column(String(50), default='')
    return_reason   = Column(Text, default='')
    product_name    = Column(String(200), default='')
    product_id      = Column(String(50), default='')
    quantity        = Column(Integer, default=0)
    unit_cost       = Column(Float, default=0)
    total_credit    = Column(Float, default=0)
    status          = Column(String(30), default='Pending')       # Pending | Approved | Rejected | Sent
    notes           = Column(Text, default='')
    created_at      = Column(String(20), default='')
    created_by      = Column(String(80), default='')
    approved_at     = Column(String(20), default='')
    approved_by     = Column(String(80), default='')
    role            = Column(String(20), default='admin')
    manager_user_id = Column(Integer, default=0)

    def to_dict(self):
        return {
            'id':             self.id,
            'return_number':  self.return_number,
            'po_number':      self.po_number,
            'supplier':       self.supplier,
            'site':           self.site,
            'return_reason':  self.return_reason,
            'product_name':   self.product_name,
            'product_id':     self.product_id,
            'quantity':       self.quantity,
            'unit_cost':      self.unit_cost,
            'total_credit':   self.total_credit,
            'status':         self.status,
            'notes':          self.notes,
            'created_at':     self.created_at,
            'created_by':     self.created_by,
            'approved_at':    self.approved_at,
            'approved_by':    self.approved_by,
        }
