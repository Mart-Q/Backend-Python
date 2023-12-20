from flask import request, Blueprint, jsonify
import mysql.connector

market_blueprint = Blueprint('market', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@market_blueprint.route('/market', methods=['GET','POST'])
def market():
    try:
        if request.method == 'GET':
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT id_market, nama_pasar, lokasi_pasar, link_google_map, longitude, latitude FROM market')
            market = cursor.fetchall()
            cursor.close()
            connection.close()

            market_list = []
            for item in market:
                market_obj = {
                    "id_market": item[0],
                    "nama_pasar": item[1],
                    "lokasi_pasar":item[2],
                    "link_google_map":item[3],
                    "longitude":item[4],
                    "latitude":item[5]
                }
                market_list.append(market_obj)

            response = jsonify({'market': market_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'POST':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO market (nama_pasar, lokasi_pasar, link_google_map, longitude, latitude) VALUES (%s, %s, %s, %s, %s)"
            data = (request.json['nama_pasar'], request.json['lokasi_pasar'], request.json['link_google_map'], request.json['longitude'], request.json['latitude'])
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": "Data market berhasil ditambahkan"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@market_blueprint.route('/market/<int:id>', methods=['PUT', 'DELETE'])
def update_market(id):
    try:
        if request.method == 'PUT':
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE market SET "
            data = []

            if 'nama_market' in request.json:
                update_query += "nama_market = %s, "
                data.append(request.json['nama_market'])
            if 'lokasi_pasar' in request.json:
                update_query += "lokasi_pasar = %s, "
                data.append(request.json['lokasi_pasar'])
            if 'link_google_map' in request.json:
                update_query += "link_google_map = %s, "
                data.append(request.json['link_google_map'])
            if 'longitude' in request.json:
                update_query += "longitude = %s, "
                data.append(request.json['longitude'])
            if 'latitude' in request.json:
                update_query += "latitude = %s, "
                data.append(request.json['latitude'])

            update_query = update_query.rstrip(', ')

            update_query += " WHERE id_market = %s"
            data.append(id)

            cursor.execute(update_query, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": f"Data market berhasil diperbarui untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'DELETE':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM market WHERE id_market = %s"
            data = (id,)
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()

            response = jsonify({"message": f"Data market berhasil dihapus untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

