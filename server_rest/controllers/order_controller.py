from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.orders import Orders
from schemas.orders_schema import order_schema,orders_schema, order_update_schema
from config.database import db

class OrderController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_order_company(company_id,table_id=None):
        """
        GET /company-orders/<company_id> - Retrieve a specific user by Company Id.
       
        """
        try:
            table_number = table_id
            _request_parameter = False   
            
            if not table_id:
                _request_parameter = True
                table_number = request.args.get('table')

            order = Orders.query.filter_by(company_id=company_id, table_id=table_number).order_by(Orders.created_at.desc()).all()
            
            if _request_parameter:
                if not order:
                    return jsonify({
                        'success': True,
                        'data': []
                    }), 200
                
            result = orders_schema.dump(order)

            if _request_parameter:
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
    def create_order():
        """
        POST /company-orders - Create a new order for a specific company.
        
        Returns:
            JSON response with created order data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            # Get query parameter 'table' from the request
          
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            # Validate and deserialize input data
            data = orders_schema.load(json_data, many=True)

            # Create new order instances
            new_orders = [Orders(**order_data) for order_data in data]
            
            # Add to session and commit
            db.session.bulk_save_objects(new_orders)
            db.session.commit()
            
            result = orders_schema.dump(new_orders, many=True)
            
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
    def update_order(company_id, order_id):
        """
        PUT /company-orders/<company_id>/<order_id> - Update a specific order for a company.
        
        Returns:
            JSON response with updated order data and HTTP status code.
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
            data = order_update_schema.load(json_data)
        
            order = Orders.query.filter_by(company_id=company_id, id=order_id).first()
            
            if not order:
                return jsonify({
                    'success': False,
                    'error': 'Order not found',
                    'message': f'Order with ID {order_id} for company {company_id} does not exist'
                }), 404
            
            # Update fields
            for key, value in data.items():
                setattr(order, key, value)
            
            db.session.commit()
            
            result = order_schema.dump(order)
            
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
    def delete_order(company_id, order_id=None, table_id=None):
        """
        DELETE /company-orders/<company_id>/<order_id> - Delete a specific order for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            if order_id:
                order = Orders.query.filter_by(company_id=company_id, id=order_id).all()
            
            if table_id:
                order = Orders.query.filter_by(company_id=company_id, table_id=table_id).all()
            
            if not order:
                return jsonify({
                    'success': False,
                    'error': 'Order not found',
                    'message': f'Order with ID {order_id} for company {company_id} does not exist'
                }), 404
            
            if len(order) == 1: 
                db.session.delete(order[0])
                db.session.commit()
            
            else:
                for ord in order:
                    db.session.delete(ord)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Order deleted successfully'
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