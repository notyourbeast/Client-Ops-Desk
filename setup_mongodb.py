"""
MongoDB Setup Script for ClientHub
This script sets up the database, collections, and indexes for optimal performance.
"""

from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('FCH_MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('FCH_DB_NAME', 'freelance_clienthub')

def setup_database():
    """Set up MongoDB database, collections, and indexes"""
    
    try:
        print("🔌 Connecting to MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        
        db = client[DB_NAME]
        print(f"📊 Using database: {DB_NAME}")
        
        # Collections that will be used
        collections = {
            'users': {
                'description': 'User accounts and authentication',
                'indexes': [
                    ('email', ASCENDING, {'unique': True}),
                    ('user_id', ASCENDING)
                ]
            },
            'clients': {
                'description': 'Client information',
                'indexes': [
                    ('user_id', ASCENDING),
                    ('email', ASCENDING)
                ]
            },
            'projects': {
                'description': 'Project details and status',
                'indexes': [
                    ('user_id', ASCENDING),
                    ('client_id', ASCENDING),
                    ('status', ASCENDING)
                ]
            },
            'invoices': {
                'description': 'Invoice records',
                'indexes': [
                    ('user_id', ASCENDING),
                    ('project_id', ASCENDING),
                    ('status', ASCENDING),
                    ('created_at', ASCENDING)
                ]
            },
            'time_logs': {
                'description': 'Time tracking logs',
                'indexes': [
                    ('user_id', ASCENDING),
                    ('project_id', ASCENDING),
                    ('start_time', ASCENDING),
                    ('end_time', ASCENDING)
                ]
            }
        }
        
        print("\n📋 Setting up collections and indexes...")
        print("-" * 60)
        
        for collection_name, config in collections.items():
            collection = db[collection_name]
            
            # Create collection (MongoDB creates it automatically on first insert)
            # But we'll verify it exists
            if collection_name not in db.list_collection_names():
                print(f"📁 Creating collection: {collection_name}")
            else:
                print(f"✅ Collection exists: {collection_name}")
            
            print(f"   Description: {config['description']}")
            
            # Create indexes
            for index_config in config['indexes']:
                if len(index_config) == 2:
                    field, direction = index_config
                    unique = False
                else:
                    field, direction, options = index_config
                    unique = options.get('unique', False)
                
                try:
                    collection.create_index(
                        [(field, direction)],
                        unique=unique,
                        background=True
                    )
                    unique_text = " (unique)" if unique else ""
                    print(f"   ✓ Index created: {field}{unique_text}")
                except Exception as e:
                    print(f"   ⚠️  Index {field}: {str(e)}")
            
            # Show collection stats
            count = collection.count_documents({})
            print(f"   📊 Documents: {count}")
            print()
        
        print("-" * 60)
        print("✅ Database setup complete!")
        print("\n📊 Database Summary:")
        print(f"   Database: {DB_NAME}")
        print(f"   Collections: {', '.join(db.list_collection_names())}")
        print(f"   Total collections: {len(db.list_collection_names())}")
        
        return True
        
    except ConnectionFailure:
        print("❌ Error: Could not connect to MongoDB")
        print(f"   URI: {MONGO_URI}")
        print("   Please check if MongoDB is running and the connection string is correct.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ClientHub MongoDB Setup")
    print("=" * 60)
    print()
    
    success = setup_database()
    
    if success:
        print("\n✨ Your database is ready to use!")
        print("   You can now run: python run.py")
    else:
        print("\n⚠️  Setup incomplete. Please fix the errors above.")
        exit(1)

