import numpy as np
import pandas as pd
import pickle
import streamlit as st

st.header("Sequential Leak Prediction")

# Function to load the models
@st.cache_resource
def load_models(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

# Load all models
model_path = 'ttnf_rf_fw1.pkl'
models = load_models(model_path)
model = models['ttnf']

# Define a function for prediction
def predict(features):
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0]

# Streamlit app layout
st.title('Batch Prediction from CSV')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    
    # Display the data
    st.write("Data Preview:")
    st.write(data.head())
    
    # Ensure the required columns are present
    required_columns = ['Year of Installation', 'NOPF', 'APF', 'Length', 'Pressure',
                        'FAULT_TYPE', 'A_DIAM', 'Material', 'Urbanization', 'Soil Corrosivity',
                        'Latitude', 'Longitude', 'Effect of Traffic Load']
    
    if all(column in data.columns for column in required_columns):
        # Extract features
        features = data[required_columns]
        
        # Make predictions
        predictions = features.apply(lambda row: predict(row), axis=1)
        
        # Add predictions to the DataFrame
        data['Prediction'] = predictions
        
        # Display the predictions
        st.write("Predictions:")
        st.write(data)
    else:
        st.error(f"Expected {len(required_columns)} features, but got {features.shape[1]}. Please check the input data.")
else:
    st.error("The uploaded CSV file does not contain all the required columns.")
