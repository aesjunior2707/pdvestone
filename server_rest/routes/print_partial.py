from flask import Blueprint
from controllers.print_partial_controller import PrintPartialController

# Create blueprint for users routes
print_bp = Blueprint('print-partial', __name__, url_prefix='/print-partial')


print_bp.route('/', methods=['POST'])(PrintPartialController.print_partial)
