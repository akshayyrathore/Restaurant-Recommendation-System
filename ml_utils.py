import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from category_encoders import TargetEncoder

class RestaurantRatingPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.cuisine_encoder = TargetEncoder(random_state=42)
        self.location_encoder = TargetEncoder(random_state=42)
        self.is_trained = False

    def preprocess_data(self, df):
        """
        Preprocess the data for training or prediction
        """
        # Create features DataFrame
        features_df = df.copy()
        
        # Extract features
        features_df['Cuisines_Count'] = features_df['Cuisines'].str.count(',') + 1
        features_df['Has_Table_booking'] = features_df['Has Table booking'].map({'Yes': 1, 'No': 0})
        features_df['Has_Online_delivery'] = features_df['Has Online delivery'].map({'Yes': 1, 'No': 0})
        
        # Extract primary cuisine (first one listed)
        features_df['Primary_Cuisine'] = features_df['Cuisines'].str.split(',').str[0]
        
        # Extract city from address
        features_df['City'] = features_df['City']
        
        # Select features for model
        feature_columns = [
            'Average Cost for two',
            'Cuisines_Count',
            'Has_Table_booking',
            'Has_Online_delivery',
            'Primary_Cuisine',
            'City'
        ]
        
        X = features_df[feature_columns].copy()
        
        if 'Aggregate rating' in df.columns:
            y = df['Aggregate rating']
        else:
            y = None
            
        return X, y

    def fit(self, df):
        """
        Train the model on the provided data
        """
        # Preprocess data
        X, y = self.preprocess_data(df)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Encode categorical variables
        X_train_encoded = X_train.copy()
        X_val_encoded = X_val.copy()
        
        # Encode cuisine and city
        X_train_encoded['Primary_Cuisine'] = self.cuisine_encoder.fit_transform(
            X_train['Primary_Cuisine'], y_train
        )
        X_train_encoded['City'] = self.location_encoder.fit_transform(
            X_train['City'], y_train
        )
        
        X_val_encoded['Primary_Cuisine'] = self.cuisine_encoder.transform(X_val['Primary_Cuisine'])
        X_val_encoded['City'] = self.location_encoder.transform(X_val['City'])
        
        # Scale numerical features
        numerical_features = [
            'Average Cost for two',
            'Cuisines_Count',
            'Has_Table_booking',
            'Has_Online_delivery'
        ]
        
        X_train_encoded[numerical_features] = self.scaler.fit_transform(
            X_train_encoded[numerical_features]
        )
        X_val_encoded[numerical_features] = self.scaler.transform(
            X_val_encoded[numerical_features]
        )
        
        # Train model
        self.model.fit(X_train_encoded, y_train)
        self.is_trained = True
        
        # Return validation score
        val_score = self.model.score(X_val_encoded, y_val)
        return val_score

    def predict(self, df):
        """
        Make predictions for new restaurants
        """
        if not self.is_trained:
            raise ValueError("Model needs to be trained before making predictions")
            
        # Preprocess data
        X, _ = self.preprocess_data(df)
        
        # Encode categorical variables
        X_encoded = X.copy()
        X_encoded['Primary_Cuisine'] = self.cuisine_encoder.transform(X['Primary_Cuisine'])
        X_encoded['City'] = self.location_encoder.transform(X['City'])
        
        # Scale numerical features
        numerical_features = [
            'Average Cost for two',
            'Cuisines_Count',
            'Has_Table_booking',
            'Has_Online_delivery'
        ]
        X_encoded[numerical_features] = self.scaler.transform(X_encoded[numerical_features])
        
        # Make predictions
        predictions = self.model.predict(X_encoded)
        return predictions
