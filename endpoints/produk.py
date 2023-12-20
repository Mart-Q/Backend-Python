from flask import request, Blueprint, jsonify
import mysql.connector

produk_blueprint = Blueprint('produk', __name__)

def create_db_connection():
    return mysql.connector.connect(
        host='34.128.86.2',  
        user='dbmartq',
        password='martkuy',
        database='capstone_martq'
    )

@produk_blueprint.route('/produk', methods=['GET'])
def get_produk():
    try:
        kategori_filter = request.args.get('kategori')

        connection = create_db_connection()
        cursor = connection.cursor()

        if kategori_filter:
            cursor.execute('SELECT produk.id_produk, produk.harga, produk.stock, produk.nama_produk, produk.image_url, kategori.nama_kategori FROM produk INNER JOIN kategori ON produk.id_kategori = kategori.id_kategori WHERE kategori.nama_kategori = %s', (kategori_filter,))
        else:
            cursor.execute('SELECT produk.id_produk, produk.harga, produk.stock, produk.nama_produk, produk.image_url, kategori.nama_kategori FROM produk INNER JOIN kategori ON produk.id_kategori = kategori.id_kategori')
        
        produk = cursor.fetchall()
        cursor.close()
        connection.close()

        produk_list = []
        for item in produk:
            produk_obj = {
                "id_produk": item[0],
                "Harga": item[1],  
                "Stock": item[2],
                "Nama_Produk": item[3],
                "Image_URL": item[4],
                "Kategori": item[5]
            }
            produk_list.append(produk_obj)

        response = jsonify({'produk': produk_list})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@produk_blueprint.route('/produk/<int:id>', methods=['GET'])
def get_produk_by_id(id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT produk.id_produk, produk.harga, produk.stock, produk.nama_produk, produk.image_url, kategori.nama_kategori FROM produk INNER JOIN kategori ON produk.id_kategori = kategori.id_kategori WHERE produk.id_produk = %s', (id,))
        produk = cursor.fetchone() 

        if not produk:
            return jsonify({"message": "Produk tidak ditemukan"}), 404

        produk_details = {
            "id_produk": produk[0],
            "Harga": produk[1],  
            "Stock": produk[2],
            "Nama_Produk": produk[3],
            "Image_URL": produk[4],
            "Kategori": produk[5]
        }

        cursor.close()
        connection.close()

        response = jsonify({'produk': produk_details})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tambahkan data baru ke tabel produk
@produk_blueprint.route('/produk', methods=['POST'])
def create_produk():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO produk (nama_produk, harga, stock, id_kategori, image_url, deskripsi, jumlah) VALUES (%s, %s, %s, %s, %s)"
        data = (request.json['nama_produk'], request.json['harga'], request.json['stock'], request.json['id_kategori'], request.json['image_url'], request.json['deskripsi'], request.json['jumlah'])
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
        
        response = jsonify({"message": "Data produk berhasil ditambahkan"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ngupdate data di tabel produk berdasarkan ID
@produk_blueprint.route('/produk/<int:id>', methods=['PUT'])
def update_produk(id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = "UPDATE produk SET "
        data = []
        if 'nama_produk' in request.json:
            update_query += "nama_produk = %s, "
            data.append(request.json['nama_produk'])
        elif 'harga' in request.json:
            update_query += "harga = %s, "
            data.append(request.json['harga'])
        elif 'stock' in request.json:
            update_query += "stock = %s, "
            data.append(request.json['stock'])
        elif 'id_kategori' in request.json:
            update_query += "id_kategori = %s, "
            data.append(request.json['id_kategori'])
        elif 'image_url' in request.json:
            update_query += "image_url = %s, "
            data.append(request.json['image_url'])
        elif 'deskripsi' in request.json:
            update_query += "deskripsi = %s, "
            data.append(request.json['deskripsi'])
        elif 'jumlah' in request.json:
            update_query += "jumlah = %s, "
            data.append(request.json['jumlah'])

        # Menghapus koma terakhir dari query
        update_query = update_query.rstrip(', ')
        
        # Menambahkan kondisi WHERE id_produk = <id>
        update_query += " WHERE id_produk = %s"
        data.append(id)

        cursor.execute(update_query, data)
        connection.commit()
        cursor.close()
        connection.close()
        
        response = jsonify({"message": f"Data produk berhasil diperbarui untuk ID {id}"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@produk_blueprint.route('/produk/<int:id>', methods=['DELETE'])
def delete_produk(id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM produk WHERE id_produk = %s"
        data = (id,)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()
        
        response = jsonify({"message": f"Data produk berhasil dihapus untuk ID {id}"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500