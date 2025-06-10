from datetime import datetime
from sqlalchemy import func
from config.database import db

class Orders(db.Model):
    """Category model representing the companies table."""
    
    __tablename__ = 'orders'
    
    # Primary key and unique constraint
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    table_id = db.Column(db.String(255), db.ForeignKey('company_tables.id'), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(255), db.ForeignKey('company_products.id'), nullable=False)
    product_description = db.Column(db.String(255), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=True, default=0.0)
    note = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='open')
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='orders_pkey'),
    )
    
    def __init__(self, id, company_id, table_id, user_id, product_id, product_description, 
                unit_price, quantity, total_price,note=None, user_name=None, status='open'):
        """Initialize a new Company instance."""
        self.id = id
        self.company_id = company_id
        self.table_id = table_id
        self.user_id = user_id
        self.product_id = product_id
        self.product_description = product_description
        self.unit_price = unit_price
        self.quantity = quantity
        self.total_price = total_price
        self.note = note
        self.user_name = user_name
        self.status = status

  
    def to_dict(self):
        """Convert company instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'table_id': self.table_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_description': self.product_description,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'note': self.note,
            'user_name': self.user_name,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
           
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the User instance."""
        return f'<Order {self.id}: {self.table_id} - {self.product_id}>'