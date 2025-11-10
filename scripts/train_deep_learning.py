"""
Deep Learning Training Script for Phishing Detection
CSE_proj_12 - Neural Network Implementation
Team: Amandeep 
"""

import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
import pickle
import os
from datetime import datetime

# Check if TensorFlow is available
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.regularizers import l2
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("⚠️  TensorFlow not installed. Install with: pip install tensorflow")

def build_neural_network(input_dim=111):
    """
    Build Neural Network Architecture
    - Input: 111 features
    - Hidden Layer 1: 256 neurons + ReLU + BatchNorm + Dropout(0.3)
    - Hidden Layer 2: 128 neurons + ReLU + BatchNorm + Dropout(0.3)
    - Hidden Layer 3: 64 neurons + ReLU + BatchNorm + Dropout(0.2)
    - Output: 1 neuron + Sigmoid
    """
    
    print("\n🏗️  BUILDING NEURAL NETWORK")
    print("="*70)
    
    model = models.Sequential(name="PhishingDetector_DL")
    
    # Input layer
    model.add(layers.Input(shape=(input_dim,), name='input'))
    
    # Hidden Layer 1: 256 neurons
    model.add(layers.Dense(256, activation='relu', 
                          kernel_regularizer=l2(0.001), name='dense_1'))
    model.add(layers.BatchNormalization(name='batch_norm_1'))
    model.add(layers.Dropout(0.3, name='dropout_1'))
    
    # Hidden Layer 2: 128 neurons
    model.add(layers.Dense(128, activation='relu',
                          kernel_regularizer=l2(0.001), name='dense_2'))
    model.add(layers.BatchNormalization(name='batch_norm_2'))
    model.add(layers.Dropout(0.3, name='dropout_2'))
    
    # Hidden Layer 3: 64 neurons
    model.add(layers.Dense(64, activation='relu',
                          kernel_regularizer=l2(0.001), name='dense_3'))
    model.add(layers.BatchNormalization(name='batch_norm_3'))
    model.add(layers.Dropout(0.2, name='dropout_3'))
    
    # Output layer
    model.add(layers.Dense(1, activation='sigmoid', name='output'))
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
            keras.metrics.AUC(name='auc')
        ]
    )
    
    print("\n📋 Model Architecture:")
    model.summary()
    
    total_params = model.count_params()
    print(f"\n📊 Total Parameters: {total_params:,}")
    
    return model

