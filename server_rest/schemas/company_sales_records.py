from marshmallow import Schema, fields, validate, ValidationError

class CompanySalesRecordsSchema(Schema):
    """Schema for Product data validation and serialization."""
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255)) 
    table_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    payment_type = fields.Str(allow_none=True, validate=validate.Length(max=255))
    total_amount = fields.Float(required=True, validate=validate.Range(min=0))  # Price must be non-negative
    user_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    user_name = fields.Str(validate=validate.Length(min=1, max=255))
    identification_nfce = fields.Str(allow_none=True, validate=validate.Length(max=255))
    type_customer = fields.Str(allow_none=True, validate=validate.Length(max=255))
    issues_invoice = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
   

# Initialize schema instances
company_sales_record_schema = CompanySalesRecordsSchema()
company_sales_records_schema = CompanySalesRecordsSchema(many=True)