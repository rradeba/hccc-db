#!/usr/bin/env python3
"""
Simple test script to debug Flask server issues
"""
import sys
import os

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))

try:
    print("\n=== Testing imports ===")
    from flask import Flask
    print("✓ Flask imported successfully")
    
    from flask_sqlalchemy import SQLAlchemy
    print("✓ SQLAlchemy imported successfully")
    
    from flask_migrate import Migrate
    print("✓ Migrate imported successfully")
    
    from flask_cors import CORS
    print("✓ CORS imported successfully")
    
    from dotenv import load_dotenv
    print("✓ dotenv imported successfully")
    
    print("\n=== Testing app creation ===")
    from app import create_app
    print("✓ create_app imported successfully")
    
    app = create_app()
    print("✓ App created successfully")
    
    print("\n=== Testing routes ===")
    with app.test_client() as client:
        response = client.get('/health')
        print(f"Health endpoint status: {response.status_code}")
        print(f"Health response: {response.get_data(as_text=True)}")
    
    print("\n=== Starting server ===")
    app.run(host='127.0.0.1', port=5050, debug=True)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()


