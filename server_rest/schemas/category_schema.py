from marshmallow import Schema, fields, validate, ValidationError

class CategorySchema(Schema):
    """Schema for category data validation and serialization."""
    
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategoryUpdateSchema(Schema):
    """Schema for category update operations (id not required)."""
    
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))

# Initialize schema instances
category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
category_update_schema = CategoryUpdateSchema()