from flask import Blueprint
from controllers.company_tables_controller import CompanyTablesController

# Create blueprint for users routes
company_tables_bp = Blueprint('company-tables', __name__, url_prefix='/company-tables')

# Define routes
company_tables_bp.route('/<string:company_id>', methods=['GET'])(CompanyTablesController.get_tables_company)
company_tables_bp.route('/', methods=['POST'])(CompanyTablesController.create_table)
company_tables_bp.route('/<string:company_id>/<string:table_id>', methods=['PUT'])(CompanyTablesController.update_company_table)
company_tables_bp.route('/<string:company_id>/<string:table_id>', methods=['DELETE'])(CompanyTablesController.delete_table)
