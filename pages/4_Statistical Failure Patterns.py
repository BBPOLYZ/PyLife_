import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter

st.set_page_config(page_title='Failure Rate and Time-to-Failure Trends in Hong Kong', layout='wide')

# Function to calculate metrics
@st.cache_data
def calculate_metrics(df, index_var):
    table_count = pd.pivot_table(df, values='LENGTH', index=[index_var, 'FAULT_TYPE'], aggfunc='count').unstack(fill_value=0)
    table_sum = pd.pivot_table(df, values='LENGTH', index=index_var, aggfunc='sum')
    table_sum[f'{index_var}_Km'] = table_sum['LENGTH'] / 1000
    table_combined = pd.concat([table_count, table_sum], axis=1)
    
    if ('LENGTH', 'BURST') in table_combined.columns:
        table_combined[f'bursts/km_{index_var}'] = table_combined[('LENGTH', 'BURST')] / table_combined[f'{index_var}_Km']
    if ('LENGTH', 'LEAK') in table_combined.columns:
        table_combined[f'leaks/km_{index_var}'] = table_combined[('LENGTH', 'LEAK')] / table_combined[f'{index_var}_Km']
    
    return table_combined

# Function to load data from file path
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
        
# Streamlit app

st.title('Failure Rate and Time-to-Failure Trends in Hong Kong')

# Sidebar for user inputs
st.sidebar.header('Select Variables')
file_path = st.sidebar.text_input('Enter the file path of your data:', 'BURSTS_SW_CT_1.xlsx')

if file_path:
    data = load_data(file_path)

    if data is not None:
        st.sidebar.write("Data Preview:")
        st.sidebar.dataframe(data.head())  # Display only the first few rows

        # User input for variable name
        selected_var = st.sidebar.text_input('Enter Categorical Variable for Analysis')

        if selected_var:
            st.header(f'Analysis for {selected_var}')
            comparison_type = st.radio("Select comparison type", ('Failure Rate', 'Time-to-Failure'), key="comparison_type")

            # Tabs for different sections
            tab1, tab2, tab3, tab4 = st.tabs(["Data Analysis", "Bar Plot", "Box Plot", "Heatmap"])

            with tab1:
                st.subheader('Data Analysis')
                if selected_var in data.columns:
                    table_metrics = calculate_metrics(data, selected_var)
                    st.dataframe(table_metrics)

            with tab2:
                st.subheader('Bar Plot')
                if comparison_type == 'Failure Rate':
                    if selected_var in data.columns:
                        table_metrics = calculate_metrics(data, selected_var)
                        fig, ax = plt.subplots(figsize=(8, 4))
                        if f'bursts/km_{selected_var}' in table_metrics.columns:
                            sns.barplot(x=table_metrics.index, y=f'bursts/km_{selected_var}', data=table_metrics, ax=ax, palette="viridis")
                            ax.set_ylabel('bursts/km')
                        elif f'leaks/km_{selected_var}' in table_metrics.columns:
                            sns.barplot(x=table_metrics.index, y=f'leaks/km_{selected_var}', data=table_metrics, ax=ax, palette="magma")
                            ax.set_ylabel('leaks/km')
                        ax.set_title(f'Bar Plot for {selected_var}')
                        ax.set_xlabel(selected_var)
                        st.pyplot(fig)
                else:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(x='Failure Year', y='LENGTH', data=data, ax=ax, palette="viridis")
                    ax.set_title(f'Comparative Bar Plot for {selected_var}')
                    ax.set_xlabel('Failure Year')
                    ax.set_ylabel('LENGTH')
                    st.pyplot(fig)

            with tab3:
                st.subheader('Box Plot')
                if selected_var in data.columns:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.boxplot(data=data, x=selected_var, y='LENGTH', hue='FAULT_TYPE', ax=ax)
                    ax.set_title(f'Box Plot for {selected_var}')
                    ax.set_xlabel(selected_var)
                    ax.set_ylabel('Length')
                    st.pyplot(fig)

            with tab4:
                st.subheader('Heatmap')
                if selected_var in data.columns:
                    failure_counts = data.pivot_table(values='LENGTH', index='Failure Year', columns=selected_var, aggfunc='count').fillna(0)
                    total_lengths = data.groupby(selected_var)['LENGTH'].sum()
                    heatmap_data = failure_counts.div(total_lengths, axis=1) * 100  # Scaling factor

                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', ax=ax)
                    cbar = ax.collections[0].colorbar
                    cbar.set_label('Failures per km (x10^-2)')
                    cbar.ax.yaxis.set_major_formatter(ScalarFormatter())
                    cbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                    cbar.ax.yaxis.get_offset_text().set_position((-0.1, 0))
                    cbar.ax.yaxis.get_offset_text().set_fontsize(10)
                    ax.set_title(f'Heatmap for {selected_var} by Year')
                    st.pyplot(fig)
                else:
                    st.error(f"Selected variable '{selected_var}' not found in the dataset")
        else:
            st.error(f"No numeric data available for the selected variable '{selected_var}'.")
    else:
        st.error(f"The variable '{selected_var}' is not found in the uploaded file.")
else:
    st.error("Failed to load the file. Please check the file format and try again.")
