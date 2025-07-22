from marshmallow import Schema, fields, validate, ValidationError

class CompanyProductsSchema(Schema):
    """Schema for Product data validation and serialization."""
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    company_id = fields.Str(required=True, validate=validate.Length(min=1, max=255)) 
    category_id = fields.Str(required=True, validate=validate.Length(min=1, max=255))  # Category ID
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    price = fields.Float(required=True, validate=validate.Range(min=0))  # Price must be non-negative
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    subcategory_id = fields.Str(allow_none=True, validate=validate.Length(max=255))  # Subcategory ID
    unit = fields.Str(missing="UN")
    ncm = fields.Str()
    cest = fields.Str()
    cfop = fields.Str()
    csosn = fields.Str()
    origin = fields.Str()
    cst_pis = fields.Str()
    cst_cofins = fields.Str()

   

class CompanyProductsUpdateSchema(Schema):
    """Schema for Product update operations (id not required)."""
  
    category_id = fields.Str(allow_none=True, validate=validate.Length(max=255))  # Category ID
    description = fields.Str(allow_none=True, validate=validate.Length(max=255))
    price = fields.Float(allow_none=True, validate=validate.Range(min=0))  # Price must be non-negative
    subcategory_id = fields.Str(allow_none=True, validate=validate.Length(max=255))  # Subcategory ID
    unit = fields.Str()
    ncm = fields.Str()
    cest = fields.Str()
    cfop = fields.Str()
    csosn = fields.Str()
    origin = fields.Str()
    cst_pis = fields.Str()
    cst_cofins = fields.Str()

# Initialize schema instances
company_product_schema = CompanyProductsSchema()
company_products_schema = CompanyProductsSchema(many=True)
company_product_update_schema = CompanyProductsUpdateSchema()