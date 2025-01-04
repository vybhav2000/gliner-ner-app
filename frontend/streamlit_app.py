import pandas as pd
import streamlit as st
import requests
import os

BACKEND_HOST = os.getenv("BACKEND_HOST")
BACKEND_PORT = os.getenv("BACKEND_PORT")

st.title("Entity Prediction with GLiNER")

query = st.text_area("Enter your text here:")

labels = st.text_input("Enter labels (comma separated, e.g. Person, Location)")

if st.button("Predict Entities"):
    if query and labels:
        data = {"text": query, "labels": [label.strip() for label in labels.split(",")]}

        try:
            response = requests.post(f"http://{BACKEND_HOST}:{BACKEND_PORT}/gliner/predict", json=data)
            if response.status_code == 200:
                result = response.json()
                st.write("Predicted Entities:")
                df = pd.DataFrame.from_records(result["entities"])
                st.dataframe(df)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please provide both the text and labels.")
