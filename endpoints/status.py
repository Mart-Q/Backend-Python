from flask import request, Blueprint, jsonify
import mysql.connector

status_blueprint = Blueprint('status', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@status_blueprint.route('/status', methods=['GET'])
def status():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM status_pesanan')
        status_pesanan = cursor.fetchall()
        cursor.close()
        connection.close()

        status_list = []
        for status in status_pesanan:
            status_obj = {
                "id_status_pesanan": status[0],
                "name": status[1]
            }
            status_list.append(status_obj)

        response = jsonify({'status': status_list})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500