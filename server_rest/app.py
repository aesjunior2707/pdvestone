from flask import Flask, jsonify
from config.database import create_app, init_database, db
from routes.company_routes import company_bp
from routes.users_routes import users_bp
from routes.auth_routes import auth_bp
from routes.company_tables_routes import company_tables_bp
from routes.category_routes import category_bp
from routes.company_products_routes import company_products_bp
from routes.subcategory_routes import subcategory_bp
from routes.orders_routes import orders_bp
from routes.sales_records_routes import sales_records_bp
from routes.print_partial import print_bp
from routes.dashboards_routes import dash_bp
from routes.printers_routes import printers_bp

def create_application():
    """Create and configure the main Flask application."""
    app = create_app()
    
    # Register blueprints
    app.register_blueprint(company_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(company_tables_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(company_products_bp)
    app.register_blueprint(subcategory_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(sales_records_bp)   
    app.register_blueprint(print_bp) 
    app.register_blueprint(dash_bp)
    app.register_blueprint(printers_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'message': 'Flask REST API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information."""
        return jsonify({
            'message': 'Company Management REST API',
            'version': '1.0.0',
            'endpoints': {
                'companies': {
                    'GET /companies': 'Retrieve all companies',
                    'GET /companies/<id>': 'Retrieve a specific company',
                    'POST /companies': 'Create a new company',
                    'PUT /companies/<id>': 'Update a company',
                    'DELETE /companies/<id>': 'Delete a company'
                },
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'success': False,
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An internal server error occurred'
        }), 500
    
    # Initialize database
    init_database(app)
    
    return app

# Create application instance
app = create_application()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)