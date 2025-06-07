from marshmallow import Schema, fields, validate, ValidationError

class CompanySchema(Schema):
    """Schema for company data validation and serialization."""
    
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    legal_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    trade_name = fields.Str(allow_none=True, validate=validate.Length(max=255))
    contact_phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    contact_email = fields.Email(allow_none=True, validate=validate.Length(max=255))
    responsible_person = fields.Str(allow_none=True, validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    tax_id = fields.Str(required=True, validate=validate.Length(min=1, max=20))

class CompanyUpdateSchema(Schema):
    """Schema for company update operations (id not required)."""
    
    legal_name = fields.Str(validate=validate.Length(min=1, max=255))
    trade_name = fields.Str(allow_none=True, validate=validate.Length(max=255))
    contact_phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    contact_email = fields.Email(allow_none=True, validate=validate.Length(max=255))
    responsible_person = fields.Str(allow_none=True, validate=validate.Length(max=255))
    tax_id = fields.Str(validate=validate.Length(min=1, max=20))

# Initialize schema instances
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
company_update_schema = CompanyUpdateSchema()