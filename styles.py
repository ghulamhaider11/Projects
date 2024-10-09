import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        body {
            color: white !important;
            background-color: black;
        }
        .stApp {
            background-color: black;
        }
        .stMarkdown, .stText, .stCode {
            color: white !important;
        }
        /* Styling for dropdown lists and input boxes */
        .stSelectbox, .stMultiSelect, .stTextInput, .stNumberInput {
            color: white !important;
        }
        .stSelectbox > div > div, 
        .stMultiSelect > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div {
            background-color: #333 !important;
            color: white !important;
            border: 1px solid #555 !important;
        }
        /* Ensure text color is white for selected options */
        .stSelectbox > div > div > div[data-baseweb="select"] > div,
        .stMultiSelect > div > div > div[data-baseweb="select"] > div {
            color: white !important;
        }
        /* Style for the dropdown arrow */
        .stSelectbox > div > div > div[data-baseweb="select"] > div:last-child {
            color: white !important;
        }
        h1 {
            font-size: 50px;
            font-weight: 700;
            color: #4db8ff !important;
        }
        h3 {
            color: white !important;
        }
        .stButton > button {
            background-color: #004080;
            color: white !important;
            border-radius: 8px;
        }
        .custom-card {
            background-color: #004080;
            color: white !important;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
        }
        .element-container, .stDataFrame {
            color: white !important;
        }
        /* Ensure sidebar text is also white */
        .css-1d391kg, .css-1d391kg .stMarkdown {
            color: white !important;
        }
        /* Style for the file uploader */
        .stFileUploader > div > div {
            background-color: #333 !important;
            color: white !important;
        }
        /* Style for the sidebar */
        .css-1d391kg {
            background-color: #1a1a1a;
        }
        /* Style for the main content area */
        .css-1d391kg {
            background-color: black;
        }
        /* Style for the plots */
        .js-plotly-plot .plotly {
            background-color: #1a1a1a !important;
        }
        </style>
    """, unsafe_allow_html=True)