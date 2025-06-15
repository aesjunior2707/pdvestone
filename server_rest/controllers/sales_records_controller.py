from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.sales_record import SalesRecord
from schemas.company_sales_records import company_sales_record_schema,company_sales_records_schema
from config.database import db
from controllers.order_controller import OrderController
from controllers.sales_records_itens_controller import SalesRecordsItensController
from datetime import datetime, timedelta

class SalesRecordsController:
    """Controller class for handling company-orders related HTTP requests."""
    
    @staticmethod
    def get_sales_records(company_id):
        """
        GET /company-salesrecords/<company_id> - Retrieve a specific user by Company Id.
       
        """
        try:
            _created_at = request.args.get('created_at')
            
            if _created_at:
                start_date = datetime.strptime(_created_at, '%Y-%m-%d')
                end_date = start_date + timedelta(days=1)
                
                sales_records = SalesRecord.query.filter_by(company_id=company_id).filter(
                    SalesRecord.created_at >= start_date,
                    SalesRecord.created_at < end_date
                ).order_by(SalesRecord.created_at.desc()).all()
            else:
                seven_days_ago = datetime.now() - timedelta(days=7)
                sales_records = SalesRecord.query.filter_by(company_id=company_id).filter(
                    SalesRecord.created_at >= seven_days_ago
                ).order_by(SalesRecord.created_at.desc()).all()
            
            if not sales_records:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
                
            result = company_sales_records_schema.dump(sales_records)
            
            for record in result:
                itens = SalesRecordsItensController.get_sales_records_itens(company_id, record['id'],False)
                record['itens'] = itens
                
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
    def create_sales_records():
        """
        POST /company-salesrecords - Create a new order for a specific company.
        
        Returns:
            JSON response with created order data and HTTP status code.
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
            data = company_sales_record_schema.load(json_data)

            # Create new order instances
            new_sale_records = SalesRecord(**data)
            
            # Add to session and commit
            db.session.add(new_sale_records)
            db.session.commit()

            orders = OrderController.get_order_company(data['company_id'], data['table_id'])
            
            if orders:    
                for order in orders:
                    _order_content = {
                        'id' : order['id'],
                        'sales_record_id' : new_sale_records.id,
                        'company_id' : order['company_id'],
                        'table_id' : order['table_id'],
                        'product_id' : order['product_id'],
                        'product_description' : order['product_description'],
                        'unit_price' : order['unit_price'],
                        'quantity' : order['quantity'],
                        'total_price' : round(order['unit_price'] * order['quantity'], 2)
                    }

                  
                    _sales_record_itens = SalesRecordsItensController()
                    _sales_record_itens.create_sales_records_itens(_order_content)
            
            OrderController.delete_order(company_id=data['company_id'],table_id=data['table_id'])
            
            result = company_sales_record_schema.dump(new_sale_records)
            
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
    def delete_sales_record(company_id, sales_id):
        """
        DELETE /company-salesrecords/<company_id>/<sales_id> - Delete a specific order for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            sales_record = SalesRecord.query.filter_by(company_id=company_id, id=sales_id).first()
            
            if not sales_record:
                return jsonify({
                    'success': False,
                    'error': 'Sales Records not found',
                    'message': f'Sales Records with ID {sales_id} for company {company_id} does not exist'
                }), 404
            
            db.session.delete(sales_record)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Sales Records deleted successfully'
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