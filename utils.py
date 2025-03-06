import pandas as pd

def load_and_process_data():
    """
    Load and preprocess the restaurant dataset
    """
    try:
        df = pd.read_csv("attached_assets/Dataset .csv")
        # Clean and process the data
        required_columns = ['Restaurant Name', 'Cuisines', 'Address', 'Aggregate rating', 'Average Cost for two', 'Currency']
        df = df[required_columns]
        df['Cuisines'] = df['Cuisines'].astype(str).str.lower()
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Dataset file not found. Please ensure 'Dataset .csv' exists in the current directory.")
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