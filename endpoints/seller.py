from flask import request, Blueprint, jsonify
import mysql.connector

seller_blueprint = Blueprint('seller', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@seller_blueprint.route('/seller', methods=['GET','POST'])
def seller():
    try:
        if request.method == 'GET':
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT id_seller, name, id_market FROM seller')
            seller = cursor.fetchall()
            cursor.close()
            connection.close()

            seller_list = []
            for item in seller:
                seller_obj = {
                    "id_seller": item[0],
                    "name": item[1],
                    "id_market": item[2]
                }
                seller_list.append(seller_obj)

            response = jsonify({'seller': seller_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'POST':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO seller (name, id_market) VALUES (%s, %s)"
            data = (request.json['name'], request.json['id_market'])
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": "Data seller berhasil ditambahkan"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@seller_blueprint.route('/seller/<int:id>', methods=['PUT', 'DELETE'])
def update_seller(id):
    try:
        if request.method == 'PUT':
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE seller SET "
            data = []

            if 'name' in request.json:
                update_query += "name = %s, "
                data.append(request.json['name'])
            if 'id_rekening' in request.json:
                update_query += "id_rekening = %s, "
                data.append(request.json['id_rekening'])

            update_query = update_query.rstrip(', ')

            update_query += " WHERE id_user = %s"
            data.append(id)

            cursor.execute(update_query, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": f"Data seller berhasil diperbarui untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'DELETE':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM seller WHERE id_seller = %s"
            data = (id,)
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()

            response = jsonify({"message": f"Data seller berhasil dihapus untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

