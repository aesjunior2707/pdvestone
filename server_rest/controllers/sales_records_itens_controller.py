from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.sales_record_itens import SalesRecordItens
from schemas.company_sales_records_itens import company_sales_record_schema_itens,company_sales_records_schema_itens
from config.database import db


class SalesRecordsItensController:
    """Controller class for handling company-orders related HTTP requests."""
    
    @staticmethod
    def get_sales_records_itens(company_id,sales_record_id, request_api=True):
        """
        GET /company-salesrecords/<company_id>/<sales_record_id> - Retrieve a specific user by Company Id.
       
        """
        try:
            sales_records_itens = SalesRecordItens.query.filter_by(company_id=company_id,sales_record_id=sales_record_id).all()
            
            if request_api:
                if not sales_records_itens:
                    return jsonify({
                        'success': True,
                        'data': []
                    }), 200
                    
            result = company_sales_records_schema_itens.dump(sales_records_itens)

           
            if request_api:
                return jsonify({
                    'success': True,
                    'data': result
                }), 200

            return result
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
    def create_sales_records_itens(content=None):
        """
        POST /company-salesrecordsitens - Create a new order for a specific company.
        
        Returns:
            JSON response with created order data and HTTP status code.
        """
        try:
            if not content:
                json_data = request.get_json()
            else:
                json_data = content
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Validate and deserialize input data
            data = company_sales_record_schema_itens.load(json_data)

            # Create new order instances
            new_sale_records_itens = SalesRecordItens(**data)
            
            # Add to session and commit
            db.session.add(new_sale_records_itens)
            db.session.commit()
            
                        
            result = company_sales_record_schema_itens.dump(new_sale_records_itens)
            
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
    def delete_sales_record_itens(company_id, sales_id,sales_record_id_itens):
        """
        DELETE /company-salesrecords/<company_id>/<sales_id>/<sales_record_id_itens> - Delete a specific order for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            sales_record_itens = SalesRecordItens.query.filter_by(company_id=company_id, sales_record_id=sales_id,id=sales_record_id_itens).first()
            
            if not sales_record_itens:
                return jsonify({
                    'success': False,
                    'error': 'Sales Records Itens not found',
                    'message': f'Sales Records with ID {sales_id} for company {company_id} does not exist'
                }), 404
            
            db.session.delete(sales_record_itens)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Sales Records Itens deleted successfully'
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