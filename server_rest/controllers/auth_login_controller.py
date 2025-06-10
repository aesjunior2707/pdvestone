from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from config.database import db
from models.users import Users


class AuthController:
    """Controller class for handling auth-related HTTP requests."""
    
    @staticmethod
    def login():
        """
        POST /auth/login - Authenticate a user.
        
        Returns:
            JSON response with authentication status and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Extract username and password from input data
            username = json_data.get('username')
            password = json_data.get('password')
            
            if not username or not password:
                return jsonify({
                    'success': False,
                    'error': 'Username and password are required'
                }), 400
            
            # Query the database for the user
            user = Users.query.filter_by(username=username).first()
            
            if not user or not user.check_password(password):  # Assuming `check_password` is a method in the Users model
                return jsonify({
                    'success': False,
                    'error': 'Invalid username or password'
                }), 401
            
            # Generate authentication token (if applicable)
            # token = generate_auth_token(user)  # Replace with your token generation logic
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'name_user' : user.name,
                'company_id': user.company_id,
                'id': user.id,
                # 'token': token  # Include token if applicable
            }), 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Database error occurred',
                'message': str(e)
            }), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
