from flask import Flask, request, jsonify, Blueprint
import tensorflow as tf
import joblib
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer

generator_blueprint = Blueprint('generator',__name__)

model = tf.keras.models.load_model(r"lstm_model.h5")
tokenizer = joblib.load(r"model_tokenizer.joblib")

max_sequence_length = model.input_shape[1]

def generate_recipe(seed_text, next_words, model, tokenizer, max_sequence_length):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_sequence_length, padding='pre')
        predicted_probabilities = model.predict(token_list, verbose=0)

        predicted_index = np.argmax(predicted_probabilities)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        seed_text += " " + output_word

    return seed_text

@generator_blueprint.route('/generate', methods=['POST'])
def generate():
    try:
        input_resep = request.json.get('input_resep')
        generated_recipe = generate_recipe(input_resep, 20, model, tokenizer, max_sequence_length)

        response_json = {'generated_recipe': generated_recipe}
        
        response = jsonify(response_json)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 201

    except Exception as e:
        return jsonify({'error': str(e)})

