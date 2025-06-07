from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.users import Users
from schemas.users_schema import user_schema, users_schema, users_update_schema
from config.database import db

class UsersController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_users():
        """
        GET /users - Retrieve all users or filter by query parameters.
        
        Returns:
            JSON response with list of companies and HTTP status code.
        """
        try:
            # Get query parameters for filtering
            name_filter = request.args.get('name')
            user_type_filter = request.args.get('user_type')
            
            # Build query
            query = Users.query
            
            if name_filter:
                query = query.filter(Users.name.ilike(f'%{name_filter}%'))
            if user_type_filter:
                query = query.filter(Users.user_type.ilike(f'%{user_type_filter}%'))
            
            # Execute query
            users = query.all()
            
            # Serialize and return
            result = users_schema.dump(users)
            return jsonify({
                'success': True,
                'data': result,
                'count': len(result)
            }), 200
            
        except SQLAlchemyError as e:
            return jsonify({
                'success': False,
                'error': 'Database error occurred',
                'message': str(e)
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    
    @staticmethod
    def get_user(user_id):
        """
        GET /users/<id> - Retrieve a specific user by ID.
        
        Args:
            user_id (str): The unique identifier of the user.
            
        Returns:
            JSON response with company data and HTTP status code.
        """
        try:
            user = Users.query.get(user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found',
                    'message': f'User with ID {user} does not exist'
                }), 404
            
            result = user_schema.dump(user)
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
            
        except SQLAlchemyError as e:
            return jsonify({
                'success': False,
                'error': 'Database error occurred',
                'message': str(e)
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def create_user():
        """
        POST /users - Create a new user.
        
        Returns:
            JSON response with created company data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Validate input data
            try:
                data = user_schema.load(json_data)

            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'error': 'Validation error',
                    'messages': err.messages
                }), 400
            
            # Check if users with same ID already exists
            existing_user = Users.query.get(data['id'])
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'User already exists',
                    'message': f'User with ID {data["id"]} already exists'
                }), 409
            
            # Create new company
            new_company = Users(**data)
            db.session.add(new_company)
            db.session.commit()
            
            # Return created company
            result = user_schema.dump(new_company)
            return jsonify({
                'success': True,
                'data': result,
                'message': 'User created successfully'
            }), 201
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Integrity constraint violation',
                'message': 'User with this ID already exists'
            }), 409
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
    
    @staticmethod
    def update_user(user_id):
        """
        PUT /users/<id> - Update an existing company.
        
        Args:
            user_id (str): The unique identifier of the company.
            
        Returns:
            JSON response with updated company data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Find existing User

            user = Users.query.get(user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found',
                    'message': f'User with ID {user_id} does not exist'
                }), 404
            
            # Validate input data
            try:
                data = users_update_schema.load(json_data)

            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'error': 'Validation error',
                    'messages': err.messages
                }), 400
            
            # Update user
            user.update_from_dict(data)
            db.session.commit()
            
            # Return updated User
            result = users_update_schema.dump(user)
            return jsonify({
                'success': True,
                'data': result,
                'message': 'User updated successfully'
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
    
    @staticmethod
    def delete_user(user_id):
        """
        DELETE /users/<id> - Delete a user.
        
        Args:
            user_id (str): The unique identifier of the user.
            
        Returns:
            JSON response with deletion confirmation and HTTP status code.
        """
        try:
            # Find existing user
            user = Users.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found',
                    'message': f'User with ID {user_id} does not exist'
                }), 404
            
            # Delete user
            db.session.delete(user)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'User with ID {user_id} deleted successfully'
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