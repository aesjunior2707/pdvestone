from marshmallow import Schema, fields, validate, ValidationError

class PrintersSchema(Schema):
    """Schema for Product data validation and serialization."""
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255)) 
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))  # Printer address
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    reference = fields.Str(required=True, validate=validate.Length(min=1, max=255))  # Printer reference
    terminal = fields.Str(required=True, validate=validate.Length(min=1, max=255))  # Terminal ID


class PrintersUpdateSchema(Schema):
    """Schema for Product update operations (id not required)."""
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255)) 
    address = fields.Str(validate=validate.Length(min=1, max=255))  # Printer address
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    reference = fields.Str(validate=validate.Length(min=1, max=255))  # Printer reference
    terminal = fields.Str(validate=validate.Length(min=1, max=255))  # Terminal ID
# Initialize schema instances
printer_schema = PrintersSchema()
printers_schema = PrintersSchema(many=True)
printer_update_schema = PrintersUpdateSchema()