import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.util import Surv
import numpy as np

# Load your data
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

st.title('Kaplan-Meier Curves and Survival Regression for Water Pipeline Types')

# Input for file path
file_path = st.text_input('Enter the file path of your data:', 'C:/Users/21071252r/Desktop/Data Science Course/pylifewaterapp/Survival.csv')

if file_path:
    data = load_data(file_path)

    if data is not None:
        # Select pipeline types to compare
        pipeline_types = st.multiselect('Select pipeline types', data['A_MAT'].unique())

        if pipeline_types:
            plt.figure(figsize=(10, 6))

            for pipeline_type in pipeline_types:
                subset = data[data['A_MAT'] == pipeline_type]
                kmf = KaplanMeierFitter()
                kmf.fit(subset['Duration'], event_observed=subset['Status'], label=pipeline_type)
                kmf.plot_survival_function()

            plt.title('Kaplan-Meier Curves')
            plt.xlabel('Time')
            plt.ylabel('Survival Probability')
            st.pyplot(plt)

            # Define numerical features
            numerical_cols = ['No. of previous failures', 'LENGTH', 'A_DIAM', 'Year', 'PRESSURE(bar)', 'Failure Year', 
                              'AADT (traffic) ( When failure occurred )', 'Mean Dew Point (deg. C) ( When failure occurred )', 
                              'Mean Relative Humidity (%) ( When failure occurred )', 'Total Rainfall (mm) ( When failure occurred )']

            # Ensure all numerical columns are of numeric type
            data[numerical_cols] = data[numerical_cols].apply(pd.to_numeric)

            # One-hot encode categorical features
            categorical_cols = ['A_MAT', 'LANDUSE', 'LPR_Corros', 'FAULT_TYPE', 'DEFECT1LV1', 'DEF_NATURE', 'TYPE']
            data = pd.get_dummies(data, columns=categorical_cols)

            # Convert boolean columns to integers
            bool_cols = data.select_dtypes(include=['bool']).columns
            data[bool_cols] = data[bool_cols].astype(int)

            # Handle inf and NaN values
            data.replace([np.inf, -np.inf], np.nan, inplace=True)
            imputer = SimpleImputer(strategy='mean')
            data[numerical_cols] = imputer.fit_transform(data[numerical_cols])

            # Scale numerical features
            scaler = StandardScaler()
            data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

            # Check for multicollinearity
            vif_data = pd.DataFrame()
            vif_data["feature"] = data.columns
            vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(len(data.columns))]
            st.write("Variance Inflation Factors:")
            st.write(vif_data)

            # Prepare data for survival analysis
            y = np.array([(event, time) for event, time in zip(data['Status'].astype(bool), data['Duration'])],
                         dtype=[('Status', bool), ('Duration', float)])
            X = data.drop(columns=['Status', 'Duration'])

            # Run survival regression
            st.subheader('Survival Regression and Risk Scores')
            cph = CoxPHSurvivalAnalysis(0.1)
            if data.isnull().values.any():
                st.write("Data contains NaN values. Please clean your data before fitting the model.")
            elif np.isinf(data.values).any():
                st.write("Data contains infinite values. Please clean your data before fitting the model.")
            else:
                try:
                    cph.fit(X, y)
                    st.write("Model coefficients:")
                    st.write(pd.DataFrame(cph.coef_, index=X.columns, columns=['Coefficient']))
                except Exception as e:
                    st.write(f"Error fitting CoxPHSurvivalAnalysis: {e}")

                # Calculate risk scores
                try:
                    data['risk_score'] = cph.predict(X)
                except Exception as e:
                    st.write(f"Error calculating risk scores: {e}")

                # Plot risk scores
                try:
                    plt.figure(figsize=(10, 6))
                    for pipeline_type in pipeline_types:
                        subset = data[data[f'A_MAT_{pipeline_type}'] == 1]
                        plt.scatter(subset['Duration'], subset['risk_score'], label=pipeline_type)

                    plt.title('Risk Scores by Time')
                    plt.xlabel('Time')
                    plt.ylabel('Risk Score')
                    plt.legend()
                    st.pyplot(plt)
                except KeyError as e:
                    st.write(f"KeyError: {e}")
        else:
            st.write('Please select at least one pipeline type.')
    else:
        st.write('Failed to load data. Please check the file path and format.')
else:
    st.write('Please enter a valid file path.')