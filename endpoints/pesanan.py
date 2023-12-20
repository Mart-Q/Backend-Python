from flask import request, Blueprint, jsonify, json
import mysql.connector

pesanan_blueprint = Blueprint('pesanan', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

def pesanan_produk():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ("SELECT p.id_pesanan, p.id_user, CASE WHEN is_delivery = 1 THEN 'True' ELSE 'False' END AS is_delivery, p.id_rekening, m.nama_pasar, p.biaya_ongkos_kirim, p.Total_Harga, p.Waktu, p.Status_Pembayaran, p.Status, JSON_ARRAYAGG(JSON_OBJECT('name', pr.nama_produk)) AS Produk FROM pesanan p LEFT JOIN pesanan_produk r ON p.id_pesanan = r.id_pesanan LEFT JOIN produk pr ON r.nama_produk = pr.nama_produk LEFT JOIN market m ON p.id_market = m.id_market GROUP BY p.id_pesanan")
        cursor.execute(sql)
        pesanan = cursor.fetchall()
        cursor.close()
        connection.close()

        pesanan_list = []
        for item in pesanan:
            produk_json = json.loads(item[10])
            pesanan_obj = {
                "id_pesanan": item[0],
                "id_user": item[1],  
                "is_delivery": item[2],
                "id_rekening": item[3],
                "id_market": item[4],
                "Biaya Kirim": item[5],
                "Total Harga": item[6],
                "Waktu": item[7],
                "Status Pembayaran": item[8],
                "Status": item[9],
                "Produk": produk_json
            }
            pesanan_list.append(pesanan_obj)

        return pesanan_list

    except Exception as e:
        print("Error:", e)
        return []

@pesanan_blueprint.route('/pesanan', methods=['GET', 'POST'])
def get_pesanan():
    try:
        if request.method == 'GET':
            
            pesanan = pesanan_produk()

            response = jsonify({'pesanan': pesanan})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
        elif request.method == 'POST':
            
            id_user = request.json['id_user']
            is_delivery = request.json['is_delivery']
            id_rekening = request.json['id_rekening']
            id_market = request.json['id_market']
            biaya_ongkos_kirim = request.json['biaya_ongkos_kirim']
            total_harga = request.json['total_harga']
            status = request.json['status']
            produk_list = request.json['produk'] 

            connection = create_db_connection()
            cursor = connection.cursor()
            
            sql_pesanan = "INSERT INTO pesanan (id_user, is_delivery, id_rekening, id_market, biaya_ongkos_kirim, Total_Harga, status) VALUES (%s, %s, %s, %s, %s, %s, %s) "
            data_pesanan = (id_user, is_delivery, id_rekening, id_market, biaya_ongkos_kirim, total_harga, status)
            cursor.execute(sql_pesanan, data_pesanan)
            connection.commit()

            id_pesanan = cursor.lastrowid

            sql_produk_pesanan = "INSERT INTO pesanan_produk (id_pesanan, nama_produk) VALUES (%s, %s)"
            for nama_produk in produk_list:
                data_produk_pesanan = (id_pesanan, nama_produk)
                cursor.execute(sql_produk_pesanan, data_produk_pesanan)
                connection.commit()

            cursor.close()
            connection.close()

            response = jsonify({"message": "Data pesanan berhasil ditambahkan"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@pesanan_blueprint.route('/pesanan/<int:id_user>', methods=['GET'])
def get_pesanan_by_user(id_user):
    try:
        if request.method == 'GET':
            connection = create_db_connection()
            cursor = connection.cursor()

            sql = ("SELECT p.id_pesanan, p.id_user, CASE WHEN is_delivery = 1 THEN 'True' ELSE 'False' END AS is_delivery, p.id_rekening, m.nama_pasar, p.biaya_ongkos_kirim, p.Total_Harga, p.Waktu, p.Status_Pembayaran, p.Status, JSON_ARRAYAGG(JSON_OBJECT('name', pr.nama_produk)) AS Produk FROM pesanan p LEFT JOIN pesanan_produk r ON p.id_pesanan = r.id_pesanan LEFT JOIN produk pr ON r.nama_produk = pr.nama_produk LEFT JOIN market m ON p.id_market = m.id_market WHERE p.id_user = %s GROUP BY p.id_pesanan")
            cursor.execute(sql, (id_user,))
            pesanan = cursor.fetchall()
            cursor.close()
            connection.close()

            pesanan_list = []
            for item in pesanan:
                produk_json = json.loads(item[10])
                pesanan_obj = {
                    "id_pesanan": item[0],
                    "id_user": item[1],  
                    "is_delivery": item[2],
                    "id_rekening": item[3],
                    "id_market": item[4],
                    "Biaya Kirim": item[5],
                    "Total Harga": item[6],
                    "Waktu": item[7],
                    "Status Pembayaran": item[8],
                    "Status":item[9],
                    "Produk": produk_json
                }
                pesanan_list.append(pesanan_obj)

            response = jsonify({'pesanan': pesanan_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pesanan_blueprint.route('/pesanan/<int:id_pesanan>/produk', methods=['PUT'])
def update_pesanan_produk(id_pesanan):
    try:
        if request.method == 'PUT':
            new_produk_list = request.json['produk'] 

            connection = create_db_connection()
            cursor = connection.cursor()

            sql_delete_produk = "DELETE FROM pesanan_produk WHERE id_pesanan = %s"
            cursor.execute(sql_delete_produk, (id_pesanan,))
            connection.commit()

            sql_insert_produk = "INSERT INTO pesanan_produk (id_pesanan, nama_produk) VALUES (%s, %s)"
            for nama_produk in new_produk_list:
                data_produk_pesanan = (id_pesanan, nama_produk)
                cursor.execute(sql_insert_produk, data_produk_pesanan)
                connection.commit()

            cursor.close()
            connection.close()

            response = jsonify({"message": "Data produk pesanan berhasil diperbarui"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@pesanan_blueprint.route('/pesanan/<int:id_pesanan>', methods=['DELETE'])
def delete_pesanan(id_pesanan):
    try:
        if request.method == 'DELETE':
            connection = create_db_connection()
            cursor = connection.cursor()

            sql_delete_produk = "DELETE FROM pesanan_produk WHERE id_pesanan = %s"
            cursor.execute(sql_delete_produk, (id_pesanan,))

            sql_delete_pesanan = "DELETE FROM pesanan WHERE id_pesanan = %s"
            cursor.execute(sql_delete_pesanan, (id_pesanan,))

            connection.commit()

            cursor.close()
            connection.close()

            response = jsonify({"message": f"Pesanan dengan ID {id_pesanan} beserta produk berhasil dihapus"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500