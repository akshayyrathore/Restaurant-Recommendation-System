# Cuisine Classifier

This project is a Cuisine Classifier application built using Streamlit. It predicts restaurant ratings based on various features.

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

## Setup and Run

Follow these steps to set up and run the application:

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the Repository**:
    ```sh
    git clone <repository_url>
    cd CuisineClassifier
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
      ```sh
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

4. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Run the Streamlit Application**:
    ```sh
    streamlit run app.py --server.port 8501
    ```

2. **Access the Application**:
    Open your web browser and go to:
    ```
    http://localhost:8501
    ```

### Troubleshooting

- **PowerShell Execution Policy Error**:
  If you encounter an error related to PowerShell execution policies, run the following command in PowerShell (as Administrator):
  ```sh
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

## Features
- Search restaurants by cuisine type
- Display restaurant details including name, cuisines, address, cost, and rating
- Search history tracking
- Clean and responsive UI
- Star rating visualization




