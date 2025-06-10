from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.company import Company
from schemas.company_schema import companies_schema,company_schema,company_update_schema
from config.database import db

class CompanyController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_companies():
        """
        GET /companies - Retrieve all companies or filter by query parameters.
        
        Returns:
            JSON response with list of companies and HTTP status code.
        """
        try:
            # Get query parameters for filtering
            legal_name = request.args.get('legal_name')
            trade_name = request.args.get('trade_name')
            contact_email = request.args.get('contact_email')
            
            # Build query
            query = Company.query
            
            if legal_name:
                query = query.filter(Company.legal_name.ilike(f'%{legal_name}%'))
            if trade_name:
                query = query.filter(Company.trade_name.ilike(f'%{trade_name}%'))
            if contact_email:
                query = query.filter(Company.contact_email.ilike(f'%{contact_email}%'))
            
            # Execute query
            companies = query.all()
            
            # Serialize and return
            result = companies_schema.dump(companies)
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
    def get_company(company_id):
        """
        GET /companies/<id> - Retrieve a specific company by ID.
        
        Args:
            company_id (str): The unique identifier of the company.
            
        Returns:
            JSON response with company data and HTTP status code.
        """
        try:
            company = Company.query.get(company_id)
            
            if not company:
                return jsonify({
                    'success': False,
                    'error': 'Company not found',
                    'message': f'Company with ID {company_id} does not exist'
                }), 404
            
            result = company_schema.dump(company)
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
    def create_company():
        """
        POST /companies - Create a new company.
        
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
                data = company_schema.load(json_data)
            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'error': 'Validation error',
                    'messages': err.messages
                }), 400
            
            # Check if company with same ID already exists
            existing_company = Company.query.get(data['id'])
            if existing_company:
                return jsonify({
                    'success': False,
                    'error': 'Company already exists',
                    'message': f'Company with ID {data["id"]} already exists'
                }), 409
            
            # Create new company
            new_company = Company(**data)
            db.session.add(new_company)
            db.session.commit()
            
            # Return created company
            result = company_schema.dump(new_company)
            return jsonify({
                'success': True,
                'data': result,
                'message': 'Company created successfully'
            }), 201
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': 'Integrity constraint violation',
                'message': 'Company with this ID already exists'
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
    def update_company(company_id):
        """
        PUT /companies/<id> - Update an existing company.
        
        Args:
            company_id (str): The unique identifier of the company.
            
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
            
            # Find existing company
            company = Company.query.get(company_id)
            if not company:
                return jsonify({
                    'success': False,
                    'error': 'Company not found',
                    'message': f'Company with ID {company_id} does not exist'
                }), 404
            
            # Validate input data
            try:
                data = company_update_schema.load(json_data)
            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'error': 'Validation error',
                    'messages': err.messages
                }), 400
            
            # Update company
            company.update_from_dict(data)
            db.session.commit()
            
            # Return updated company
            result = company_schema.dump(company)
            return jsonify({
                'success': True,
                'data': result,
                'message': 'Company updated successfully'
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
    def delete_company(company_id):
        """
        DELETE /companies/<id> - Delete a company.
        
        Args:
            company_id (str): The unique identifier of the company.
            
        Returns:
            JSON response with deletion confirmation and HTTP status code.
        """
        try:
            # Find existing company
            company = Company.query.get(company_id)
            if not company:
                return jsonify({
                    'success': False,
                    'error': 'Company not found',
                    'message': f'Company with ID {company_id} does not exist'
                }), 404
            
            # Delete company
            db.session.delete(company)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Company with ID {company_id} deleted successfully'
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