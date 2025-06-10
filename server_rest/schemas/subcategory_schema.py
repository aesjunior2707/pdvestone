from marshmallow import Schema, fields, validate, ValidationError

class SubCategorySchema(Schema):
    """Schema for category data validation and serialization."""
    
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    category_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))  # Category ID
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SubCategoryUpdateSchema(Schema):
    """Schema for category update operations (id not required)."""
    category_id = fields.Str(allow_none=True, validate=validate.Length(max=255))  # Category ID
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))

# Initialize schema instances
subcategory_schema = SubCategorySchema()
subcategorys_schema = SubCategorySchema(many=True)
subcategory_update_schema = SubCategoryUpdateSchema()