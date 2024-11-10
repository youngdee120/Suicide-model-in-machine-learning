import streamlit as st
import pickle
import numpy as np
import re
import string
import random

# Load the model
with open('model.pickle', 'rb') as file:
    model = pickle.load(file)

# Load vocabulary
with open('vocabulary.txt', 'r', encoding="utf-8") as file:
    vocabulary = file.read().splitlines()

# Load reasons
with open('model/suicidal_reasons.txt', 'r', encoding="utf-8") as file:
    suicidal_reasons = file.read().splitlines()

with open('model/non_suicidal_reasons.txt', 'r', encoding="utf-8") as file:
    non_suicidal_reasons = file.read().splitlines()

# Preprocessing function
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove links
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    # Remove punctuation
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    return text

# Vectorizer function
def vectorizer(ds, vocabulary):
    vectorized_lst = []
    sentence_lst = np.zeros(len(vocabulary))
    for i, vocab_word in enumerate(vocabulary):
        if vocab_word in ds.split():
            sentence_lst[i] = 1
    vectorized_lst.append(sentence_lst)
    return np.array(vectorized_lst, dtype=np.float32)

# Streamlit app title and instructions
st.title("Suicide Prediction Model")
st.write("This model predicts if a given text is suicidal or non-suicidal and provides a reason for the classification.")

# User input
user_input = st.text_area("Enter the text to analyze")

# Predict button
if st.button("Predict"):
    if user_input:
        # Preprocess and vectorize input
        processed_text = preprocess_text(user_input)
        vectorized_text = vectorizer(processed_text, vocabulary)
        
        # Predict
        prediction = model.predict(vectorized_text)[0]
        
        # Select a reason based on prediction
        if prediction == 1:
            st.write("The text is classified as **Suicidal**.")
            reason = random.choice(suicidal_reasons)
        else:
            st.write("The text is classified as **Non-Suicidal**.")
            reason = random.choice(non_suicidal_reasons)
        
        # Display the reason
        st.write("**Reason:**", reason)
        
    else:
        st.write("Please enter some text for analysis.")
