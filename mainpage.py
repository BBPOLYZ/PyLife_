import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="TTF")

# Define the glossary as a dictionary
glossary = {
    "Asset Management": {
        "Definition": "The systematic process of operating, maintaining, and upgrading physical assets cost-effectively.",
        "Relevance": "Ensures the longevity and reliability of water pipelines by planning maintenance and replacements."
    },
    "Failure Rate": {
        "Definition": "The frequency with which a pipeline fails over a specified period.",
        "Relevance": "A key metric in predicting time-to-failure and planning maintenance schedules."
    },
    "Failure Risk": {
        "Definition": "The probability of a pipeline failing within a specified period.",
        "Relevance": "Helps in assessing the likelihood of failure and prioritizing maintenance activities."
    },
    "Hazard Rate": {
        "Definition": "The rate at which failures occur over time, often used in reliability engineering.",
        "Relevance": "Provides insight into the failure dynamics of pipelines and helps in predicting future failures."
    },
    "Machine Learning": {
        "Definition": "A subset of artificial intelligence that uses algorithms to identify patterns and make predictions based on data.",
        "Relevance": "Enhances the accuracy of pipe failure predictions by analyzing large and complex datasets."
    },
    "Mean Time to Failure (MTTF)": {
        "Definition": "The average time expected until the first failure of a pipeline.",
        "Relevance": "A critical measure for understanding the reliability of pipelines and planning maintenance."
    },
    "Predictive Maintenance": {
        "Definition": "Maintenance performed based on the prediction of failures using data analysis and monitoring tools.",
        "Relevance": "Helps in reducing unexpected failures and optimizing maintenance schedules."
    },
    "Probabilistic Models": {
        "Definition": "Models that incorporate randomness and provide a range of possible outcomes with associated probabilities.",
        "Relevance": "Useful for predicting the likelihood and timing of pipe failures."
    },
    "Regression Analysis": {
        "Definition": "A statistical method for estimating the relationships among variables.",
        "Relevance": "Used to identify factors that influence pipe failures and predict future failures based on historical data."
    },
    "Survival Analysis": {
        "Definition": "A branch of statistics that deals with the analysis of time-to-event data.",
        "Relevance": "Used to estimate the time until a pipeline fails, considering various influencing factors."
    },
    "Time-to-Failure": {
        "Definition": "The expected duration before a pipeline fails.",
        "Relevance": "A critical measure for planning maintenance and replacement activities."
    },
    "Time-to-Next Failure": {
        "Definition": "The expected time until the next failure occurs after a previous failure.",
        "Relevance": "Important for scheduling maintenance and understanding the failure patterns of pipelines."
    }
}

# Display the menu
home_option = st.sidebar.radio("Knowledge Module", ["Introduction to the project", "Objectives", "Glossary", "Factors Influencing Time-to-Failure of Water Pipelines"])

if home_option == "Introduction to the project":
    st.title("Predicting Time-to-Failure of Water Pipelines")
    st.write("""
Hong Kong has around 8,300 km of potable and saltwater pipes, many over 30 years old and costly to maintain. In 2019, there were 7,113 pipe bursts/leaks, showing improvement in the Hong Kong Water Distribution Network (HKWDN) compared to 20 years ago. This web application predicts time-to-failure for water pipelines using statistical, machine learning, and integrated approaches. It helps monitor and improve pipeline performance, ensuring efficient and cost-effective maintenance. Key users include WSD, municipal workforces, academics, contractors, and other stakeholders. The research aims to advance municipal practices, enhance decision-making, increase pipeline safety and functionality, reduce water loss, and mitigate catastrophic failures.
    """)
    st.image("Picture4.png", caption="Water Pipeline Network")

elif home_option == "Objectives":
    st.title("Objectives")
    st.write("""
    Understanding Past Failure Patterns and Predicting Time-to-Failure of Water Pipelines
    1. Factors Influencing TTF 
    2. Exploratory Data Analysis
    3. Prediction of 1st, 2nd and 3rd Failure
    4. Prediction of Time-to-Next Failure
    """)
    # st.image("Picture3.jpeg", caption="Hong Kong Water Pipeline Burst")

elif home_option == "Glossary":
    st.title("Glossary")
    # Display glossary terms as a list
    for term, details in glossary.items():
        st.subheader(term)
        st.write(f"**Definition**: {details['Definition']}")
        st.write(f"**Relevance**: {details['Relevance']}")

elif home_option == "Factors Influencing Time-to-Failure of Water Pipelines":
    st.title("Factors Influencing Time-to-Failure of Water Pipelines")
    st.write("This section provides an explanation of the data used in the project...")
    st.image("Picture5.png", caption="Factors affecting Time-to-Failure of water pipelines")

# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f8f9fa;
    color: #495057;
    text-align: center;
    padding: 10px;
    box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.1);
}
</style>
<div class="footer">
    <p>© 2024 pyLIFE Water. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
