from flask import Flask, request, jsonify, Blueprint
import json
import joblib
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise import Reader

daily_blueprint = Blueprint('daily',__name__)

with open(r'svd_model.pkl', 'rb') as pickle_file:
    svd_model = joblib.load(pickle_file)

file_path = r'dataset_daily.csv'
resep_df = pd.read_csv(file_path)

def recommend_recipe(user_id, svd_model, resep_df, trainset):
    recipes_to_recommend = []

    for item_id in resep_df['Title'].unique():
        if not trainset.knows_user(user_id) or not trainset.knows_item(item_id):
            recipes_to_recommend.append(item_id)

    return recipes_to_recommend[:5]

reader = Reader(rating_scale=(1, 500))
dataset = Dataset.load_from_df(resep_df[['User', 'Title', 'Loves']], reader)
trainset = dataset.build_full_trainset()

@daily_blueprint.route('/daily', methods=['POST'])
def daily():
    try:
        if request.method == 'POST':
            user_id = request.form['user_id']
            recommendations = recommend_recipe(user_id, svd_model, resep_df, trainset)

            response = jsonify({'user_id': user_id, 'recommendations': recommendations})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response, 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

