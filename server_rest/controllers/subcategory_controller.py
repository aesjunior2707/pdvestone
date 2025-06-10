from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.subcategory import SubCategory
from schemas.subcategory_schema import subcategory_schema,subcategorys_schema, subcategory_update_schema
from config.database import db

class SubCategoryController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_subcategory_company(company_id,category_id,response=False):
        """
        GET /company-subcategory/<company_id>/category_id - Retrieve a specific user by Company Id.
       
        """
        try:
            subcategory = SubCategory.query.filter_by(company_id=company_id,category_id=category_id).all()
            
            if not subcategory and not response:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
        
            result = subcategorys_schema.dump(subcategory)
            
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
    def create_subcategory():
        """
        POST /company-subcategory - Create a new category for a specific company.
        
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
            data = subcategory_schema.load(json_data)

            # Create new category instance
            new_category = SubCategory(**data)
            
            # Add to session and commit
            db.session.add(new_category)
            db.session.commit()
            
            result = subcategory_schema.dump(new_category)
            
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
    def update_subcategory(company_id, category_id,subcategory_id):
        """
        PUT /company-subcategory/<company_id>/<category_id>/<subcategory_id> - Update a specific category for a company.
        
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
            data = subcategory_update_schema.load(json_data)
            
            # Query the table to update
            subcategory = SubCategory.query.filter_by(company_id=company_id, id=category_id,category_id=subcategory_id).first()
            
            if not subcategory:
                return jsonify({
                    'success': False,
                    'error': 'SubCategory not found',
                    'message': f'SubCategory with ID {category_id} for company {category_id} does not exist'
                }), 404
            
            # Update fields
            for key, value in data.items():
                setattr(subcategory, key, value)
            
            db.session.commit()
            
            result = subcategory_schema.dump(subcategory)
            
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
    def delete_subcategory(company_id, category_id,subcategory_id):
        """
        DELETE /company-subcategory/<company_id>/<category_id>/<subcategory_id> - Delete a specific category for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            subcategory = SubCategory.query.filter_by(company_id=company_id, id=category_id,category_id=subcategory_id).first()
            
            if not subcategory:
                return jsonify({
                    'success': False,
                    'error': 'SubCategory not found',
                    'message': f'Category with ID {category_id} for company {category_id} does not exist'
                }), 404
            
            db.session.delete(subcategory)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'SubCategory deleted successfully'
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