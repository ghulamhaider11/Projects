import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def display_preview_option(dataframe, num_rows=5):
    st.subheader("Dataset Preview (First 5 rows)")
    st.dataframe(dataframe.head(num_rows))
    st.write(f"Total rows: {len(dataframe)}, Total columns: {len(dataframe.columns)}")
    preview_option = st.radio("Select an option:", ("Hide Data Preview", "Show Data Preview"))
    if preview_option == "Show Data Preview":
        num_rows = st.number_input("Enter number of rows to preview", min_value=1, max_value=len(dataframe), value=5)
        st.dataframe(dataframe.head(num_rows))
    else:
        st.write("Data preview is hidden.")