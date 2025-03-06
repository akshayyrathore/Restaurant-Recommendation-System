# Restaurant Finder Application - Download Instructions

## Directory Structure
First, create the following directory structure:
```bash
restaurant-finder/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── banner.svg
├── attached_assets/
│   └── Dataset .csv
├── app.py
├── styles.py
└── utils.py
```

## File Contents

### 1. .streamlit/config.toml
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### 2. assets/banner.svg
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="120" viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect width="100%" height="120" fill="#FF4B4B"/>
    
    <!-- Restaurant icons -->
    <g transform="translate(50, 60)" fill="white" opacity="0.2">
        <!-- Fork -->
        <path d="M20,0 L20,60 M10,0 L10,30 Q10,40 20,40 M30,0 L30,30 Q30,40 20,40" 
              stroke="white" stroke-width="4" fill="none"/>
        
        <!-- Knife -->
        <path d="M60,0 Q80,20 80,40 L80,60 M60,0 L80,40" 
              stroke="white" stroke-width="4" fill="none"/>
    </g>
    
    <!-- Main Title -->
    <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" 
          fill="white" style="font-size: 48px; font-family: sans-serif; font-weight: bold;">
        Restaurant Finder
    </text>
    
    <!-- Decorative underline -->
    <path d="M300,70 L500,70" stroke="white" stroke-width="2" opacity="0.5"/>
    
    <!-- Small icon on the right -->
    <g transform="translate(650, 60)" fill="white" opacity="0.2">
        <!-- Plate -->
        <circle cx="0" cy="0" r="20" stroke="white" stroke-width="2" fill="none"/>
        <circle cx="0" cy="0" r="15" stroke="white" stroke-width="1" fill="none"/>
    </g>
</svg>
```

### 3. app.py
```python
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
                    "Address": st.column_config.TextColumn("Address", width="large"),
                    "Cost": st.column_config.TextColumn("Average Cost", width="small"),
                    "Rating": st.column_config.TextColumn("Rating", width="small")
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
```

### 4. styles.py
```python
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
```

### 5. utils.py
```python
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
```

### 6. requirements.txt
```
streamlit==1.43.0
pandas==2.2.3
```

## Setup Instructions

1. Create the directory structure:
```bash
mkdir -p restaurant-finder/.streamlit restaurant-finder/assets restaurant-finder/attached_assets
```

2. Copy all the files into their respective directories as shown in the structure above.

3. Copy your Dataset .csv file into the attached_assets directory.

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
streamlit run app.py
```

The application will be available at http://localhost:5000

Note: Make sure you have Python 3.7+ installed on your system.
