from marshmallow import Schema, fields, validate, ValidationError

class OrdersSchema(Schema):
    """Schema for category data validation and serialization."""
    
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    table_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    user_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    product_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    product_description = fields.Str(validate=validate.Length(min=1, max=255))
    unit_price = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    total_price = fields.Float()  # Excluded from input validation
    note = fields.Str(allow_none=True, validate=validate.Length(max=255))
    user_name = fields.Str(validate=validate.Length(min=1, max=255))
    status = fields.Str(required=True, validate=validate.OneOf(['open', 'peding', 'closed']))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OrdersUpdateSchema(Schema):
    """Schema for category update operations (id not required)."""
    table_id = fields.Str(allow_none=True, validate=validate.Length(max=255))
    product_id = fields.Str(allow_none=True, validate=validate.Length(max=255))
    product_description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    unit_price = fields.Float(allow_none=True, validate=validate.Range(min=0))
    quantity = fields.Int(allow_none=True, validate=validate.Range(min=1))
    note = fields.Str(allow_none=True, validate=validate.Length(max=255))
    status = fields.Str(allow_none=True, validate=validate.OneOf(['open', 'peding', 'closed']))

# Initialize schema instances
order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)
order_update_schema = OrdersUpdateSchema()