import pandas as pd
import numpy as np

def load_and_process_data():
    """
    Load and preprocess the restaurant dataset
    """
    try:
        df = pd.read_csv("attached_assets/Dataset .csv")

        # Define required columns
        required_columns = [
            'Restaurant Name', 'Cuisines', 'Address', 'City',
            'Aggregate rating', 'Average Cost for two', 'Currency',
            'Has Table booking', 'Has Online delivery'
        ]

        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Select and clean data
        df = df[required_columns]
        df['Cuisines'] = df['Cuisines'].astype(str).str.lower()

        return df
    except FileNotFoundError:
        raise FileNotFoundError("Dataset file not found. Please ensure 'Dataset .csv' exists in the attached_assets directory.")
    except Exception as e:
        raise Exception(f"Error processing data: {str(e)}")

def filter_restaurants(df, cuisine_type):
    """
    Filter restaurants based on cuisine type
    """
    cuisine_type = cuisine_type.lower()
    filtered_df = df[df["Cuisines"].str.contains(cuisine_type, case=False, na=False)]

    if filtered_df.empty:
        return f"No restaurants found serving {cuisine_type} cuisine."

    # Format the display data
    display_df = filtered_df.copy()
    display_df['Cost'] = display_df.apply(
        lambda x: f"{x['Currency']} {x['Average Cost for two']:.2f}", axis=1
    )
    display_df['Rating'] = display_df['Aggregate rating'].apply(
        lambda x: f"{'⭐' * int(round(x))}" if pd.notnull(x) else "Not rated"
    )

    # Select and rename columns for display
    return display_df[["Restaurant Name", "Cuisines", "Address", "Cost", "Rating"]]

def get_restaurant_recommendations(df, preferences):
    """
    Get restaurant recommendations based on user preferences
    """
    try:
        # Create a scoring system
        scored_df = df.copy()
        scored_df['score'] = 0.0

        # Score based on cuisine preferences (30% weight)
        for cuisine in preferences['preferred_cuisines']:
            cuisine = cuisine.lower()
            scored_df['score'] += scored_df['Cuisines'].str.contains(cuisine, case=False, na=False) * 30

        # Score based on rating (40% weight)
        min_rating = preferences.get('min_rating', 0)
        scored_df['score'] += (scored_df['Aggregate rating'] - min_rating) * 8

        # Score based on budget (30% weight)
        max_budget = preferences.get('max_budget', float('inf'))
        budget_score = 30 * (1 - scored_df['Average Cost for two'] / (max_budget * 2))
        scored_df['score'] += budget_score.clip(lower=0)

        # Sort by score and get top recommendations
        recommendations = scored_df.nlargest(10, 'score')

        # Format display data
        recommendations['Cost'] = recommendations.apply(
            lambda x: f"{x['Currency']} {x['Average Cost for two']:.2f}", axis=1
        )
        recommendations['Rating'] = recommendations['Aggregate rating'].apply(
            lambda x: f"{'⭐' * int(round(x))}" if pd.notnull(x) else "Not rated"
        )

        return recommendations[["Restaurant Name", "Cuisines", "Address", "Cost", "Rating"]]

    except Exception as e:
        raise Exception(f"Error generating recommendations: {str(e)}")