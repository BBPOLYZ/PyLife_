import pandas as pd
import streamlit as st
import os

# Header
st.header("Prepare the Data")

# Specify the directory where the CSV files will be saved
output_directory = "output_csv_files"
os.makedirs(output_directory, exist_ok=True)

# Function to load CSV data in chunks using pandas
def load_csv_pandas(uploaded_file):
    try:
        # Read CSV in chunks
        chunks = pd.read_csv(uploaded_file, chunksize=10000)
        df = pd.concat(chunks, ignore_index=True)
        return df
    except Exception as e:
        st.error(f"Error loading {uploaded_file.name}: {e}")
        return None

# Sidebar - Upload CSV
with st.sidebar.header('1. Upload your CSV files for Analysis'):
    uploaded_files = st.sidebar.file_uploader("Upload your input CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    # Load all uploaded files using pandas
    pandas_dfs = [load_csv_pandas(file) for file in uploaded_files if file is not None]
    pandas_dfs = [df for df in pandas_dfs if df is not None]  # Filter out any None values
    
    if pandas_dfs:
        st.sidebar.success("Files uploaded successfully!")
        st.write("Files loaded successfully!")
        
        st.header('2. Select Columns for Concatenation')
        
        # Get common columns from all dataframes
        common_columns = list(set.intersection(*(set(df.columns) for df in pandas_dfs)))
        
        # Multi-select step for selecting columns
        concat_columns = st.multiselect('Select columns to concatenate on:', common_columns, default=common_columns)
        
        if concat_columns:
            st.write("Columns selected for concatenation:", concat_columns)
            
            # Concatenate dataframes on selected columns using pandas
            concatenated_df = pd.concat([df[concat_columns] for df in pandas_dfs], axis=0, ignore_index=True)
            
            # Provide a summary of the concatenated dataframe
            st.write(f"Shape of concatenated dataframe: {concatenated_df.shape}")
            st.dataframe(concatenated_df.head())
            
            # Use st.data_editor to explore the concatenated dataframe
            st.header('3. Explore and Edit Data')
            edited_df = st.data_editor(concatenated_df, num_rows="dynamic")
            
            # Display the edited dataframe
            st.write("Edited Dataframe:")
            st.dataframe(edited_df)
            
            # Button to save the edited dataframe to a CSV file
            if st.button('Save Edited CSV'):
                output_file_path = os.path.join(output_directory, "edited_concatenated_data.csv")
                edited_df.to_csv(output_file_path, index=False)
                st.success(f"Edited data saved to {output_file_path}")
else:
    st.info('Awaiting CSV files to be uploaded.')
