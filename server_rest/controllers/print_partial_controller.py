from flask import request, jsonify
from controllers.mqtt_controller import MQTTController
import json

class PrintPartialController:
    @staticmethod
    def print_partial():
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                'success': False,
                'error': 'No input data provided'
            }), 400
        

        _company_id = json_data.get('company_id',None)

        if not _company_id:
            return jsonify({
                'success': False,
                'error': 'Company ID is required'
            }), 400
        
        _table_id = json_data.get('table_id',None)
        if not _table_id:
            return jsonify({
                'success': False,
                'error': 'Table ID is required'
            }), 400
        
        try:
            send_content = { 
                'company_id': _company_id,
                'table_id': _table_id,
                'action': 'print_partial'
            }
            

            _send_partial = MQTTController('B906')
            _send_partial.connect()
            _send_partial.publish('go/B906/print', json.dumps(send_content))
            _send_partial.disconnect()
            return jsonify({
                'success': True,
                'message': 'Print partial request sent successfully'
            }), 200
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
        