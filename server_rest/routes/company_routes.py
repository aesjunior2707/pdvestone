from flask import Blueprint
from controllers.company_controller import CompanyController

# Create blueprint for company routes
company_bp = Blueprint('companies', __name__, url_prefix='/companies')

# Define routes
company_bp.route('/', methods=['GET'])(CompanyController.get_companies)
company_bp.route('/<string:company_id>', methods=['GET'])(CompanyController.get_company)
company_bp.route('/', methods=['POST'])(CompanyController.create_company)
company_bp.route('/<string:company_id>', methods=['PUT'])(CompanyController.update_company)
company_bp.route('/<string:company_id>', methods=['DELETE'])(CompanyController.delete_company)