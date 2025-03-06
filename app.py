import streamlit as st
import pandas as pd
from utils import load_and_process_data, filter_restaurants, get_restaurant_recommendations
from styles import apply_custom_styles

# Page configuration
st.set_page_config(
    page_title="Restaurant Finder",
    page_icon="🍽️",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

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
st.title("Restaurant Finder & Recommender")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Search by Cuisine", "Get Personalized Recommendations"])

with tab1:
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
                        "Address": st.column_config.TextColumn("Address", width="large"),
                        "Cost": st.column_config.TextColumn("Average Cost", width="small"),
                        "Rating": st.column_config.TextColumn("Rating", width="small")
                    },
                    hide_index=True,
                )

with tab2:
    st.subheader("Get Personalized Restaurant Recommendations")

    # User preferences form
    with st.form("preferences_form"):
        # Multiple cuisine selection
        preferred_cuisines = st.multiselect(
            "Select your preferred cuisines",
            options=all_cuisines,
            help="Choose one or more cuisines you enjoy"
        )

        # Budget preference
        col1, col2 = st.columns(2)
        with col1:
            max_budget = st.number_input(
                "Maximum budget per person",
                min_value=10,
                value=100,
                help="Enter your maximum budget per person"
            )

        with col2:
            min_rating = st.slider(
                "Minimum rating",
                min_value=0.0,
                max_value=5.0,
                value=3.5,
                step=0.5,
                help="Select minimum acceptable rating"
            )

        # Submit button
        submitted = st.form_submit_button("Get Recommendations", type="primary")

    if submitted and preferred_cuisines:
        # Create preferences dictionary
        preferences = {
            'preferred_cuisines': preferred_cuisines,
            'max_budget': max_budget,
            'min_rating': min_rating
        }

        # Show loading spinner
        with st.spinner('Finding the best restaurants for you...'):
            recommendations = get_restaurant_recommendations(df, preferences)

            st.success("Here are your personalized restaurant recommendations!")

            # Display recommendations
            st.dataframe(
                recommendations,
                column_config={
                    "Restaurant Name": st.column_config.TextColumn("Restaurant Name", width="medium"),
                    "Cuisines": st.column_config.TextColumn("Cuisines", width="large"),
                    "Address": st.column_config.TextColumn("Address", width="large"),
                    "Cost": st.column_config.TextColumn("Average Cost", width="small"),
                    "Rating": st.column_config.TextColumn("Rating", width="small")
                },
                hide_index=True,
            )
    elif submitted:
        st.warning("Please select at least one preferred cuisine type.")

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