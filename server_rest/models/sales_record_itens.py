from datetime import datetime
from sqlalchemy import func
from config.database import db

class SalesRecordItens(db.Model): 
    __tablename__ = 'sales_record_items'
    
    # Primary key and unique constraint

    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    table_id = db.Column(db.String(255), db.ForeignKey('company_tables.id'), nullable=False) 
    sales_record_id = db.Column(db.String(255), db.ForeignKey('sales_records.id'), nullable=False)
    product_id = db.Column(db.String(255), db.ForeignKey('company_products.id'), nullable=False)
    product_description = db.Column(db.String(255), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
        
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='sales_record_items_pkey'),
    )
    
    def __init__(self, id, company_id,table_id, sales_record_id, product_id,product_description,unit_price, quantity, total_price=0.0):
        self.id = id
        self.company_id = company_id
        self.table_id = table_id
        self.sales_record_id = sales_record_id
        self.product_id = product_id
        self.product_description = product_description
        self.unit_price = unit_price
        self.quantity = quantity
        self.total_price = total_price

  
    def to_dict(self):
        """Convert Products instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'table_id' : self.table_id,
            'sales_record_id': self.sales_record_id,
            'product_id': self.product_id,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        return f'<SalesRecordItens {self.id}: {self.table_id}>'