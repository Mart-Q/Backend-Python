from flask import Flask, render_template, request, jsonify, Response, Blueprint
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import json

recommender_blueprint = Blueprint('recommender',__name__)

with open(r'recipe_recommendation.pkl', 'rb') as model_file:
    cosine_sim = pickle.load(model_file)

df = pd.read_csv(r"dataset_recipe.csv")

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined'])

def recommend_recipe(selected_ingredients, df, cosine_sim=cosine_sim):
    selected_text = ' '.join(selected_ingredients)
    df_temp = df.copy()
    df_temp['selected'] = selected_text
    df_temp['combined_selected'] = df_temp['Title'] + ' ' + df_temp['selected']

    tfidf_matrix_selected = tfidf_vectorizer.transform(df_temp['combined_selected'])
    cosine_sim_selected = linear_kernel(tfidf_matrix_selected, tfidf_matrix)
    recommended_indices = cosine_sim_selected[0].argsort()[:-6:-1]

    filtered_indices = [idx for idx in recommended_indices if selected_text.lower() in df['Title'].iloc[idx].lower()]
    remaining_recommendations = 5 - len(filtered_indices)

    additional_indices = [idx for idx in recommended_indices if idx not in filtered_indices][:remaining_recommendations]
    filtered_indices += additional_indices

    recommended_recipes = df['Title'].iloc[filtered_indices]

    return recommended_recipes.tolist()


@recommender_blueprint.route('/recommender', methods=['GET'])
def recommender():
    try:
        selected_ingredients = request.args.get('ingredients', '').split(',')
        recommendations = recommend_recipe(selected_ingredients, df)

        json_data = {
            'input_ingredients': selected_ingredients,
            'recommendations': recommendations
        }

        response = jsonify(json_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers["Content-Disposition"] = "attachment; filename=recommendations.json"
        return response, 200

    except Exception as e:
        return jsonify({'error': str(e)})


