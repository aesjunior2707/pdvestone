from datetime import datetime
from sqlalchemy import func
from config.database import db

class Tables(db.Model):
    """Tables model representing the companies table."""
    
    __tablename__ = 'company_tables'
    
    # Primary key and unique constraint

    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    
    
    # Tables information
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=True)

    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='company_tables_pkey'),
    )
    
    def __init__(self, id, company_id,description, status):
        """Initialize a new Company instance."""
        self.id = id
        self.company_id = company_id
        self.description = description
        self.status = status
  
    def to_dict(self):
        """Convert Tables instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the Tables instance."""
        return f'<Table {self.id}: {self.description}>'