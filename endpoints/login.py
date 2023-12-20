from flask import request, Blueprint, jsonify, render_template
import mysql.connector

login_blueprint = Blueprint('login', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@login_blueprint.route('/login', methods=['POST'])
def login():
    try:
        
        if request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            if not email or not password:
                return jsonify({"message": "Email dan password diperlukan"}), 400

            connection = create_db_connection()
            cursor = connection.cursor()

            query = "SELECT id_user, name, alamat, email, no_telpon, id_role FROM user WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                response = {
                    "message": "Login berhasil",
                    "id_user": user[0],
                    "name": user[1],
                    "alamat":user[2],
                    "email": user[3],
                    "no_telpon":user[4],
                    "id_role": user[5]
                }

                response = jsonify(response)
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                return response, 200
                
            else:
                response = jsonify({"message": "Email atau password salah"})
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                return response, 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500