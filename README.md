# Cloud Computing Path
Create REST API and deploying to Google Cloud Platform using [Cloud Function]. Creating databse using [Compute Engine] and storing images using [Cloud Storage]
The CC team consist of:
- Andi Muhammad Ichsan Jalaluddin (C183BSY3323)
- Andi Muhammad Yanwar (C008BSY4057)

### API
We using Python Flask to build the API's that'll consume to MD and ML
[![N|Solid](https://vercel.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fe5382hct74si%2F6Dqa9T8XOOC95yJb0z9jew%2Fce4932b8d23046f260510e24c1ec39e1%2Fthumbnail.png&w=1920&q=75&dpl=dpl_8whFbfnjCmzPv538NhNbpsGCuH7g)](https://flask.palletsprojects.com/en/3.0.x/)

### How to Use
##### 1. Clone this repository
#
```
git clone https://github.com/Mart-Q/Backend-Python.git
```

##### 2. Install requirements
#
```
pip install -r requirements.txt
```

#### Base URL:
|  https://us-central1-capstone-martq.cloudfunctions.net/dbmartq/

#### Method:
| GET

- Show list Users
```
GET {{host}}/dbmartq/users
```
Response:
```
{
  "alamat": "Jl. Kaliurang",
  "email": "tiara@email.com",
  "id_user": 7,
  "name": "Tiara Andini",
  "no_telpon": "08123456789",
  "password": "tiara"
  "role": "Customer"
}
```

- Show list Produk
```
GET {{host}}/dbmartq/produk
```
Response:
```
{
  "Harga": 5500,
  "Image_URL": "https://storage.googleapis.com/storage-gambar-menu/Makanan/Dada%20ayam",
  "Kategori": "Ikan & Daging",
  "Nama_Produk": "Dada Ayam 100 gram",
  "Stock": 20,
  "id_produk": 1
}
```

- show list kategori
```
GET {{host}}/dbmartq/kategori
```
Response:
```
{
    "id_kategori": 1,
    "image_url": "https://storage.googleapis.com/storage-gambar-menu/Kategori/Sayur%20%26%20Buah.png",
    "nama_kategori": "Sayur & Buah"
}
```

- show list roles
```
GET {{host}}/dbmartq/roles
```
Response:
```
{
    "id_role": 1,
    "name": "Admin"
}
``` 
- show list market
```
GET {{host}}/dbmartq/market
```
Response:
```
{
    "id_market": 1,
    "latitude": "-7.75977826",
    "link_google_map": "https://maps.app.goo.gl/GWij7DLxcuPwhjhYA",
    "lokasi_pasar": "Jl. Ring Road Utara No.414, Ngringin, Condongcatur",
    "longitude": "-249.5927909",
    "nama_pasar": "Pasar Condongcatur"
}
``` 
- show list seller
```
GET {{host}}/dbmartq/seller
```
Response:
```
{
    "id_market": 2,
    "id_seller": 1,
    "name": "Fulan"
}
``` 

```
{
    "Biaya Kirim": 3000,
    "Produk": [
        {
            "name": "Pokcoy 100 gram"
        }
    ],
    "Status": "Pesanan Sedang Disiapkan",
    "Status Pembayaran": "unpaid",
    "Total Harga": 51000,
    "Waktu": "Wed, 20 Dec 2023 17:02:16 GMT",
    "id_market": "Pasar Condongcatur",
    "id_pesanan": 39,
    "id_rekening": null,
    "id_user": 7,
    "is_delivery": "False"
}
```

#### Method:
| POST

- Login
```
POST {{host}}/dbmartq/login
```
- Request JSON
```
{
    "email":"tiara@email.com",
    "password":"tiara"
}
```
- Response:
```
{
    "alamat": "Jl. Kaliurang, Gg. Pamungkas Jl. Pogung Baru No.Km. 5,3 Blok W5",
    "email": "tiara@email.com",
    "id_role": 3,
    "id_user": 7,
    "message": "Login berhasil",
    "name": "Tiara Andini",
    "no_telpon": "08123456789"
}
```

### MODEL Machine Learning
From Machine Learning using library Tensorflow, pickle, and joblib 

#### MODEL API:
```
GET {{host}}/dbmartq/recommender
```

Response:
```
{
    "input_ingredients": [
        ""
    ],
    "recommendations": [
        "gurame saus padang",
        "gurame crispy asam manis ala amih fatih",
        "gurame crispy saus tiram brokoli",
        "gurame kecap",
        "gurame panggang teplon padang*"
    ]
}
```
And the rest of model for develop is:
- Daily Recommended recipe
- Recipe Generator

   [Cloud Function]: <https://cloud.google.com/functions/docs>
   [Compute Engine]: <https://cloud.google.com/compute/docs?hl=id>
   [Cloud Storage]: <https://cloud.google.com/storage>

For More Documentation:
- https://documenter.getpostman.com/view/30300359/2s9YkgEm9X
- https://documenter.getpostman.com/view/30300359/2s9Ykn8hEU

