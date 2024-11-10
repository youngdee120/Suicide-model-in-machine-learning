from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import re
import string
import random

app = Flask(__name__)

# Load the model and data
with open('model.pickle', 'rb') as file:
    model = pickle.load(file)

with open('vocabulary.txt', 'r', encoding="utf-8") as file:
    vocabulary = file.read().splitlines()

with open('/home/kush/Projects/Data Science/loice suicide model/model/suicidal_reasons.txt', 'r', encoding="utf-8") as file:
    suicidal_reasons = file.read().splitlines()

with open('/home/kush/Projects/Data Science/loice suicide model/model/non_suicidal_reasons.txt', 'r', encoding="utf-8") as file:
    non_suicidal_reasons = file.read().splitlines()

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    text = re.sub(r'\d+', '', text)
    return text

# Vectorizer function
def vectorizer(ds, vocabulary):
    sentence_lst = np.zeros(len(vocabulary))
    for i, vocab_word in enumerate(vocabulary):
        if vocab_word in ds.split():
            sentence_lst[i] = 1
    return np.array([sentence_lst], dtype=np.float32)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['text']
    processed_text = preprocess_text(user_input)
    vectorized_text = vectorizer(processed_text, vocabulary)
    
    prediction = model.predict(vectorized_text)[0]
    
    if prediction == 1:
        reason = random.choice(suicidal_reasons)
        result = {"classification": "Suicidal", "reason": reason}
    else:
        reason = random.choice(non_suicidal_reasons)
        result = {"classification": "Non-Suicidal", "reason": reason}
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)