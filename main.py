from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from endpoints.user import user_blueprint
from endpoints.login import login_blueprint
from endpoints.roles import roles_blueprint
from endpoints.produk import produk_blueprint
from endpoints.kategori import kategori_blueprint
from endpoints.status import status_blueprint
from endpoints.pesanan import pesanan_blueprint
from endpoints.market import market_blueprint
from endpoints.rekening import rekening_blueprint
from endpoints.seller import seller_blueprint

from modell.daily import daily_blueprint
from modell.generator import generator_blueprint
from modell.recommender import recommender_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(roles_blueprint)
app.register_blueprint(produk_blueprint)
app.register_blueprint(kategori_blueprint)
app.register_blueprint(status_blueprint)
app.register_blueprint(pesanan_blueprint)
app.register_blueprint(market_blueprint)
app.register_blueprint(rekening_blueprint)
app.register_blueprint(seller_blueprint)

app.register_blueprint(daily_blueprint)
app.register_blueprint(generator_blueprint)
app.register_blueprint(recommender_blueprint)



def dbmartq(request):
    if request.method == 'GET':
        if request.path == '/login':
            return login_blueprint.login()
        elif request.path == '/roles':
            return roles_blueprint.get_roles()
        elif request.path == '/produk':
            return produk_blueprint.produk()
        elif request.path.startswith('/produk'):
            id_produk = int(request.path.split('/')[-1])
            return produk_blueprint.get_produk_by_id(id_produk)
        elif request.path == '/kategori':
            return kategori_blueprint.get_kategori()
        elif request.path =='/users':
            return user_blueprint.users()
        elif request.path =='/users':
            return user_blueprint.user_email()
        elif request.path =='/status':
            return status_blueprint.status()
        elif request.path =='/pesanan':
            return pesanan_blueprint.get_pesanan()
        elif request.path.startswith('/pesanan'):
            id_pesanan = int(request.path.split('/')[-1])
            return pesanan_blueprint.get_pesanan_by_user(id_pesanan)
        elif request.path == '/seller':
            return seller_blueprint.seller()
        elif request.path =='/market':
            return market_blueprint.market()
        elif request.path =='/rekening':
            return rekening_blueprint.rekening()

        #model
        elif request.path == '/recommender':
            return recommender_blueprint.recommender()

    elif request.method == 'POST':
        if request.path == '/login':
            return login_blueprint.login()
        elif request.path == '/roles':
            return roles_blueprint.get_roles()
        elif request.path == '/produk':
            return produk_blueprint.produk()
        elif request.path == '/kategori':
            return kategori_blueprint.create_kategori()
        elif request.path =='/users':
            return user_blueprint.users()
        elif request.path == '/seller':
            return seller_blueprint.seller()
        elif request.path == '/market':
            return market_blueprint.market()
        elif request.path == '/rekening':
            return rekening_blueprint.rekening()
        elif request.path == '/pesanan':
            return pesanan_blueprint.get_pesanan()
        
        #model
        elif request.path == '/daily':
            return daily_blueprint.daily()
        elif request.path == '/generate':
            return generator_blueprint.generate()

    elif request.method == 'PUT':
        if request.path.startswith('/produk'):
            id_produk = int(request.path.split('/')[-1])
            return produk_blueprint.update_produk(id_produk)
        elif request.path.startswith('/kategori'):
            id_kategori = int(request.path.split('/')[-1])
            return kategori_blueprint.update_kategori(id_kategori)
        elif request.path.startswith('/users'):
            id_user = int(request.path.split('/')[-2])
            multiple = request.path.split('/')[-1]
            return user_blueprint.update_user_attribute(id_user, multiple)
        elif request.path.startswith('/market'):
            id_market = int(request.path.split('/')[-1])
            return market_blueprint.update_market(id_market)
        elif request.path.startswith('/rekening'):
            id_rekening = int(request.path.split('/')[-1])
            return rekening_blueprint.update_rekening(id_rekening)
        elif request.path.startswith('/pesanan'):
            id_pesanan = int(request.path.split('/')[-2])
            edit_produk = request.path.split('/')[-1]
            return pesanan_blueprint.update_pesanan_produk(id_pesanan, edit_produk)
        elif request.path.startswith('/seller'):
            id_seller = int(request.path.split('/')[-1])
            return seller_blueprint.update_seller(id_seller)

    elif request.method == 'DELETE':
        if request.path.startswith('/produk'):
            id_produk = int(request.path.split('/')[-1])
            return produk_blueprint.update_produk(id_produk)
        elif request.path.startswith('/kategori'):
            id_kategori = int(request.path.split('/')[-1])
            return kategori_blueprint.delete_kategori(id_kategori)
        elif request.path.startswith('/users'):
            id_user = int(request.path.split('/')[-1])
            return user_blueprint.delete_user(id_user)
        elif request.path.startswith('/market'):
            id_market = int(request.path.split('/')[-1])
            return market_blueprint.delete_market(id_market)
        elif request.path.startswith('/rekening'):
            id_rekening = int(request.path.split('/')[-1])
            return rekening_blueprint.update_rekening(id_rekening)
        elif request.path.startswith('/pesanan'):
            id_pesanan = int(request.path.split('/')[-1])
            return pesanan_blueprint.delete_pesanan(id_pesanan)
        elif request.path.startswith('/seller'):
            id_seller = int(request.path.split('/')[-1])
            return seller_blueprint.update_seller(id_seller)

    else:
        return 'Method not allowed', 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)