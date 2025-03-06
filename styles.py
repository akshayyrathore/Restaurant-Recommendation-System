import streamlit as st

def apply_custom_styles():
    """
    Apply custom CSS styles to the Streamlit app
    """
    st.markdown("""
        <style>
        /* Main content styling */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        .stTitle {
            color: #FF4B4B !important;
            font-weight: 700 !important;
        }
        
        /* Subheader styling */
        .stSubheader {
            color: #262730 !important;
            font-size: 1.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 5px;
            height: 3rem;
            background-color: #FF4B4B;
            color: white;
            font-weight: 600;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 5px;
        }
        
        /* DataFrame styling */
        .dataframe {
            font-family: sans-serif !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        /* Loading spinner styling */
        .stSpinner > div {
            border-top-color: #FF4B4B !important;
        }
        
        /* Success message styling */
        .stSuccess {
            background-color: #D4EDDA;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Warning message styling */
        .stWarning {
            background-color: #FFF3CD;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
