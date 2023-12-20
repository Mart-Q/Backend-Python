from flask import request, Blueprint, jsonify
import mysql.connector

user_blueprint = Blueprint('user', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@user_blueprint.route('/users', methods=['GET','POST'])
def users():
    try:
        if request.method == 'GET':
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT user.id_user, user.name, user.alamat, user.email, user.no_telpon, user.password, role.name FROM user INNER JOIN role ON user.id_role = role.id_role')
            users = cursor.fetchall()
            cursor.close()
            connection.close()

            user_list = []
            for item in users:
                user_obj = {
                    "id_user": item[0],
                    "name": item[1],
                    "alamat": item[2],
                    "email": item[3],
                    "no_telpon": item[4],
                    "password": item[5],
                    "role": item[6]
                }
                user_list.append(user_obj)

            response = jsonify({'users': user_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method =='POST':
            connection = create_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO user (name, alamat, email, no_telpon, password, id_role) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (request.json['name'], request.json['alamat'], request.json['email'], request.json['no_telpon'], request.json['password'], request.json['id_role'])
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()

            response = jsonify({"message": "Data user berhasil ditambahkan"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/users/email/<string:email>', methods=['GET'])
def user_email(email):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT user.id_user, user.name, user.alamat, user.email, user.no_telpon, user.password, role.name FROM user INNER JOIN role ON user.id_role = role.id_role WHERE user.email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            user_obj = {
                "id_user": user[0],
                "name": user[1],
                "alamat": user[2],
                "email": user[3],
                "no_telpon": user[4],
                "password": user[5],
                "role": user[6]
            }
            response = jsonify({'user': user_obj})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        else:
            return jsonify({"message": "Pengguna dengan email tersebut tidak ditemukan"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/users/<int:id>/multiple', methods=['PUT'])
def update_user_attribute(id, attribute):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        update_query = "UPDATE user SET "
        data = []

        if 'name' in request.json:
            update_query += "name = %s, "
            data.append(request.json['name'])
        if 'email' in request.json:
            update_query += "email = %s, "
            data.append(request.json['email'])
        if 'password' in request.json:
            update_query += "password = %s, "
            data.append(request.json['password'])

        update_query = update_query.rstrip(', ')

        update_query += " WHERE id_user = %s"
        data.append(id)

        cursor.execute(update_query, data)
        connection.commit()
        cursor.close()
        connection.close()

        response = jsonify({"message": f"Atribut pengguna berhasil diperbarui untuk ID {id}"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM user WHERE id_user = %s"
        data = (id,)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
        
        response = jsonify({"message": f"Data user berhasil dihapus untuk ID {id}"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500