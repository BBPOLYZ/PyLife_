import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

# Function to make predictions
def predict_failure(model, input_data, numerical_features, categorical_features):
    columns = numerical_features + categorical_features
    input_df = pd.DataFrame([input_data], columns=columns)
    return model.predict(input_df)[0]

# Function to load the models
@st.cache_resource
def load_models(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

# Load all models
models = load_models('FW_123.pkl')
model_first_failure = models['model_first_failure']
model_second_failure = models['model_second_failure']
model_third_failure = models['model_third_failure']

# Streamlit app
st.title("Single Point Prediction")

# Tabs for different failure predictions
tab1, tab2, tab3 = st.tabs(["Time to First Failure", "Time to Second Failure", "Time to Third Failure"])

# Features for each model
numerical_features_model1 = ['Year of Installation', 'SA', 'PRESSURE(bar)', 'AADT','MWI_1']
categorical_features_model1 = ['A_MAT', 'LANDUSE', 'TYPE', 'LPR_Corros']

numerical_features_model2 = ['Year of Installation', 'Age at 1st Failure', 'SA', 'PRESSURE(bar)', 'AADT','MWI_1']
categorical_features_model2 = ['A_MAT', 'LANDUSE', 'TYPE', 'LPR_Corros']

numerical_features_model3 = ['Age at 1st Failure', 'Age at 2nd Failure', 'SA', 'PRESSURE(bar)', 'AADT','MWI_1']
categorical_features_model3 = ['A_MAT', 'LANDUSE', 'TYPE', 'LPR_Corros']

def input_form(numerical_features, categorical_features, key_prefix):
    inputs = {}
    cols = st.columns(2)
    for i, feature in enumerate(numerical_features):
        if feature == 'Year of Installation':
            inputs[feature] = cols[i % 2].number_input(feature, min_value=1900, max_value=9999, key=f"{key_prefix}_{feature}", help=f"Enter the {feature.lower()}")
        else:
            inputs[feature] = cols[i % 2].number_input(feature, key=f"{key_prefix}_{feature}", help=f"Enter the {feature.lower()}")
    for i, feature in enumerate(categorical_features):
        if feature == 'LANDUSE':
            options = ["URBAN", "RURAL", "WATERBODY"]
        elif feature == 'LPR_Corros':
            options = ["Non-Corrosive", "Mildly Corrosive", "Highly-Corrosive"]
        elif feature == 'DEFECT1LV1':
            options = ["C01", "C02", "C03", "C04", "C05"]
        elif feature == 'DEF_NATURE':
            options = ["M", "N", "J"]
        elif feature == 'TYPE':
            options = ["CARRIAGEWAY", "FOOTWAY", "Other Location"]
        else:
            options = ["DI","S","SS","PE"]
        inputs[feature] = cols[i % 2].selectbox(feature, options=options, key=f"{key_prefix}_{feature}", help=f"Select the {feature.lower()}")
    return inputs

with tab1:
    st.header("Time to First Failure Prediction")
    input_data = input_form(numerical_features_model1, categorical_features_model1, "first_failure")
    if st.button("Predict First Failure", key="first_failure_button"):
        prediction = predict_failure(model_first_failure, list(input_data.values()), numerical_features_model1, categorical_features_model1)
        st.success(f"Predicted time to first failure: {prediction}")

with tab2:
    st.header("Time to Second Failure Prediction")
    input_data = input_form(numerical_features_model2, categorical_features_model2, "second_failure")
    if st.button("Predict Second Failure", key="second_failure_button"):
        prediction = predict_failure(model_second_failure, list(input_data.values()), numerical_features_model2, categorical_features_model2)
        st.success(f"Predicted time to second failure: {prediction}")

with tab3:
    st.header("Time to Third Failure Prediction")
    input_data = input_form(numerical_features_model3, categorical_features_model3, "third_failure")
    if st.button("Predict Third Failure", key="third_failure_button"):
        prediction = predict_failure(model_third_failure, list(input_data.values()), numerical_features_model3, categorical_features_model3)
        st.success(f"Predicted time to third failure: {prediction}")

# Section for CSV upload and batch prediction
st.header("Batch Prediction from CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())

    if st.button("Predict from CSV"):
        # Ensure the CSV has the required columns for each model
        required_columns_model1 = set(numerical_features_model1 + categorical_features_model1)
        required_columns_model2 = set(numerical_features_model2 + categorical_features_model2)
        required_columns_model3 = set(numerical_features_model3 + categorical_features_model3)

        missing_columns_model1 = required_columns_model1 - set(data.columns)
        missing_columns_model2 = required_columns_model2 - set(data.columns)
        missing_columns_model3 = required_columns_model3 - set(data.columns)

        if missing_columns_model1:
            st.error(f"The uploaded CSV is missing the following columns for the first failure prediction: {missing_columns_model1}")
        elif missing_columns_model2 - {'Age at 1st Failure'}:
            st.error(f"The uploaded CSV is missing the following columns for the second failure prediction: {missing_columns_model2 - {'Age at 1st Failure'}}")
        elif missing_columns_model3 - {'Age at 1st Failure', 'Age at 2nd Failure'}:
            st.error(f"The uploaded CSV is missing the following columns for the third failure prediction: {missing_columns_model3 - {'Age at 1st Failure', 'Age at 2nd Failure'}}")
        else:
            # Predict first failure
            data['First Failure Prediction'] = data.apply(lambda row: predict_failure(model_first_failure, row[numerical_features_model1 + categorical_features_model1], numerical_features_model1, categorical_features_model1), axis=1)
            
            # Prepare data for second failure prediction
            data['Age at 1st Failure'] = data['First Failure Prediction']
            
            # Predict second failure
            data['Second Failure Prediction'] = data.apply(lambda row: predict_failure(model_second_failure, row[numerical_features_model2 + categorical_features_model2], numerical_features_model2, categorical_features_model2), axis=1)
            
            # Prepare data for third failure prediction
            data['Age at 2nd Failure'] = data['Second Failure Prediction']
            
            # Predict third failure
            data['Third Failure Prediction'] = data.apply(lambda row: predict_failure(model_third_failure, row[numerical_features_model3 + categorical_features_model3], numerical_features_model3, categorical_features_model3), axis=1)
            
            # Display final data with predictions
            st.write("Predictions:")
            st.write(data)
            
            # Save final data to CSV
            data.to_csv("predictions.csv", index=False)
            st.success("Predictions saved to predictions.csv")
            
            # Visualization
            fig = px.scatter(data, x='Year of Installation', y=['First Failure Prediction', 'Second Failure Prediction', 'Third Failure Prediction'], 
                             labels={'value': 'Time to Failure', 'variable': 'Failure Type'}, title="Failure Predictions")
            st.plotly_chart(fig)

# Sidebar for surface area calculation
st.sidebar.header("Calculate Surface Area")
length = st.sidebar.number_input("Enter the length of the pipe (m):", min_value=0.0, format="%.2f")
width = st.sidebar.number_input("Enter the width of the pipe (m):", min_value=0.0, format="%.2f")
if st.sidebar.button("Calculate Surface Area"):
    # Assuming the pipe is cylindrical, the surface area formula is: A = 2 * π * r * (r + h)
    # where r is the radius (width / 2) and h is the length of the cylinder.
    # For simplicity, π is approximated to 3.14159.
    radius = width / 2
    surface_area = 2 * 3.14159 * radius * (radius + length)
    st.sidebar.write(f"The surface area of the pipe is: {surface_area:.2f} square meters.")
