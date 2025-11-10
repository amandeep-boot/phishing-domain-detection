import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle
import os

def train_with_phishing_dataset():
    """Train model using the phishing_domain.csv dataset"""
    
    print("=" * 60)
    print("Phishing Detection - Training with Full Dataset")
    print("=" * 60)
    
    # Load dataset
    print("\n[1/6] Loading dataset...")
    try:
        df = pd.read_csv('phishing_domain.csv')
        print(f"✓ Dataset loaded successfully")
        print(f"  Shape: {df.shape}")
        print(f"  Features: {df.shape[1] - 1}")
        print(f"  Samples: {df.shape[0]}")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return
    
    # Check target distribution
    print("\n[2/6] Analyzing dataset...")
    print(f"  Target column: 'phishing'")
    print(f"  Class distribution:")
    print(df['phishing'].value_counts())
    print(f"\n  Legitimate (0): {(df['phishing'] == 0).sum()}")
    print(f"  Phishing (1): {(df['phishing'] == 1).sum()}")
    
    # Prepare features and target
    print("\n[3/6] Preparing data...")
    X = df.drop('phishing', axis=1)
    y = df['phishing']
    
    # Handle any missing values
    if X.isnull().sum().sum() > 0:
        print(f"  Handling {X.isnull().sum().sum()} missing values...")
        X = X.fillna(0)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    
    # Train model
    print("\n[4/6] Training Random Forest model...")
    print("  This may take several minutes...")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train, y_train)
    print("✓ Training completed!")
    
    # Evaluate
    print("\n[5/6] Evaluating model...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✓ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  True Negatives:  {cm[0][0]}")
    print(f"  False Positives: {cm[0][1]}")
    print(f"  False Negatives: {cm[1][0]}")
    print(f"  True Positives:  {cm[1][1]}")
    
    # Feature importance
    print("\n[6/6] Top 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")
    
    # Save model
    print("\nSaving model...")
    model_data = {
        'model': model,
        'feature_names': X.columns.tolist(),
        'accuracy': accuracy
    }
    
    with open('model_full.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("✓ Model saved to model_full.pkl")
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"\nModel Performance:")
    print(f"  Accuracy: {accuracy*100:.2f}%")
    print(f"  Features: {len(X.columns)}")
    print(f"  Training samples: {len(X_train)}")
    
    print("\nTo use this model, update your code to load 'model_full.pkl'")

if __name__ == '__main__':
    train_with_phishing_dataset()
