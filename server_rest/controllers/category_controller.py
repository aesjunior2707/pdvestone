from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.category import Category
from schemas.category_schema import category_schema,categorys_schema, category_update_schema
from config.database import db

class CategoryController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_category_company(company_id):
        """
        GET /company-category/<company_id> - Retrieve a specific user by Company Id.
       
        """
        try:
            category = Category.query.filter_by(company_id=company_id).all()
            
            if not category:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
            result = categorys_schema.dump(category)
            
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
    def create_category():
        """
        POST /company-category - Create a new category for a specific company.
        
        Returns:
            JSON response with created category data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Validate and deserialize input data
            data = category_schema.load(json_data)

            # Create new category instance
            new_category = Category(**data)
            
            # Add to session and commit
            db.session.add(new_category)
            db.session.commit()
            
            result = category_schema.dump(new_category)
            
            return jsonify({
                'success': True,
                'data': result
            }), 201
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Integrity error occurred',
                'message': str(e.orig)
            }), 400
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error occurred',
                'message': str(e.messages)
            }), 422
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
    def update_category(company_id, category_id):
        """
        PUT /company-category/<company_id>/<category_id> - Update a specific category for a company.
        
        Returns:
            JSON response with updated category data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Validate and deserialize input data
            data = category_update_schema.load(json_data)
            
            # Query the table to update
            category = Category.query.filter_by(company_id=company_id, id=category_id).first()
            
            if not category:
                return jsonify({
                    'success': False,
                    'error': 'Category not found',
                    'message': f'Category with ID {category_id} for company {category_id} does not exist'
                }), 404
            
            # Update fields
            for key, value in data.items():
                setattr(category, key, value)
            
            db.session.commit()
            
            result = category_schema.dump(category)
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Integrity error occurred',
                'message': str(e.orig)
            }), 400
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error occurred',
                'message': str(e.messages)
            }), 422
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
    def delete_category(company_id, category_id):
        """
        DELETE /company-category/<company_id>/<category_id> - Delete a specific category for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            category = Category.query.filter_by(company_id=company_id, id=category_id).first()
            
            if not category:
                return jsonify({
                    'success': False,
                    'error': 'Category not found',
                    'message': f'Category with ID {category_id} for company {category_id} does not exist'
                }), 404
            
            db.session.delete(category)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Category deleted successfully'
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