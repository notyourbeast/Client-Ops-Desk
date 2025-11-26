#!/usr/bin/env python3
"""
Connection Verification Script
Run this to verify your MongoDB connection is working correctly.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

def verify_connection():
    print("=" * 60)
    print("🔍 MongoDB Connection Verification")
    print("=" * 60)
    print()
    
    # Step 1: Check environment variables
    print("📋 Step 1: Checking Environment Variables")
    print("-" * 60)
    mongo_uri = os.getenv('FCH_MONGO_URI', '')
    db_name = os.getenv('FCH_DB_NAME', 'freelance_clienthub')
    
    print(f"   FCH_MONGO_URI: {mongo_uri if mongo_uri else 'NOT SET'}")
    print(f"   FCH_DB_NAME: {db_name}")
    
    if not mongo_uri:
        print("   ❌ MONGO_URI is not set!")
        print("   Please configure MongoDB connection in .env file")
        return False
    
    print("   ✅ Environment variables configured")
    print()
    
    # Step 2: Test MongoDB connection
    print("🔌 Step 2: Testing MongoDB Connection")
    print("-" * 60)
    try:
        # Handle Atlas connections with SSL fix
        if 'mongodb+srv://' in mongo_uri:
            from pymongo.server_api import ServerApi
            client = MongoClient(
                mongo_uri, 
                server_api=ServerApi('1'),
                serverSelectionTimeoutMS=10000,
                tlsAllowInvalidCertificates=True
            )
        else:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("   ✅ MongoDB connection successful!")
        print(f"   ✅ Server: {client.address}")
    except ConnectionFailure as e:
        error_msg = str(e)
        print(f"   ❌ Connection failed")
        if 'authentication failed' in error_msg.lower() or 'bad auth' in error_msg.lower():
            print("   ⚠️  Authentication error - check:")
            print("      • Password is correct")
            print("      • IP address is whitelisted in Atlas")
        elif 'SSL' in error_msg or 'CERTIFICATE' in error_msg:
            print("   ⚠️  SSL certificate error - this should be fixed in the code")
        else:
            print(f"   Error details: {error_msg[:200]}")
        return False
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ Error: {error_msg[:200]}")
        if 'authentication' in error_msg.lower() or 'bad auth' in error_msg.lower():
            print("   ⚠️  Check your password and IP whitelist in Atlas")
        return False
    print()
    
    # Step 3: Test database access
    print("📊 Step 3: Testing Database Access")
    print("-" * 60)
    try:
        db = client[db_name]
        collections = db.list_collection_names()
        print(f"   ✅ Database '{db_name}' accessible")
        print(f"   ✅ Collections found: {len(collections)}")
        if collections:
            print(f"   ✅ Collection names: {', '.join(collections)}")
        else:
            print("   ℹ️  No collections yet (will be created automatically)")
    except Exception as e:
        print(f"   ❌ Database access failed: {e}")
        return False
    print()
    
    # Step 4: Test application database connection
    print("🚀 Step 4: Testing Application Database Connection")
    print("-" * 60)
    try:
        from app.repositories.db import get_db
        app_db = get_db()
        
        if hasattr(app_db, 'name'):
            print(f"   ✅ Application connected to MongoDB")
            print(f"   ✅ Database name: {app_db.name}")
            print(f"   ✅ Database type: MongoDB Database")
        else:
            print("   ❌ Application database connection failed")
            print("   ❌ Check your MongoDB connection settings")
            return False
    except Exception as e:
        print(f"   ❌ Application connection test failed: {e}")
        return False
    print()
    
    # Final summary
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("🎉 Your MongoDB connection is working correctly!")
    print()
    print("Next steps:")
    print("   1. Run: python run.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Register a new account")
    print("   4. Start using the application!")
    print()
    
    return True

if __name__ == '__main__':
    success = verify_connection()
    if not success:
        print("❌ Connection verification failed. Please check the errors above.")
        exit(1)

