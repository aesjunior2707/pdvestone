from flask import Blueprint
from controllers.auth_login_controller import AuthController

# Create blueprint for users routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp.route('/login', methods=['POST'])(AuthController.login)
