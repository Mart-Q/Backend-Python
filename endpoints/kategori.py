from flask import request, Blueprint, jsonify
import mysql.connector

kategori_blueprint = Blueprint('kategori', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@kategori_blueprint.route('/kategori', methods=['GET','POST'])
def kategori():
    try:
        if request.method == 'GET':
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT id_kategori, nama_kategori, image_url FROM kategori')
            kategori = cursor.fetchall()
            cursor.close()
            connection.close()

            kategori_list = []
            for item in kategori:
                kategori_obj = {
                    "id_kategori": item[0],
                    "nama_kategori": item[1],
                    "image_url": item[2]
                }
                kategori_list.append(kategori_obj)

            response = jsonify({'kategori': kategori_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'POST':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO kategori (nama_kategori, image_url) VALUES (%s, %s)"
            data = (request.json['nama_kategori'], request.json['image_url'])
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": "Data kategori berhasil ditambahkan"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@kategori_blueprint.route('/kategori/<int:id>', methods=['PUT', 'DELETE'])
def update_kategori(id):
    try:
        if request.method == 'PUT':
            connection = create_db_connection()
            cursor = connection.cursor()
            
            if 'nama_kategori' in request.json: 
                sql = "UPDATE kategori SET nama_kategori = %s WHERE id_kategori = %s"
                data = (request.json['nama_kategori'], id)  
                cursor.execute(sql, data)

            if 'image_url' in request.json:  
                sql = "UPDATE kategori SET image_url = %s WHERE id_kategori = %s"
                data = (request.json['image_url'], id) # 'id' sesuai dengan ID kategori yang diinginkan
                cursor.execute(sql, data)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            response = jsonify({"message": f"Data kategori berhasil diperbarui untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'DELETE':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM kategori WHERE id_kategori = %s"
            data = (id,)
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()

            response = jsonify({"message": f"Data kategori berhasil dihapus untuk ID {id}"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

