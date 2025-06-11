from datetime import datetime
from sqlalchemy import func
from config.database import db

class SalesRecord(db.Model): 
    __tablename__ = 'sales_records'
    
    # Primary key and unique constraint

    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    table_id = db.Column(db.String(255), db.ForeignKey('company_tables.id'), nullable=False) 
    
    # sales record information
    payment_type = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='sales_records_pkey'),
    )
    
    def __init__(self, id, company_id,table_id, payment_type,total_amount=0.0):

        self.id = id
        self.company_id = company_id
        self.table_id = table_id
        self.payment_type = payment_type
        self.total_amount = total_amount
  
    def to_dict(self):
        """Convert Products instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'table_id' : self.table_id,
            'payment_type' : self.payment_type,
            'total_amount' : self.total_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        return f'<SalesRecord {self.id}: {self.table_id}>'