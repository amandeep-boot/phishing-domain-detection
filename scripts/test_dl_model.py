"""
Test Deep Learning Model
Quick inference test for the trained neural network
"""

import sys
sys.path.insert(0, '.')

import numpy as np
import pickle

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("❌ TensorFlow not installed")
    sys.exit(1)

def test_dl_model():
    """Test the trained deep learning model"""
    
    print("="*70)
    print("🧪 TESTING DEEP LEARNING MODEL")
    print("="*70)
    
    # Load model
    print("\n📦 Loading model...")
    try:
        model = tf.keras.models.load_model('models/phishing_model_dl.h5')
        print("   ✓ Model loaded: models/phishing_model_dl.h5")
    except Exception as e:
        print(f"   ✗ Error loading model: {e}")
        return
    
    # Load scaler
    try:
        with open('models/scaler_dl.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("   ✓ Scaler loaded: models/scaler_dl.pkl")
    except Exception as e:
        print(f"   ✗ Error loading scaler: {e}")
        return
    
    # Model info
    print(f"\n📊 Model Information:")
    print(f"   Input shape: {model.input_shape}")
    print(f"   Output shape: {model.output_shape}")
    print(f"   Total parameters: {model.count_params():,}")
    
    # Test with random features (111 features)
    print(f"\n🔮 Testing predictions...")
    
    # Create sample features
    test_samples = np.random.rand(5, 111)
    
    # Scale
    test_samples_scaled = scaler.transform(test_samples)
    
    # Predict
    predictions = model.predict(test_samples_scaled, verbose=0)
    
    print(f"\n✅ Predictions:")
    for i, pred in enumerate(predictions):
        prob = pred[0]
        label = "Phishing" if prob > 0.5 else "Legitimate"
        confidence = max(prob, 1-prob) * 100
        print(f"   Sample {i+1}: {label} (confidence: {confidence:.2f}%)")
    
    print("\n" + "="*70)
    print("✅ MODEL TEST COMPLETE")
    print("="*70)

if __name__ == '__main__':
    test_dl_model()
