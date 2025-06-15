from marshmallow import Schema, fields, validate, ValidationError

class CompanySalesItensRecordsSchema(Schema):
    """Schema for Product data validation and serialization."""
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    sales_record_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255)) 
    table_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    product_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    product_description = fields.Str(validate=validate.Length(min=1, max=255))
    unit_price = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Float(required=True, validate=validate.Range(min=0))
    total_price = fields.Float(required=True, validate=validate.Range(min=0))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
   
# Initialize schema instances
company_sales_record_schema_itens = CompanySalesItensRecordsSchema()
company_sales_records_schema_itens = CompanySalesItensRecordsSchema(many=True)