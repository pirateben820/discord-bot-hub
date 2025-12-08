"""
Quick test script to verify backend can start
"""
import sys
sys.path.insert(0, 'backend')

try:
    print("Testing imports...")
    from config import settings
    print("✅ Config imported successfully")
    
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
    
    import socketio
    print("✅ Socket.IO imported successfully")
    
    print("\n🎉 All imports successful! Backend is ready to run.")
    print("\nTo start the backend, run:")
    print("  cd backend")
    print("  python main.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

