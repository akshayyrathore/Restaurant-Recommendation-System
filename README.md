# Restaurant Finder Application

A Streamlit-based restaurant search application with cuisine-based filtering and clean table display.

## Project Structure
```
.
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

## Setup Instructions

1. Create the directory structure:
```bash
mkdir -p .streamlit assets attached_assets
```

2. Install the required packages:
```bash
pip install streamlit pandas
```

3. Place the provided Dataset.csv file in the attached_assets/ directory

4. Run the application:
```bash
streamlit run app.py
```

## Features
- Search restaurants by cuisine type
- Display restaurant details including name, cuisines, address, cost, and rating
- Search history tracking
- Clean and responsive UI
- Star rating visualization
