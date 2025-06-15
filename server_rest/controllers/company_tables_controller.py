from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.tables import Tables
from schemas.company_tables import company_table_schema,company_tables_schema, company_tables_update_schema
from config.database import db
from controllers.order_controller import OrderController
class CompanyTablesController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_tables_company(company_id):
        """
        GET /company-tables/<company_id> - Retrieve a specific user by Company Id.
       
        """
        try:
            tables = Tables.query.filter_by(company_id=company_id).all()
            
            if not tables:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
            result = company_tables_schema.dump(tables)

            for table in result:            
                controller_order = OrderController()
                orders_table = controller_order.get_order_company(table['company_id'], table['id'])
                
                status = 'available' if len(orders_table) == 0 else 'occupied'
                table['status'] = status 
                
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
    def create_table():
        """
        POST /company-tables - Create a new table for a specific company.
        
        Returns:
            JSON response with created table data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
            
            print("Received JSON data:", json_data)
            # Validate and deserialize input data
            data = company_table_schema.load(json_data)
            
            if data.get('description') is None:
                print("Description is None, setting it to id")
                data['description'] = data['id']

            if data.get('status') is None:
                print("Status is None, setting it to 'available'")
                data['status'] = 'available'
            
            print("Creating new table with data:", data)


            # Create new table instance
            new_table = Tables(**data)
            
            # Add to session and commit
            db.session.add(new_table)
            db.session.commit()
            
            result = company_table_schema.dump(new_table)
            
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
    def update_company_table(company_id, table_id,data=None):
        """
        PUT /company-tables/<company_id>/<table_id> - Update a specific table for a company.
        
        Returns:
            JSON response with updated table data and HTTP status code.
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
            data = company_tables_update_schema.load(json_data)
            
            # Query the table to update
            table = Tables.query.filter_by(company_id=company_id, id=table_id).first()
            
            if not table:
                return jsonify({
                    'success': False,
                    'error': 'Table not found',
                    'message': f'Table with ID {table_id} for company {company_id} does not exist'
                }), 404
            
            # Update fields
            for key, value in data.items():
                setattr(table, key, value)
            
            db.session.commit()
            
            result = company_table_schema.dump(table)
            
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
    def delete_table(company_id, table_id):
        """
        DELETE /company-tables/<company_id>/<table_id> - Delete a specific table for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            table = Tables.query.filter_by(company_id=company_id, id=table_id).first()
            
            if not table:
                return jsonify({
                    'success': False,
                    'error': 'Table not found',
                    'message': f'Table with ID {table_id} for company {company_id} does not exist'
                }), 404
            
            db.session.delete(table)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Table deleted successfully'
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