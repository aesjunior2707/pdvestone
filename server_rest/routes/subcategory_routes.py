from flask import Blueprint
from controllers.subcategory_controller import SubCategoryController

# Create blueprint for users routes
subcategory_bp = Blueprint('company-subcategory', __name__, url_prefix='/company-subcategory')

# Define routes
subcategory_bp.route('/<string:company_id>/<string:category_id>', methods=['GET'])(SubCategoryController.get_subcategory_company)
subcategory_bp.route('/', methods=['POST'])(SubCategoryController.create_subcategory)
subcategory_bp.route('/<string:company_id>/<string:category_id>/<string:subcategory_id>', methods=['PUT'])(SubCategoryController.update_subcategory)
subcategory_bp.route('/<string:company_id>/<string:category_id>/<string:subcategory_id>', methods=['DELETE'])(SubCategoryController.delete_subcategory)
