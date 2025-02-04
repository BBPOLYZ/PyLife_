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

# Function to load data
@st.cache_data
def load_data(uploaded_file):
    try:
        return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
        
# Streamlit app

st.title('Failure Rate and Time-to-Failure Trends in Hong Kong')

# Sidebar for file uploader and user inputs
st.sidebar.header('Upload Data and Select Variables')
uploaded_files = st.sidebar.file_uploader("Choose Excel files", accept_multiple_files=True, type=["xlsx"])

if uploaded_files:
    dataframes = []
    for uploaded_file in uploaded_files:
        df = load_data(uploaded_file)
        if df is not None:
            dataframes.append((uploaded_file.name, df))
            st.sidebar.write(f"Uploaded file: {uploaded_file.name}")
            st.sidebar.dataframe(df.head())  # Display only the first few rows

    if dataframes:
        # Debug: Print file names and dataframe info
        for file_name, df in dataframes:
            st.write(f"File name: {file_name}")
            st.write(df.info())

        # User input for variable name
        selected_var = st.sidebar.text_input('Enter Categorical Variable for Analysis')

        if selected_var:
            st.header(f'Analysis for {selected_var}')
            comparison_type = st.radio("Select comparison type", ('Failure Rate', 'Time-to-Failure'), key="comparison_type")

            # Tabs for different sections
            tab1, tab2, tab3, tab4 = st.tabs(["Data Analysis", "Bar Plot", "Box Plot", "Heatmap"])

            with tab1:
                st.subheader('Data Analysis')
                for file_name, df in dataframes:
                    if selected_var in df.columns:
                        table_metrics = calculate_metrics(df, selected_var)
                        st.subheader(f'Data Analysis for {file_name}')
                        st.dataframe(table_metrics)

            with tab2:
                st.subheader('Bar Plot')
                if comparison_type == 'Failure Rate':
                    for file_name, df in dataframes:
                        if selected_var in df.columns:
                            table_metrics = calculate_metrics(df, selected_var)
                            st.write(f'Bar Plot for {file_name}')
                            fig, ax = plt.subplots(figsize=(8, 4))
                            if f'bursts/km_{selected_var}' in table_metrics.columns:
                                sns.barplot(x=table_metrics.index, y=f'bursts/km_{selected_var}', data=table_metrics, ax=ax, palette="viridis")
                                ax.set_ylabel('bursts/km')
                            elif f'leaks/km_{selected_var}' in table_metrics.columns:
                                sns.barplot(x=table_metrics.index, y=f'leaks/km_{selected_var}', data=table_metrics, ax=ax, palette="magma")
                                ax.set_ylabel('leaks/km')
                            ax.set_title(f'Bar Plot for {selected_var} in {file_name}')
                            ax.set_xlabel(selected_var)
                            st.pyplot(fig)

                    # Add a third chart for comparison of FW and SW
                    if len(dataframes) >= 2:
                        df1_name, df1 = dataframes[0]
                        df2_name, df2 = dataframes[1]
                        if selected_var in df1.columns and selected_var in df2.columns:
                            table_metrics1 = calculate_metrics(df1, selected_var)
                            table_metrics2 = calculate_metrics(df2, selected_var)
                            combined_metrics = pd.concat([table_metrics1.assign(Dataset='FW'), table_metrics2.assign(Dataset='SW')])

                            st.write('Comparison of FW and SW')
                            fig, ax = plt.subplots(figsize=(10, 6))
                            if f'bursts/km_{selected_var}' in combined_metrics.columns:
                                sns.barplot(x=combined_metrics.index, y=f'bursts/km_{selected_var}', hue='Dataset', data=combined_metrics, ax=ax, palette="viridis")
                                ax.set_ylabel('bursts/km')
                            elif f'leaks/km_{selected_var}' in combined_metrics.columns:
                                sns.barplot(x=combined_metrics.index, y=f'leaks/km_{selected_var}', hue='Dataset', data=combined_metrics, ax=ax, palette="magma")
                                ax.set_ylabel('leaks/km')
                            ax.set_title(f'Comparison of FW and SW for {selected_var}')
                            ax.set_xlabel(selected_var)
                            st.pyplot(fig)
                else:
                    combined_df = pd.concat([df.assign(Dataset=file_name) for file_name, df in dataframes])
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(x='Failure Year', y='LENGTH', hue='Dataset', data=combined_df, ax=ax, palette="viridis")
                    ax.set_title(f'Comparative Bar Plot for {selected_var}')
                    ax.set_xlabel('Failure Year')
                    ax.set_ylabel('LENGTH')
                    st.pyplot(fig)

            with tab3:
                st.subheader('Box Plot')
                for file_name, df in dataframes:
                    if selected_var in df.columns:
                        fig, ax = plt.subplots(figsize=(8, 4))
                        sns.boxplot(data=df, x=selected_var, y='LENGTH', hue='FAULT_TYPE', ax=ax)
                        ax.set_title(f'Box Plot for {selected_var} in {file_name}')
                        ax.set_xlabel(selected_var)
                        ax.set_ylabel('Length')
                        st.pyplot(fig)

            with tab4:
                st.subheader('Heatmap')
                for file_name, df in dataframes:
                    if selected_var in df.columns:
                        failure_counts = df.pivot_table(values='LENGTH', index='Failure Year', columns=selected_var, aggfunc='count').fillna(0)
                        total_lengths = df.groupby(selected_var)['LENGTH'].sum()
                        heatmap_data = failure_counts.div(total_lengths, axis=1) * 100  # Scaling factor

                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', ax=ax)
                        cbar = ax.collections[0].colorbar
                        cbar.set_label('Failures per km (x10^-2)')
                        cbar.ax.yaxis.set_major_formatter(ScalarFormatter())
                        cbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                        cbar.ax.yaxis.get_offset_text().set_position((-0.1, 0))
                        cbar.ax.yaxis.get_offset_text().set_fontsize(10)
                        ax.set_title(f'Heatmap for {selected_var} in {file_name} by Year')
                        st.pyplot(fig)
                    else:
                        st.error(f"Selected variable '{selected_var}' not found in one of the datasets")
        else:
            st.error(f"No numeric data available for the selected variable '{selected_var}' in {file_name}.")
    else:
        st.error(f"The variable '{selected_var}' is not found in the uploaded file.")
else:
    st.error("Failed to load the file. Please check the file format and try again.")