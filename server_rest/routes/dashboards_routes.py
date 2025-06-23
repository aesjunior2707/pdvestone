from flask import Blueprint
from controllers.dashboards_controller import DashboardsController

# Create blueprint for users routes
dash_bp = Blueprint('dashboards', __name__, url_prefix='/dashboards')


dash_bp.route('/home-page', methods=['GET'])(DashboardsController.dash_homepage)
