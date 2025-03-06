import streamlit as st
import pandas as pd
from utils import load_and_process_data, filter_restaurants
from styles import apply_custom_styles

# Page configuration
st.set_page_config(
    page_title="Restaurant Finder",
    page_icon="🍽️",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

# Banner SVG
banner_svg = """
<svg width="100%" height="120" viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="120" fill="#FF4B4B"/>
    <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" 
          fill="white" style="font-size: 48px; font-family: sans-serif;">
        Restaurant Finder
    </text>
</svg>
"""
st.markdown(banner_svg, unsafe_allow_html=True)

# Load and process data
df = load_and_process_data()

# Sidebar for search history
with st.sidebar:
    st.header("Search History")
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    for hist in st.session_state.search_history[-5:]:
        st.text(f"🔍 {hist}")

# Main content
st.subheader("Find Restaurants by Cuisine")

# Get unique cuisines for autocomplete
all_cuisines = set()
for cuisines in df['Cuisines'].str.split(','):
    if isinstance(cuisines, list):
        all_cuisines.update([c.strip() for c in cuisines])
all_cuisines = sorted(list(all_cuisines))

# Search interface
col1, col2 = st.columns([3, 1])
with col1:
    cuisine_type = st.selectbox(
        "Select cuisine type",
        options=all_cuisines,
        index=None,
        placeholder="Choose a cuisine..."
    )
with col2:
    search_button = st.button("Search", type="primary")

if cuisine_type and search_button:
    # Add to search history
    if cuisine_type not in st.session_state.search_history:
        st.session_state.search_history.append(cuisine_type)
    
    # Show loading spinner
    with st.spinner('Searching restaurants...'):
        results = filter_restaurants(df, cuisine_type)
        
        if isinstance(results, str):
            st.warning(results)
        else:
            st.success(f"Found {len(results)} restaurants serving {cuisine_type} cuisine")
            
            # Display results in a clean table
            st.dataframe(
                results,
                column_config={
                    "Restaurant Name": st.column_config.TextColumn("Restaurant Name", width="medium"),
                    "Cuisines": st.column_config.TextColumn("Cuisines", width="large"),
                    "Address": st.column_config.TextColumn("Address", width="large")
                },
                hide_index=True,
            )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ for food lovers</p>
    </div>
    """,
    unsafe_allow_html=True
)
