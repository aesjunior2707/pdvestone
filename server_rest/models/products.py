from datetime import datetime
from sqlalchemy import func
from config.database import db

class Products(db.Model):
    """Products model representing the companies table."""
    
    __tablename__ = 'company_products'
    
    # Primary key and unique constraint

    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    category_id = db.Column(db.String(255), db.ForeignKey('categories.id'), nullable=False) 
    
    # Products information
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    subcategory_id = db.Column(db.String(255), nullable=True)  # Subcategory ID
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='company_products_pkey'),
    )
    
    def __init__(self, id, company_id,category_id, description,price=0.0, subcategory_id=None):
        """Initialize a new Company instance."""
        self.id = id
        self.company_id = company_id
        self.category_id = category_id
        self.description = description
        self.price = price
        self.subcategory_id = subcategory_id
  
    def to_dict(self):
        """Convert Products instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'category_id': self.category_id,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'subcategory_id': self.subcategory_id
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the Products instance."""
        return f'<Product {self.id}: {self.description}>'