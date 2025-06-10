from flask import Blueprint
from controllers.company_product_controller import CompanyProductController

# Create blueprint for users routes
company_products_bp = Blueprint('company-products', __name__, url_prefix='/company-products')

# Define routes
company_products_bp.route('/<string:company_id>/<string:category_id>', methods=['GET'])(CompanyProductController.get_products_company)
company_products_bp.route('/', methods=['POST'])(CompanyProductController.create_product)
company_products_bp.route('/<string:company_id>/<string:product_id>/<string:category_id>', methods=['PUT'])(CompanyProductController.update_company_product)
company_products_bp.route('/<string:company_id>/<string:product_id>/<string:category_id>', methods=['DELETE'])(CompanyProductController.delete_product)
