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
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header styling */
        .stTitle {
            color: #FF4B4B !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            margin-bottom: 2rem !important;
            text-align: center !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Subheader styling */
        .stSubheader {
            color: #262730 !important;
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            margin: 1.5rem 0 !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 2px solid #FF4B4B;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            white-space: pre-wrap;
            background-color: white;
            border-radius: 5px;
            color: #FF4B4B;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #FFE5E5;
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF4B4B !important;
            color: white !important;
        }

        /* Button styling */
        .stButton > button {
            width: 100%;
            height: 3rem;
            background-color: #FF4B4B;
            color: white;
            font-weight: 600;
            border-radius: 5px;
            border: none;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .stButton > button:hover {
            background-color: #FF3131;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 5px;
            border: 1px solid #E0E0E0;
            padding: 0.5rem;
            transition: all 0.3s ease;
        }

        .stSelectbox > div > div:hover {
            border-color: #FF4B4B;
        }

        /* DataFrame styling */
        .dataframe {
            font-family: 'Inter', sans-serif !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            width: 100% !important;
            border-radius: 10px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }

        .dataframe th {
            background-color: #FF4B4B !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 1rem !important;
            text-align: left !important;
        }

        .dataframe td {
            padding: 1rem !important;
            border-top: 1px solid #E0E0E0 !important;
            background-color: white !important;
            transition: background-color 0.3s ease !important;
        }

        .dataframe tr:hover td {
            background-color: #FFF5F5 !important;
        }

        /* Form styling */
        .stForm {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Slider styling */
        .stSlider input {
            color: #FF4B4B !important;
        }

        /* Success message styling */
        .stSuccess {
            background-color: #D4EDDA;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            animation: fadeIn 0.5s ease;
        }

        /* Warning message styling */
        .stWarning {
            background-color: #FFF3CD;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            animation: fadeIn 0.5s ease;
        }

        /* Info message styling */
        .stInfo {
            background-color: #E7F5FF;
            color: #004085;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            border-left: 4px solid #004085;
        }

        /* Animation keyframes */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Sidebar styling */
        .css-1d391kg {
            padding: 2rem 1rem;
        }

        .css-1d391kg .stMarkdown {
            background-color: #FFF5F5;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 0.5rem;
        }

        /* Card-like containers */
        .stMarkdown {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .stMarkdown:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)