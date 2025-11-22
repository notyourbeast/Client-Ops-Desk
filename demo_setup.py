"""
Demo setup script - Run this to enable demo mode without MongoDB

Usage:
    export FCH_USE_MOCK_DB=true
    python demo_setup.py

Or set FCH_USE_MOCK_DB=true in your .env file
"""

import os
import sys

os.environ['FCH_USE_MOCK_DB'] = 'true'
os.environ['FCH_SECRET_KEY'] = os.environ.get('FCH_SECRET_KEY', 'demo-secret-key')
os.environ['FCH_JWT_SECRET_KEY'] = os.environ.get('FCH_JWT_SECRET_KEY', 'demo-jwt-secret')

print("Demo mode enabled!")
print("\nTo use demo mode:")
print("1. Set FCH_USE_MOCK_DB=true in your environment")
print("2. Or run: export FCH_USE_MOCK_DB=true")
print("\nDemo credentials:")
print("Email: demo@example.com")
print("Password: demo")
print("\nStarting Flask app...")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    app.run(debug=True, port=5000)

