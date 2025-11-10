"""
Unified Predictor for both Random Forest and Deep Learning models
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from app.utils.ml_loader_enhanced import model_loader
from app.utils.feature_extraction_full import full_feature_extractor

class UnifiedPredictor:
    """Predict using either Random Forest or Deep Learning"""
    
    def __init__(self):
        self.feature_extractor = full_feature_extractor
    
    def predict(self, url: str, model_type: str = None) -> Dict[str, Any]:
        """
        Predict if URL is phishing
        
        Args:
            url: URL to check
            model_type: 'rf', 'dl', or None (use active model)
        
        Returns:
            Dictionary with prediction results
        """
        
        if not model_loader.is_loaded():
            raise Exception("No model loaded. Train a model first.")
        
        # Determine which model to use
        if model_type is None:
            model_type = model_loader.active_model
        
        # Extract features
        features = self.feature_extractor.extract_features(url)
        
        if model_type == 'rf':
            return self._predict_rf(features, url)
        elif model_type == 'dl':
            return self._predict_dl(features, url)
        else:
            raise ValueError(f"Invalid model type: {model_type}")
    
    def _predict_rf(self, features: Dict, url: str) -> Dict[str, Any]:
        """Predict using Random Forest"""
        if model_loader.rf_model is None:
            raise Exception("Random Forest model not loaded")
        
        # Convert to DataFrame
        X = pd.DataFrame([features])
        
        # Predict
        prediction = model_loader.rf_model.predict(X)[0]
        probabilities = model_loader.rf_model.predict_proba(X)[0]
        
        return {
            'url': url,
            'prediction': 'phishing' if prediction == 1 else 'legitimate',
            'is_phishing': bool(prediction),
            'confidence': float(max(probabilities) * 100),
            'probabilities': {
                'legitimate': float(probabilities[0] * 100),
                'phishing': float(probabilities[1] * 100)
            },
            'model_used': 'Random Forest',
            'risk_level': self._get_risk_level(probabilities[1])
        }
    
    def _predict_dl(self, features: Dict, url: str) -> Dict[str, Any]:
        """Predict using Deep Learning"""
        if model_loader.dl_model is None:
            raise Exception("Deep Learning model not loaded")
        
        # Convert to array (111 features)
        feature_values = list(features.values())
        X = np.array(feature_values).reshape(1, -1)
        
        # Scale features if scaler available
        if model_loader.scaler is not None:
            X = model_loader.scaler.transform(X)
        
        # Predict
        prediction_proba = model_loader.dl_model.predict(X, verbose=0)[0][0]
        prediction = 1 if prediction_proba > 0.5 else 0
        
        return {
            'url': url,
            'prediction': 'phishing' if prediction == 1 else 'legitimate',
            'is_phishing': bool(prediction),
            'confidence': float(max(prediction_proba, 1 - prediction_proba) * 100),
            'probabilities': {
                'legitimate': float((1 - prediction_proba) * 100),
                'phishing': float(prediction_proba * 100)
            },
            'model_used': 'Neural Network',
            'risk_level': self._get_risk_level(prediction_proba)
        }
    
    def _get_risk_level(self, phishing_prob: float) -> str:
        """Determine risk level based on probability"""
        if phishing_prob > 0.7:
            return 'high'
        elif phishing_prob > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def compare_models(self, url: str) -> Dict[str, Any]:
        """Get predictions from both models for comparison"""
        results = {
            'url': url,
            'models': {}
        }
        
        # Extract features once
        features = self.feature_extractor.extract_features(url)
        
        if model_loader.rf_model is not None:
            try:
                results['models']['random_forest'] = self._predict_rf(features, url)
            except Exception as e:
                results['models']['random_forest'] = {'error': str(e)}
        
        if model_loader.dl_model is not None:
            try:
                results['models']['deep_learning'] = self._predict_dl(features, url)
            except Exception as e:
                results['models']['deep_learning'] = {'error': str(e)}
        
        return results

# Global predictor instance
predictor = UnifiedPredictor()
