from marshmallow import Schema, fields, validate, ValidationError

class UsersSchema(Schema):
    """Schema for user data validation and serialization."""
    
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    username = fields.Str(allow_none=True, validate=validate.Length(max=255))
    password = fields.Str(allow_none=True, validate=validate.Length(max=20))
    user_type = fields.Str(allow_none=True, validate=validate.Length(max=20))  # e.g., 'admin', 'user', etc.
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UsersUpdateSchema(Schema):
    """Schema for user update operations (id not required)."""
    
    company_id = fields.Str(validate=validate.Length(min=1, max=255))
    name = fields.Str(validate=validate.Length(min=1, max=255))
    username = fields.Str(allow_none=True, validate=validate.Length(max=255))
    password = fields.Str(allow_none=True, validate=validate.Length(max=20))
    user_type = fields.Str(allow_none=True, validate=validate.Length(max=20))  # e.g., 'admin', 'user', etc.

# Initialize schema instances
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
users_update_schema = UsersUpdateSchema()