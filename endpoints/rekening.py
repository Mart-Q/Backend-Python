from flask import request, Blueprint, jsonify
import mysql.connector

rekening_blueprint = Blueprint('rekening', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@rekening_blueprint.route('/rekening', methods=['GET','POST'])
def rekening():
    try:
        if request.method == 'GET':
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT rekening.id_rekening, rekening.nama_bank, rekening.no_rekening, seller.name FROM rekening INNER JOIN seller ON rekening.id_seller = seller.id_seller')
            rekening = cursor.fetchall()
            cursor.close()
            connection.close()

            rekening_list = []
            for item in rekening:
                rekening_obj = {
                    "id_rekening": item[0],
                    "nama_bank": item[1],
                    "no_rekening":item[2],
                    "atas_nama":item[3]
                }
                rekening_list.append(rekening_obj)

            response = jsonify({'rekening': rekening_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'POST':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO rekening (nama_bank, no_rekening, id_seller) VALUES (%s, %s, %s)"
            data = (request.json['nama_bank'], request.json['no_rekening'], request.json['id_seller'])
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": "Data rekening berhasil ditambahkan"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rekening_blueprint.route('/rekening/<int:id>', methods=['PUT', 'DELETE'])
def update_rekening(id):
    try:
        if request.method == 'PUT':
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = "UPDATE rekening SET "
            data = []
            if 'nama_bank' in request.json:
                update_query += "nama_bank = %s, "
                data.append(request.json['nama_bank'])
            elif 'no_rekening' in request.json:
                update_query += "no_rekening = %s, "
                data.append(request.json['no_rekening'])

            update_query = update_query.rstrip(', ')

            update_query += " WHERE id_rekening = %s"
            data.append(id)
            
            cursor.execute(update_query, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": f"Data rekening berhasil diperbarui untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'DELETE':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM rekening WHERE id_rekening = %s"
            data = (id,)
            cursor.execute(sql, data)

            connection.commit()
            cursor.close()
            connection.close()

            response = jsonify({"message": f"Data rekening berhasil dihapus untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

