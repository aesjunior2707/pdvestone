from datetime import datetime
from sqlalchemy import func
from config.database import db

class Company(db.Model):
    """Company model representing the companies table."""
    
    __tablename__ = 'companies'
    
    # Primary key and unique constraint
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    
    # Company information
    legal_name = db.Column(db.String(255), nullable=False)
    trade_name = db.Column(db.String(255), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    responsible_person = db.Column(db.String(255), nullable=True)
    tax_id = db.Column(db.String(20), nullable=True, unique=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='unique_company_id'),
    )
    
    def __init__(self, id, legal_name,tax_id,trade_name=None, contact_phone=None, 
                 contact_email=None, responsible_person=None):
        """Initialize a new Company instance."""
        self.id = id
        self.legal_name = legal_name
        self.trade_name = trade_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.responsible_person = responsible_person
        self.tax_id = tax_id

    
    def to_dict(self):
        """Convert company instance to dictionary."""
        return {
            'id': self.id,
            'legal_name': self.legal_name,
            'trade_name': self.trade_name,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'responsible_person': self.responsible_person,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tax_id': self.tax_id
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the Company instance."""
        return f'<Company {self.id}: {self.legal_name}>'