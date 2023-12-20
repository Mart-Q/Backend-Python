from flask import request, Blueprint, jsonify
import mysql.connector

roles_blueprint = Blueprint('roles', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@roles_blueprint.route('/roles', methods=['GET'])
def get_roles():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM role')
        roles = cursor.fetchall()
        cursor.close()
        connection.close()

        roles_list = []
        for role in roles:
            role_obj = {
                "id_role": role[0],
                "name": role[1]
            }
            roles_list.append(role_obj)

        response = jsonify({"roles": roles_list})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@roles_blueprint.route('/roles', methods=['POST'])
def create_role():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO role (name) VALUES (%s)"
        data = (request.json['name'],)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
        
        response = jsonify({"message": "Data berhasil ditambahkan ke tabel role"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@roles_blueprint.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE role SET name = %s WHERE id_role = %s"
        data = (request.json['name'], id)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
        
        response = jsonify({"message": f"Data berhasil diperbarui untuk ID {id}"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@roles_blueprint.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM role WHERE id_role = %s"
        data = (id,)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
    
        response = jsonify({"message": f"Data berhasil dihapus untuk ID {id}"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500