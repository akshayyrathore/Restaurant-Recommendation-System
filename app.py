import streamlit as st
import pandas as pd
from utils import load_and_process_data, filter_restaurants, get_restaurant_recommendations
from styles import apply_custom_styles
from ml_utils import RestaurantRatingPredictor

# Page configuration
st.set_page_config(
    page_title="Restaurant Finder",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    # Apply custom styles
    apply_custom_styles()

    # Load and process data
    df = load_and_process_data()

    # Initialize ML model
    if 'rating_predictor' not in st.session_state:
        st.session_state.rating_predictor = RestaurantRatingPredictor()
        with st.spinner('Training rating prediction model...'):
            val_score = st.session_state.rating_predictor.fit(df)
            st.session_state.model_accuracy = val_score

    # Sidebar for search history
    with st.sidebar:
        st.image("assets/banner.svg", use_column_width=True)
        st.markdown("### 🕒 Recent Searches")
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []

        for hist in st.session_state.search_history[-5:]:
            st.markdown(f"🔍 `{hist}`")

        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.markdown(f"Total Restaurants: **{len(df)}**")
        st.markdown(f"Cuisines Available: **{len(set(df['Cuisines'].str.split(',').sum()))}**")
        st.markdown(f"Cities Covered: **{len(df['City'].unique())}**")

    # Main content
    st.title("🍽️ Restaurant Finder & Recommender")
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            Discover the perfect dining experience with our intelligent restaurant finder and recommendation system.
        </div>
    """, unsafe_allow_html=True)

    # Create tabs with icons
    tab1, tab2, tab3 = st.tabs([
        "🔍 Search by Cuisine", 
        "⭐ Get Recommendations",
        "🎯 Predict Rating"
    ])

    # Tab 1: Search by Cuisine
    with tab1:
        st.markdown("""
            <div style='background-color: #FFF5F5; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
                <h3 style='margin: 0; color: #FF4B4B;'>Find Your Favorite Cuisine</h3>
                <p style='margin: 0.5rem 0 0 0;'>Search through our extensive database of restaurants by cuisine type.</p>
            </div>
        """, unsafe_allow_html=True)

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
                "What cuisine are you craving today?",
                options=all_cuisines,
                index=None,
                placeholder="Choose a cuisine..."
            )
        with col2:
            search_button = st.button("Search Restaurants", type="primary")

        if cuisine_type and search_button:
            if cuisine_type not in st.session_state.search_history:
                st.session_state.search_history.append(cuisine_type)

            with st.spinner('🔍 Searching for the best restaurants...'):
                results = filter_restaurants(df, cuisine_type)

                if isinstance(results, str):
                    st.warning(results)
                else:
                    st.success(f"🎉 Found {len(results)} amazing restaurants serving {cuisine_type} cuisine!")
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

    # Tab 2: Personalized Recommendations
    with tab2:
        st.markdown("""
            <div style='background-color: #FFF5F5; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
                <h3 style='margin: 0; color: #FF4B4B;'>Personalized Restaurant Recommendations</h3>
                <p style='margin: 0.5rem 0 0 0;'>Tell us your preferences, and we'll find the perfect restaurants for you.</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("preferences_form"):
            st.markdown("### Your Preferences")

            preferred_cuisines = st.multiselect(
                "What cuisines do you enjoy?",
                options=all_cuisines,
                help="Choose one or more cuisines you love"
            )

            col1, col2 = st.columns(2)
            with col1:
                max_budget = st.number_input(
                    "What's your maximum budget per person?",
                    min_value=10,
                    value=100,
                    help="Enter your maximum budget"
                )

            with col2:
                min_rating = st.slider(
                    "Minimum rating you prefer",
                    min_value=0.0,
                    max_value=5.0,
                    value=3.5,
                    step=0.5,
                    help="Select minimum acceptable rating"
                )

            submitted = st.form_submit_button("Find My Restaurants", type="primary")

        if submitted and preferred_cuisines:
            preferences = {
                'preferred_cuisines': preferred_cuisines,
                'max_budget': max_budget,
                'min_rating': min_rating
            }

            with st.spinner('🔍 Finding your perfect restaurants...'):
                recommendations = get_restaurant_recommendations(df, preferences)
                st.success("✨ Here are your personalized restaurant recommendations!")
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
            st.warning("Please select at least one cuisine type to get recommendations.")

    # Tab 3: Rating Prediction
    with tab3:
        st.markdown("""
            <div style='background-color: #FFF5F5; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
                <h3 style='margin: 0; color: #FF4B4B;'>Restaurant Rating Predictor</h3>
                <p style='margin: 0.5rem 0 0 0;'>Use our AI model to predict a restaurant's rating based on its characteristics.</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"🎯 Model Accuracy: {st.session_state.model_accuracy:.2%}")

        with st.form("prediction_form"):
            st.markdown("### Restaurant Details")

            col1, col2 = st.columns(2)
            with col1:
                cuisines = st.text_input(
                    "What cuisines will be served?",
                    help="Enter cuisines, e.g., 'Italian, Pizza'"
                )
                cost = st.number_input(
                    "Average cost for two",
                    min_value=10,
                    value=50,
                    help="Enter the average cost for two people"
                )
                city = st.text_input(
                    "Which city is the restaurant in?",
                    help="Enter the city name"
                )

            with col2:
                has_table = st.selectbox(
                    "Will you offer table booking?",
                    options=["Yes", "No"],
                    help="Select if table booking will be available"
                )
                has_online = st.selectbox(
                    "Will you offer online delivery?",
                    options=["Yes", "No"],
                    help="Select if online delivery will be available"
                )

            predict_button = st.form_submit_button("Predict Rating", type="primary")

        if predict_button and cuisines and city:
            pred_data = pd.DataFrame({
                'Cuisines': [cuisines],
                'City': [city],
                'Average Cost for two': [cost],
                'Has Table booking': [has_table],
                'Has Online delivery': [has_online]
            })

            with st.spinner('🤔 Analyzing restaurant details...'):
                predicted_rating = st.session_state.rating_predictor.predict(pred_data)[0]

                st.markdown("""
                    <div style='background-color: #D4EDDA; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                        <h3 style='margin: 0; color: #155724;'>Predicted Rating</h3>
                        <div style='font-size: 2rem; margin: 0.5rem 0;'>
                """, unsafe_allow_html=True)
                st.success(f"{'⭐' * int(round(predicted_rating))} ({predicted_rating:.1f})")

                st.markdown("""
                    <div style='background-color: #E7F5FF; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                        <h4 style='margin: 0; color: #004085;'>Key Factors in This Prediction</h4>
                        <ul style='margin: 0.5rem 0 0 0;'>
                            <li>Number and types of cuisines offered</li>
                            <li>Price point (average cost for two)</li>
                            <li>Location and market characteristics</li>
                            <li>Available services (booking and delivery)</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

        elif predict_button:
            st.warning("Please fill in all required fields (Cuisines and City).")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <p>Made with ❤️ for food lovers everywhere</p>
            <p style='font-size: 0.8rem; color: #666;'>Using advanced AI and data analysis to help you find the perfect dining experience</p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please make sure all required data and dependencies are properly set up.")