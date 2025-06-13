from flask import Blueprint
from controllers.sales_records_controller import SalesRecordsController

# Create blueprint for users routes
sales_records_bp = Blueprint('company-salesrecords', __name__, url_prefix='/company-salesrecords')

# Define routes
sales_records_bp.route('/<string:company_id>', methods=['GET'])(SalesRecordsController.get_sales_records)
sales_records_bp.route('/', methods=['POST'])(SalesRecordsController.create_sales_records)
sales_records_bp.route('/<string:company_id>/<string:sales_id>', methods=['DELETE'])(SalesRecordsController.delete_sales_record)
