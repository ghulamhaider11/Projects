import streamlit as st
import pandas as pd
from io import BytesIO
from ydata_profiling import ProfileReport

from data_operations import data_operations,train_model
from visualization import visualization
from utils import load_data, display_preview_option
from styles import inject_custom_css
def main():
    # Set a wide layout and page title
    st.set_page_config(page_title='Data Exploration Tool', layout='wide')

    # Inject custom CSS
    inject_custom_css()

    # Title and description
    st.markdown("""
    <h1 style="text-align: center;">📊 DATA REFINERY </h1>
    <p style="text-align: center; font-size: 18px; color: white; background-color: #004080; padding: 10px; border-radius: 5px;">
    Welcome to Data Refinery Tool! This app helps you to perform Basic preprocessing & visualize data from CSV or Excel files.<br>
    </p>
    <hr style="border: 1px solid #004080;">
    """, unsafe_allow_html=True)

    # Sidebar Section - File Upload
    st.sidebar.title("📁 Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])

    df = None  # Initialize df to None

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            # Display Data Preview
            st.markdown("""
                <div class="custom-card">
                    <h2>Preview Raw Data</h2>
                </div>
            """, unsafe_allow_html=True)
            display_preview_option(df)
            if st.sidebar.checkbox("Enable Machine Learning"):
                target_column = st.selectbox("Select target column", df.columns)
                feature_columns = st.multiselect("Select feature columns", df.columns)
            if st.button("Train Model"):
              accuracy, report = train_model(df, target_column, feature_columns)
              st.write(f"Model Accuracy: {accuracy}")
              st.text(report)
    

            # Sidebar menu with buttons for sections
            st.sidebar.title("🛠️ Menu")
            if 'data_operations' not in st.session_state:
                st.session_state['data_operations'] = False
            if 'visualization' not in st.session_state:
                st.session_state['visualization'] = False

            if st.sidebar.button("🛠️ Data Operations"):
                st.session_state['data_operations'] = True
                st.session_state['visualization'] = False

            if st.sidebar.button("📊 Visualization"):
                st.session_state['data_operations'] = False
                st.session_state['visualization'] = True

            if st.session_state['data_operations']:
                df = data_operations(df)

            if st.session_state['visualization']:
                visualization(df)

            # Download updated DataFrame
            st.sidebar.subheader("Download Updated Data")
            file_format = st.sidebar.radio("Choose file format", ["CSV", "Excel"])
            
            if df is not None:  # Check if df is not None before trying to download
                if file_format == "CSV":
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.sidebar.download_button("Download Updated CSV", data=csv, file_name='updated_data.csv', mime='text/csv')
                else:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Sheet1')
                    excel_data = output.getvalue()
                    st.sidebar.download_button("Download Updated Excel", data=excel_data, file_name='updated_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                st.sidebar.warning("No data available for download. Please upload a file first.")
        else:
            st.error("Failed to load the data. Please check your file and try again.")
    else:
        st.info("Please upload a CSV or Excel file to get started.")

if __name__ == "__main__":
    main()