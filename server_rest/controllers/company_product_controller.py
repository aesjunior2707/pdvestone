from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.products import Products
from schemas.company_products import company_product_schema,company_products_schema, company_product_update_schema
from controllers.subcategory_controller import SubCategoryController
from config.database import db

class CompanyProductController:
    """Controller class for handling company-related HTTP requests."""
    
    @staticmethod
    def get_all_products_company(company_id):
        try:
            """
            GET /company-products/<company_id> - Retrieve all products by Company Id.
           
            """
            products = Products.query.filter_by(company_id=company_id).order_by(Products.created_at.desc()).all()
            
            if not products:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
            result = company_products_schema.dump(products)
            
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


    def get_products_company(company_id,category_id):
        """
        GET /company-products/<company_id>/<category_id> - Retrieve a specific list products by Company Id.
       
        """
        try:
            _subcategory_id = request.args.get('subcategory_id')
            
            if _subcategory_id:
                products = Products.query.filter_by(company_id=company_id,category_id=category_id,subcategory_id=_subcategory_id).all()
            else:
                products = Products.query.filter_by(company_id=company_id,category_id=category_id).all()
               
            result = company_products_schema.dump(products)

            if not _subcategory_id:
                subcagtegories = SubCategoryController.get_subcategory_company(company_id,category_id,True)
            
                subcategories_json = subcagtegories[0].get_json()

                print('subcategories_json',subcategories_json)
            
                for subcategory in subcategories_json['data']:
                    result.append({
                        'id': subcategory['id'],
                        'company_id': subcategory['company_id'],
                        'category_id': subcategory['category_id'],
                        'subcategory_id_menu': subcategory['id'],
                        'description' : subcategory['description'],
                        'created_at': subcategory['created_at'],
                        'updated_at': subcategory['updated_at'],
                        'price' : 0.0
                    })
    
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
    def create_product():
        """
        POST /company-products - Create a new products for a specific company.
        
        Returns:
            JSON response with created products data and HTTP status code.
        """
        try:
            # Get JSON data from request
            json_data = request.get_json()
            
            if not json_data:
                return jsonify({
                    'success': False,
                    'error': 'No input data provided'
                }), 400
 
            data = company_product_schema.load(json_data)
           
            # Create new table instance
            new_product = Products(**data)
            
            # Add to session and commit
            db.session.add(new_product)
            db.session.commit()
            
            result = company_product_schema.dump(new_product)
            
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
    def update_company_product(company_id,product_id,category_id):
        """
        PUT /company-products/<company_id>/<product_id>/<category_id> - Update a specific product for a company.
        
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
            data = company_product_update_schema.load(json_data)
            
            # Query the table to update
            products = Products.query.filter_by(company_id=company_id, id=product_id,category_id=category_id).first()
            
            if not products:
                return jsonify({
                    'success': False,
                    'error': 'Product not found',
                    'message': f'Product with ID {product_id} for company {company_id} does not exist'
                }), 404
            
            # Update fields
            for key, value in data.items():
                setattr(products, key, value)
            
            db.session.commit()
            
            result = company_product_schema.dump(products)
            
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
    def delete_product(company_id, product_id,category_id):
        """
        DELETE /company-products/<company_id>/<product_id>/<category_id> - Delete a specific table for a company.
        
        Returns:
            JSON response with success status and HTTP status code.
        """
        try:
            # Query the table to delete
            products = Products.query.filter_by(company_id=company_id, id=product_id,category_id=category_id).first()
            
            if not products:
                return jsonify({
                    'success': False,
                    'error': 'Product not found',
                    'message': f'Product with ID {product_id} for company {company_id} does not exist'
                }), 404
            
            db.session.delete(products)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Products deleted successfully'
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