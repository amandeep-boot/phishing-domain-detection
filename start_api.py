"""
Startup script for Phishing Detection API
Automatically loads models and starts server
"""

import os
import sys

def check_models():
    """Check which models are available"""
    print("\n" + "="*70)
    print("🔍 Checking for trained models...")
    print("="*70)
    
    rf_exists = os.path.exists('model.pkl')
    dl_exists = os.path.exists('models/phishing_model_dl.h5')
    
    print(f"\n{'Model':<30} {'Status':<20} {'Path':<30}")
    print("-"*70)
    print(f"{'Random Forest':<30} {'✓ Found' if rf_exists else '✗ Not found':<20} {'model.pkl':<30}")
    print(f"{'Deep Learning':<30} {'✓ Found' if dl_exists else '✗ Not found':<20} {'models/phishing_model_dl.h5':<30}")
    
    if not rf_exists and not dl_exists:
        print("\n⚠️  No models found!")
        print("\nTrain a model first:")
        print("  Random Forest: python scripts/train_with_dataset.py")
        print("  Deep Learning: python scripts/train_deep_learning.py")
        print("\n" + "="*70)
        return False
    
    print("\n" + "="*70)
    return True

def check_dataset():
    """Check if dataset exists"""
    if not os.path.exists('phishing_domain.csv'):
        print("\n⚠️  Dataset not found: phishing_domain.csv")
        print("Please add the dataset to the root directory.")
        return False
    return True

def start_server():
    """Start FastAPI server"""
    print("\n" + "="*70)
    print("🚀 Starting Phishing Detection API")
    print("="*70)
    print("\n📍 API will be available at:")
    print("   • http://localhost:8000")
    print("   • http://localhost:8000/docs (Swagger UI)")
    print("   • http://localhost:8000/redoc (ReDoc)")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Start uvicorn
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

def main():
    """Main startup function"""
    print("\n" + "="*70)
    print("🧠 Phishing Detection API - CSE_proj_12")
    print("="*70)
    print("Team: Akash Kumar, Aman Jadon, Amandeep")
    print("Mentor: Dr. Rupam Bhagawati")
    print("="*70)
    
    # Check dataset
    if not check_dataset():
        sys.exit(1)
    
    # Check models
    models_exist = check_models()
    
    if not models_exist:
        response = input("\nDo you want to train a model now? (y/n): ")
        if response.lower() == 'y':
            print("\nWhich model would you like to train?")
            print("1. Random Forest (fast, ~2 minutes)")
            print("2. Deep Learning (slow, ~15-30 minutes)")
            choice = input("Enter choice (1 or 2): ")
            
            if choice == '1':
                print("\n🌲 Training Random Forest...")
                os.system('python scripts/train_with_dataset.py')
            elif choice == '2':
                print("\n🧠 Training Deep Learning model...")
                os.system('python scripts/train_deep_learning.py')
            else:
                print("Invalid choice. Exiting.")
                sys.exit(1)
        else:
            print("\nExiting. Train a model first.")
            sys.exit(1)
    
    # Start server
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Server stopped")
        print("="*70)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
