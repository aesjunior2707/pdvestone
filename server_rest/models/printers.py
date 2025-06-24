from datetime import datetime
from sqlalchemy import func
from config.database import db

class Printers(db.Model):
    """Category model representing the companies table."""
    
    __tablename__ = 'printers'
    
    # Primary key and unique constraint
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    
    # Category information
    description = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)  # Printer address
    reference = db.Column(db.String(255), nullable=False)  # Printer reference
    terminal = db.Column(db.String(255), nullable=False)  # Terminal ID
    __table_args__ = (
        db.UniqueConstraint('id', name='printers_pkey'),
    )
    
    def __init__(self, id, company_id,description,andress,reference,terminal):
        """Initialize a new Company instance."""
        self.id = id
        self.company_id = company_id
        self.description = description
        self.address = andress
        self.reference = reference
        self.terminal = terminal
  
    def to_dict(self):
        """Convert company instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'description': self.description,
            'address': self.address,
            'reference': self.reference,
            'terminal': self.terminal
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the User instance."""
        return f'<Printers {self.id}: {self.description}>'