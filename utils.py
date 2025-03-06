import pandas as pd

def load_and_process_data():
    """
    Load and preprocess the restaurant dataset
    """
    try:
        df = pd.read_csv("Dataset .csv")
        # Ensure Cuisines column exists and clean it
        if 'Cuisines' not in df.columns:
            raise ValueError("Required 'Cuisines' column not found in dataset")
        
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
    
    # Select and return relevant columns
    return filtered_df[["Restaurant Name", "Cuisines", "Address"]]
