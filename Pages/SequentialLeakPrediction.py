#!/usr/bin/env python
# coding: utf-8

# In[3]:
import os
#import navbar
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime
import matplotlib.pyplot as plt

st.header("Sequential Leak Prediction")

# Display the menu
#navbar.nav('Sequential Leak Prediction')

model_path = 'D:/OneDrive - The Hong Kong Polytechnic University/PhD Database/CleanData/Sequential_Modeling/DataPlay/ttnf1.keras'
model = load_model(model_path)

# Define a function for prediction
def predict(spatial_data, temporal_data):
    spatial_data = np.array(spatial_data).reshape(1, -1, 2)
    temporal_data = np.array(temporal_data).reshape(1, -1, len(temporal_data[0]))
    prediction = model.predict([spatial_data, temporal_data])
    return prediction[0][0]

# Streamlit app layout
st.title('Single Point Prediction')

# User input for spatial data
st.subheader('Spatial Data')
lat = st.number_input('Latitude', min_value=22.15, max_value=22.65, value=22.30)
lon = st.number_input('Longitude', min_value=113.80, max_value=114.40, value=114.00)
spatial_data = [[lat, lon]]
    
# Define a function for prediction
def predict(spatial_data, temporal_data):
    spatial_data = np.array(spatial_data).reshape(1, -1, 2)
    temporal_data = np.array(temporal_data).reshape(1, -1, len(temporal_data[0]))
    prediction = model.predict([spatial_data, temporal_data])
    return prediction[0][0]

# User input for temporal data
st.subheader('Temporal Data')
doi = st.date_input('Installation Date (DOI)', value=datetime(2000, 1, 1).date())
timestamp = st.date_input('Failure Date', value=datetime(2023, 1, 1).date())
nopf = st.selectbox('Number of Previous Failures (NOPF)', options=[0, 1, 2])
time_prev_failure = st.number_input('Time of Previous Failure (Yrs.)', min_value=0.0, value=0.0)

# Convert dates to numerical format (e.g., timestamp)
doi_datetime = datetime.combine(doi, datetime.min.time())
failure_datetime = datetime.combine(timestamp, datetime.min.time())
doi_timestamp = doi_datetime.timestamp()
failure_timestamp = failure_datetime.timestamp()

# Automatically set time_prev_failure to 0 if nopf is 0
if nopf == 0:
    time_prev_failure = 0.0

temporal_data = [[doi_timestamp, failure_timestamp, nopf, time_prev_failure]]

# Prediction button
if st.button('Predict'):
    # Ensure time_prev_failure is set to 0 if nopf is 0
    if nopf == 0:
        time_prev_failure = 0.0
        temporal_data = [[doi_timestamp, failure_timestamp, nopf, time_prev_failure]]
    
    result = predict(spatial_data, temporal_data)
    st.write(f'Prediction: {result}')