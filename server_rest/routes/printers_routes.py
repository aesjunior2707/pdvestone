from flask import Blueprint
from controllers.printers_controller import PrintersController

# Create blueprint for users routes
printers_bp = Blueprint('company-printers', __name__, url_prefix='/company-printers')

# Define routes
printers_bp.route('/<string:company_id>', methods=['GET'])(PrintersController.get_printers_company)
printers_bp.route('/', methods=['POST'])(PrintersController.create_printers)
printers_bp.route('/<string:company_id>/<string:printer_id>', methods=['PUT'])(PrintersController.update_printer)
printers_bp.route('/<string:company_id>/<string:printer_id>', methods=['DELETE'])(PrintersController.delete_printer)
