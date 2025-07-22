from flask import Blueprint
from controllers.order_controller import OrderController

# Create blueprint for users routes
orders_bp = Blueprint('company-orders', __name__, url_prefix='/company-orders')

# Define routes
orders_bp.route('/<string:company_id>', methods=['GET'])(OrderController.get_order_company)
orders_bp.route('/', methods=['POST'])(OrderController.create_order)
orders_bp.route('/<string:company_id>/<string:order_id>', methods=['PUT'])(OrderController.update_order)
orders_bp.route('/<string:company_id>/<string:order_id>', methods=['DELETE'])(OrderController.delete_order)
orders_bp.route('/<string:company_id>/table/<string:table_id>',methods=['DELETE'])(OrderController.delete_all_orders_table)
