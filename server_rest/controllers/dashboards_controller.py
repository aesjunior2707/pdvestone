from flask import request, jsonify
from controllers.mqtt_controller import MQTTController
import json
from config.database import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from models.sales_record_itens import SalesRecordItens
from models.orders import Orders
from models.sales_record import SalesRecord
from sqlalchemy import func, and_
from datetime import datetime, timedelta

class DashboardsController:
    @staticmethod
    def dash_homepage():
        _company_id = request.args.get('company_id', None)

        try:
            current_date = datetime.now().date()
            next_date = current_date + timedelta(days=1)

            sales_records_count = db.session.query(func.count(SalesRecordItens.id)).filter(
                and_(
                    SalesRecordItens.created_at >= current_date,
                    SalesRecordItens.created_at < next_date,
                    SalesRecordItens.company_id == _company_id
                )
            ).scalar()

            orders = db.session.query(func.count(Orders.id)).filter(
                and_(
                    Orders.created_at >= current_date,
                    Orders.created_at < next_date,
                    Orders.company_id == _company_id
                )
            ).scalar()
            

            total_amount = db.session.query(func.sum(SalesRecord.total_amount)).filter(
                and_(
                    SalesRecord.created_at >= current_date,
                    SalesRecord.created_at < next_date,
                    SalesRecord.company_id == _company_id
                )
            ).scalar()
            
            total_orders = sales_records_count + orders
            
            json_response = {
                'total_orders': total_orders,
                'total_amount': total_amount if total_amount is not None else 0,
            }

            print(f"Sales records count for company {_company_id} on {current_date}: {sales_records_count}")

            return jsonify(
              json_response
            ), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
        except json.JSONDecodeError:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON format',
                'message': 'Failed to decode JSON data'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }), 500
        