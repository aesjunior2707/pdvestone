from marshmallow import Schema, fields, validate, ValidationError

class CompanyTablesSchema(Schema):
    """Schema for company data validation and serialization."""
    
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255)) 
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    status = fields.Str(allow_none=True, validate=validate.Length(max=20))  # e.g., 'available', 'ocupped'
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
   

class CompanyTablesUpdateSchema(Schema):
    """Schema for company update operations (id not required)."""
    company_id = fields.Str(allow_none=True, validate=validate.Length(max=255))
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    status = fields.Str(allow_none=True, validate=validate.Length(max=20))  # e.g., 'available', 'ocupped'

# Initialize schema instances
company_table_schema = CompanyTablesSchema()
company_tables_schema = CompanyTablesSchema(many=True)
company_tables_update_schema = CompanyTablesUpdateSchema()