def train_deep_learning_model():
    """Train Neural Network on phishing_domain.csv"""
    
    if not TF_AVAILABLE:
        print("\n❌ Cannot proceed without TensorFlow")
        print("Install with: pip install tensorflow scikit-learn")
        return
    
    print("="*70)
    print("🧠 DEEP LEARNING TRAINING - CSE_proj_12")
    print("="*70)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Step 1: Load dataset
    print("\n[1/7] 📊 Loading dataset...")
    try:
        df = pd.read_csv('phishing_domain.csv')
        print(f"   ✓ Dataset loaded: {df.shape}")
        print(f"   ✓ Features: {df.shape[1] - 1}")
        print(f"   ✓ Samples: {df.shape[0]:,}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Step 2: Prepare data
    print("\n[2/7] 🔧 Preparing data...")
    X = df.drop('phishing', axis=1).values
    y = df['phishing'].values
    
    print(f"   ✓ Features shape: {X.shape}")
    print(f"   ✓ Target distribution:")
    print(f"      Legitimate (0): {(y == 0).sum():,}")
    print(f"      Phishing (1): {(y == 1).sum():,}")
    
    # Handle missing values
    if np.isnan(X).any():
        print(f"   ⚠️  Handling missing values...")
        X = np.nan_to_num(X, 0)
    
    # Step 3: Split data (train/val/test)
    print("\n[3/7] ✂️  Splitting data...")
    
    # First split: 80% train+val, 20% test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Second split: 80% train, 20% val (of the temp set)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.2, random_state=42, stratify=y_temp
    )
    
    print(f"   ✓ Training: {len(X_train):,} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"   ✓ Validation: {len(X_val):,} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"   ✓ Test: {len(X_test):,} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # Step 4: Scale features
    print("\n[4/7] ⚖️  Scaling features...")
    scaler = StandardScaler()
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"   ✓ Train - Mean: {X_train_scaled.mean():.4f}, Std: {X_train_scaled.std():.4f}")
    print(f"   ✓ Feature range: [{X_train_scaled.min():.2f}, {X_train_scaled.max():.2f}]")
    
    # Save scaler
    os.makedirs('models', exist_ok=True)
    with open('models/scaler_dl.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print(f"   ✓ Scaler saved: models/scaler_dl.pkl")
    
    # Step 5: Build model
    print("\n[5/7] 🏗️  Building model...")
    model = build_neural_network(input_dim=X_train_scaled.shape[1])
    
    # Step 6: Train model with EPOCHS
    print("\n[6/7] 🎯 TRAINING WITH EPOCHS")
    print("="*70)
    
    epochs = 100
    batch_size = 64
    
    print(f"Epochs: {epochs}")
    print(f"Batch Size: {batch_size}")
    print(f"Training Samples: {len(X_train):,}")
    print(f"Validation Samples: {len(X_val):,}")
    print("="*70 + "\n")
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            'models/best_model_dl.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train
    history = model.fit(
        X_train_scaled, y_train,
        validation_data=(X_val_scaled, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE")
    print("="*70)
    
    # Step 7: Evaluate
    print("\n[7/7] 📈 MODEL EVALUATION")
    print("="*70)
    
    # Predictions
    y_pred_proba = model.predict(X_test_scaled, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("\n📊 PERFORMANCE METRICS")
    print("="*70)
    print(f"✓ Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"✓ Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"✓ Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"✓ F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    print(f"✓ ROC-AUC:   {roc_auc:.4f}")
    
    print(f"\n📋 Confusion Matrix:")
    print(f"   True Negatives:  {tn:,}")
    print(f"   False Positives: {fp:,} ({fp/(tn+fp)*100:.2f}%)")
    print(f"   False Negatives: {fn:,} ({fn/(fn+tp)*100:.2f}%)")
    print(f"   True Positives:  {tp:,}")
    
    print(f"\n📝 Classification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Legitimate', 'Phishing'],
        digits=4
    ))
    
    # Training history
    print(f"\n📉 Training History:")
    print(f"   Total epochs: {len(history.history['loss'])}")
    print(f"   Best val_accuracy: {max(history.history['val_accuracy']):.4f}")
    print(f"   Final train_accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"   Final val_accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    # Save model
    print("\n💾 Saving model...")
    model.save('models/phishing_model_dl.h5')
    print("   ✓ Model saved: models/phishing_model_dl.h5")
    
    # Save training info
    training_info = {
        'timestamp': datetime.now().isoformat(),
        'epochs': len(history.history['loss']),
        'batch_size': batch_size,
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'roc_auc': float(roc_auc),
        'model_parameters': model.count_params()
    }
    
    with open('models/training_info_dl.txt', 'w') as f:
        for key, value in training_info.items():
            f.write(f"{key}: {value}\n")
    
    print("   ✓ Training info saved: models/training_info_dl.txt")
    
    print("\n" + "="*70)
    print("✅ DEEP LEARNING TRAINING COMPLETE!")
    print("="*70)
    print(f"\n🎯 Final Results:")
    print(f"   Accuracy: {accuracy*100:.2f}%")
    print(f"   Model: models/phishing_model_dl.h5")
    print(f"   Scaler: models/scaler_dl.pkl")
    print("\n🚀 Next steps:")
    print("   1. Test model: python scripts/test_dl_model.py")
    print("   2. Deploy API with DL model")
    print("="*70)

if __name__ == '__main__':
    train_deep_learning_model()
