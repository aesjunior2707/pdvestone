from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.printers import Printers
from schemas.printers_schema import printer_schema,printers_schema, printer_update_schema
from config.database import db

class PrintersController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_printers_company(company_id):
        """
        GET /company-printers/<company_id> - Retrieve a specific user by Company Id.
       
        """
        try:
            printers = Printers.query.filter_by(company_id=company_id).all()
            
            
            if not printers:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
            result = printers_schema.dump(printers)
            
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
    def create_printers():
        """
        POST /company-printers - Create a new Printer for a specific company.
        
        Returns:
            JSON response with created Printer data and HTTP status code.
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
            data = printer_schema.load(json_data)

            # Create new Printer instance
            new_printer = Printers(**data)
            
            # Add to session and commit
            db.session.add(new_printer)
            db.session.commit()
            
            result = printer_schema.dump(new_printer)
            
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
    def update_printer(company_id, printer_id):
        """
        PUT /company-printers/<company_id>/<printer_id> - Update a specific Printer for a company.
        
        Returns:
            JSON response with updated Printer data and HTTP status code.
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
            data = printer_update_schema.load(json_data)
            
            # Query the table to update
            printer = Printers.query.filter_by(company_id=company_id, id=printer_id).first()
            
            if not printer:
                return jsonify({
                    'success': False,
                    'error': 'Printer not found',
                    'message': f'Printer with ID {printer_id} for company {printer_id} does not exist'
                }), 404
            
            # Update fields
            for key, value in data.items():
                setattr(printer, key, value)
            
            db.session.commit()
            
            result = printer_schema.dump(printer)
            
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
    def delete_printer(company_id, printer_id):
        """
        DELETE /company-printers/<company_id>/<printer_id> - Delete a specific Printer for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            printer = Printers.query.filter_by(company_id=company_id, id=printer_id).first()
            
            if not printer:
                return jsonify({
                    'success': False,
                    'error': 'Printer not found',
                    'message': f'Printer with ID {printer_id} for company {printer_id} does not exist'
                }), 404
            
            db.session.delete(printer)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': ' deleted successfully'
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