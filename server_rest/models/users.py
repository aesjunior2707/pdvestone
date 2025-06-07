from datetime import datetime
from sqlalchemy import func
from config.database import db

class Users(db.Model):
    """Users model representing the companies table."""
    
    __tablename__ = 'users'
    
    # Primary key and unique constraint
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    company_id = db.Column(db.String(255), db.ForeignKey('companies.id'), nullable=False)
    
    # Users information
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.String(20), nullable=True)  # e.g., 'admin', 'user', etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Unique constraint on id (already covered by primary key)
    __table_args__ = (
        db.UniqueConstraint('id', name='unique_company_id'),
    )
    
    def __init__(self, id, company_id,name,username, password,user_type):
        """Initialize a new Company instance."""
        self.id = id
        self.company_id = company_id
        self.name = name
        self.username = username
        self.password = password
        self.user_type = user_type

    
    def to_dict(self):
        """Convert company instance to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_from_dict(self, data):
        """Update company instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the User instance."""
        return f'<User {self.id}: {self.username}>'