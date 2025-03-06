import streamlit as st
import pandas as pd
from utils import load_and_process_data, filter_restaurants, get_restaurant_recommendations
from styles import apply_custom_styles
from ml_utils import RestaurantRatingPredictor

# Page configuration
st.set_page_config(
    page_title="Restaurant Finder",
    page_icon="🍽️",
    layout="wide"
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
        st.header("Search History")
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []

        for hist in st.session_state.search_history[-5:]:
            st.text(f"🔍 {hist}")

    # Main content
    st.title("Restaurant Finder & Recommender")

    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs([
        "Search by Cuisine", 
        "Get Personalized Recommendations",
        "Predict Restaurant Rating"
    ])

    # Tab 1: Search by Cuisine
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
            if cuisine_type not in st.session_state.search_history:
                st.session_state.search_history.append(cuisine_type)

            with st.spinner('Searching restaurants...'):
                results = filter_restaurants(df, cuisine_type)

                if isinstance(results, str):
                    st.warning(results)
                else:
                    st.success(f"Found {len(results)} restaurants serving {cuisine_type} cuisine")
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
        st.subheader("Get Personalized Restaurant Recommendations")

        with st.form("preferences_form"):
            preferred_cuisines = st.multiselect(
                "Select your preferred cuisines",
                options=all_cuisines,
                help="Choose one or more cuisines you enjoy"
            )

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

            submitted = st.form_submit_button("Get Recommendations", type="primary")

        if submitted and preferred_cuisines:
            preferences = {
                'preferred_cuisines': preferred_cuisines,
                'max_budget': max_budget,
                'min_rating': min_rating
            }

            with st.spinner('Finding the best restaurants for you...'):
                recommendations = get_restaurant_recommendations(df, preferences)
                st.success("Here are your personalized restaurant recommendations!")
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

    # Tab 3: Rating Prediction
    with tab3:
        st.subheader("Predict Restaurant Rating")

        # Show model accuracy
        st.info(f"Model Accuracy: {st.session_state.model_accuracy:.2%}")

        # Input form for prediction
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)

            with col1:
                cuisines = st.text_input(
                    "Cuisines (comma-separated)",
                    help="Enter cuisines, e.g., 'Italian, Pizza'"
                )
                cost = st.number_input(
                    "Average cost for two",
                    min_value=10,
                    value=50
                )
                city = st.text_input("City")

            with col2:
                has_table = st.selectbox(
                    "Has table booking?",
                    options=["Yes", "No"]
                )
                has_online = st.selectbox(
                    "Has online delivery?",
                    options=["Yes", "No"]
                )

            predict_button = st.form_submit_button("Predict Rating", type="primary")

        if predict_button and cuisines and city:
            # Create a DataFrame for prediction
            pred_data = pd.DataFrame({
                'Cuisines': [cuisines],
                'City': [city],
                'Average Cost for two': [cost],
                'Has Table booking': [has_table],
                'Has Online delivery': [has_online]
            })

            with st.spinner('Predicting rating...'):
                predicted_rating = st.session_state.rating_predictor.predict(pred_data)[0]

                # Display prediction with confidence interval
                st.success(f"Predicted Rating: {'⭐' * int(round(predicted_rating))} ({predicted_rating:.1f})")

                # Show feature importance explanation
                st.write("Key factors affecting this prediction:")
                st.write("- Number of cuisines offered")
                st.write("- Average cost for two")
                st.write("- Location (city)")
                st.write("- Booking and delivery options")

        elif predict_button:
            st.warning("Please fill in all required fields (Cuisines and City).")

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

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please make sure all required data and dependencies are properly set up.")