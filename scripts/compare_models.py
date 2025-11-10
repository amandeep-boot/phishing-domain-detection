"""
Model Comparison: Random Forest vs Deep Learning
CSE_proj_12 - Performance Benchmarking
"""

import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import time
import pickle

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

def compare_models():
    """Compare Random Forest vs Neural Network"""
    
    print("="*70)
    print("⚖️  MODEL COMPARISON: Random Forest vs Neural Network")
    print("="*70)
    
    # Load dataset
    print("\n📊 Loading dataset...")
    df = pd.read_csv('phishing_domain.csv')
    X = df.drop('phishing', axis=1).values
    y = df['phishing'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Training samples: {len(X_train):,}")
    print(f"   Test samples: {len(X_test):,}")
    
    results = {}
    
    # ========== RANDOM FOREST ==========
    print("\n" + "="*70)
    print("🌲 RANDOM FOREST")
    print("="*70)
    
    print("\nTraining Random Forest...")
    start_time = time.time()
    
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    rf_train_time = time.time() - start_time
    
    # Predict
    start_time = time.time()
    rf_pred = rf_model.predict(X_test)
    rf_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    rf_inference_time = (time.time() - start_time) / len(X_test) * 1000  # ms per sample
    
    # Metrics
    results['Random Forest'] = {
        'accuracy': accuracy_score(y_test, rf_pred),
        'precision': precision_score(y_test, rf_pred),
        'recall': recall_score(y_test, rf_pred),
        'f1_score': f1_score(y_test, rf_pred),
        'roc_auc': roc_auc_score(y_test, rf_pred_proba),
        'train_time': rf_train_time,
        'inference_time': rf_inference_time
    }
    
    print(f"✓ Training time: {rf_train_time:.2f} seconds")
    print(f"✓ Accuracy: {results['Random Forest']['accuracy']:.4f}")
    print(f"✓ Inference: {rf_inference_time:.2f} ms/sample")
    
    # ========== NEURAL NETWORK ==========
    if TF_AVAILABLE:
        print("\n" + "="*70)
        print("🧠 NEURAL NETWORK")
        print("="*70)
        
        # Scale features
        print("\nScaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Build model
        print("Building neural network...")
        from tensorflow.keras import layers, models
        
        model = models.Sequential([
            layers.Input(shape=(X_train_scaled.shape[1],)),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.2),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Train
        print("Training neural network (50 epochs)...")
        start_time = time.time()
        
        history = model.fit(
            X_train_scaled, y_train,
            epochs=50,
            batch_size=64,
            validation_split=0.2,
            verbose=0,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
            ]
        )
        
        nn_train_time = time.time() - start_time
        
        # Predict
        start_time = time.time()
        nn_pred_proba = model.predict(X_test_scaled, verbose=0).flatten()
        nn_pred = (nn_pred_proba > 0.5).astype(int)
        nn_inference_time = (time.time() - start_time) / len(X_test) * 1000
        
        # Metrics
        results['Neural Network'] = {
            'accuracy': accuracy_score(y_test, nn_pred),
            'precision': precision_score(y_test, nn_pred),
            'recall': recall_score(y_test, nn_pred),
            'f1_score': f1_score(y_test, nn_pred),
            'roc_auc': roc_auc_score(y_test, nn_pred_proba),
            'train_time': nn_train_time,
            'inference_time': nn_inference_time,
            'epochs': len(history.history['loss'])
        }
        
        print(f"✓ Training time: {nn_train_time:.2f} seconds ({results['Neural Network']['epochs']} epochs)")
        print(f"✓ Accuracy: {results['Neural Network']['accuracy']:.4f}")
        print(f"✓ Inference: {nn_inference_time:.2f} ms/sample")
    
    # ========== COMPARISON TABLE ==========
    print("\n" + "="*70)
    print("📊 COMPARISON RESULTS")
    print("="*70)
    
    print(f"\n{'Metric':<20} {'Random Forest':<20} {'Neural Network':<20} {'Winner':<10}")
    print("-"*70)
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
    
    for metric in metrics:
        rf_val = results['Random Forest'][metric]
        
        if TF_AVAILABLE:
            nn_val = results['Neural Network'][metric]
            winner = 'NN ✓' if nn_val > rf_val else 'RF ✓' if rf_val > nn_val else 'Tie'
            print(f"{metric.upper():<20} {rf_val:.4f} ({rf_val*100:.2f}%){'':<3} {nn_val:.4f} ({nn_val*100:.2f}%){'':<3} {winner:<10}")
        else:
            print(f"{metric.upper():<20} {rf_val:.4f} ({rf_val*100:.2f}%)")
    
    print("\n" + "-"*70)
    print(f"{'Training Time':<20} {results['Random Forest']['train_time']:.2f}s{'':<14}", end='')
    
    if TF_AVAILABLE:
        nn_time = results['Neural Network']['train_time']
        winner = 'RF ✓' if results['Random Forest']['train_time'] < nn_time else 'NN ✓'
        print(f"{nn_time:.2f}s{'':<14} {winner:<10}")
    else:
        print()
    
    print(f"{'Inference Speed':<20} {results['Random Forest']['inference_time']:.2f}ms{'':<13}", end='')
    
    if TF_AVAILABLE:
        nn_inf = results['Neural Network']['inference_time']
        winner = 'RF ✓' if results['Random Forest']['inference_time'] < nn_inf else 'NN ✓'
        print(f"{nn_inf:.2f}ms{'':<13} {winner:<10}")
    else:
        print()
    
    # ========== RECOMMENDATIONS ==========
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)
    
    print("\n✅ Use Random Forest IF:")
    print("   • Quick prototyping (trains in ~2 minutes)")
    print("   • Need fast inference (<10ms)")
    print("   • Want interpretable model")
    print("   • Limited computational resources")
    
    if TF_AVAILABLE:
        print("\n✅ Use Neural Network IF:")
        print("   • Want maximum accuracy (96-98%)")
        print("   • Have GPU available")
        print("   • Showcase deep learning expertise")
        print("   • Plan to scale with more data")
        
        print("\n🎯 BEST APPROACH FOR CSE_proj_12:")
        print("   Primary: Random Forest (speed + reliability)")
        print("   Bonus: Neural Network (showcase DL knowledge)")
        print("   → This gives you both approaches for comparison!")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    compare_models()
