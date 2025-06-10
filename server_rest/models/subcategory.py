from datetime import datetime
from sqlalchemy import func
from config.database import db

class SubCategory(db.Model):
    """Category model representing the companies subcategories."""
    
    __tablename__ = 'subcategories'
    
    # Primary key and unique constraint
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    category_id = db.Column(db.String(255), db.ForeignKey('categories.id'), nullable=False)

    # Category information
    description = db.Column(db.String(255), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='subcategories_pkey'),
    )
    
    def __init__(self, id, company_id,category_id,description):
        """Initialize a new Company instance."""
        self.id = id
        self.company_id = company_id
        self.category_id = category_id
        self.description = description

  
    def to_dict(self):
        """Convert company instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'category_id': self.category_id,
            'description': self.description,
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the User instance."""
        return f'<SubCategory {self.id}: {self.description}>'