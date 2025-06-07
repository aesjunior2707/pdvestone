from flask import Blueprint
from controllers.user_controller import UsersController

# Create blueprint for users routes
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Define routes
users_bp.route('/', methods=['GET'])(UsersController.get_users)
users_bp.route('/<string:user_id>', methods=['GET'])(UsersController.get_user)
users_bp.route('/', methods=['POST'])(UsersController.create_user)
users_bp.route('/<string:user_id>', methods=['PUT'])(UsersController.update_user)
users_bp.route('/<string:user_id>', methods=['DELETE'])(UsersController.delete_user)