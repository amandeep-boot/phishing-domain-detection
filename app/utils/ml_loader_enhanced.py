"""
Enhanced ML Model Loader
Supports both Random Forest and Deep Learning models
"""

import os
import pickle
from typing import Optional, Dict, Any

# Try to import TensorFlow
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    tf = None

class ModelLoader:
    """Load and manage ML models (RF and DL)"""
    
    def __init__(self):
        self.rf_model = None
        self.dl_model = None
        self.scaler = None
        self.active_model = None  # 'rf' or 'dl'
        
    def load_random_forest(self, model_path='model.pkl'):
        """Load Random Forest model"""
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                
                if isinstance(data, dict):
                    self.rf_model = data.get('model')
                else:
                    self.rf_model = data
                
                print(f"✓ Random Forest model loaded from {model_path}")
                if self.active_model is None:
                    self.active_model = 'rf'
                return True
            except Exception as e:
                print(f"✗ Error loading Random Forest: {e}")
                return False
        else:
            print(f"⚠ Random Forest model not found at {model_path}")
            return False
    
    def load_deep_learning(self, model_path='models/phishing_model_dl.h5', 
                          scaler_path='models/scaler_dl.pkl'):
        """Load Deep Learning model"""
        if not TF_AVAILABLE:
            print("⚠ TensorFlow not available. Cannot load DL model.")
            return False
        
        if os.path.exists(model_path):
            try:
                self.dl_model = tf.keras.models.load_model(model_path)
                print(f"✓ Deep Learning model loaded from {model_path}")
                
                # Load scaler
                if os.path.exists(scaler_path):
                    with open(scaler_path, 'rb') as f:
                        self.scaler = pickle.load(f)
                    print(f"✓ Scaler loaded from {scaler_path}")
                
                if self.active_model is None:
                    self.active_model = 'dl'
                return True
            except Exception as e:
                print(f"✗ Error loading Deep Learning model: {e}")
                return False
        else:
            print(f"⚠ Deep Learning model not found at {model_path}")
            return False
    
    def load_all_models(self):
        """Try to load all available models"""
        print("\n" + "="*60)
        print("🔧 Loading ML Models")
        print("="*60)
        
        rf_loaded = self.load_random_forest('model.pkl')
        dl_loaded = self.load_deep_learning()
        
        if not rf_loaded and not dl_loaded:
            print("\n⚠ No models loaded!")
            print("Train a model first:")
            print("  Random Forest: python scripts/train_with_dataset.py")
            print("  Deep Learning: python scripts/train_deep_learning.py")
        else:
            print(f"\n✅ Active model: {self.active_model.upper()}")
        
        print("="*60 + "\n")
        
        return rf_loaded or dl_loaded
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            'random_forest_loaded': self.rf_model is not None,
            'deep_learning_loaded': self.dl_model is not None,
            'active_model': self.active_model,
            'tensorflow_available': TF_AVAILABLE
        }
    
    def set_active_model(self, model_type: str):
        """Switch active model"""
        if model_type == 'rf' and self.rf_model is not None:
            self.active_model = 'rf'
            return True
        elif model_type == 'dl' and self.dl_model is not None:
            self.active_model = 'dl'
            return True
        return False
    
    def is_loaded(self) -> bool:
        """Check if any model is loaded"""
        return self.rf_model is not None or self.dl_model is not None

# Global model loader instance
model_loader = ModelLoader()
