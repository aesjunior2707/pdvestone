from flask import Blueprint
from controllers.category_controller import CategoryController

# Create blueprint for users routes
category_bp = Blueprint('company-category', __name__, url_prefix='/company-category')

# Define routes
category_bp.route('/<string:company_id>', methods=['GET'])(CategoryController.get_category_company)
category_bp.route('/', methods=['POST'])(CategoryController.create_category)
category_bp.route('/<string:company_id>/<string:category_id>', methods=['PUT'])(CategoryController.update_category)
category_bp.route('/<string:company_id>/<string:category_id>', methods=['DELETE'])(CategoryController.delete_category)
