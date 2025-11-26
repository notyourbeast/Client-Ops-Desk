# Step-by-Step MongoDB Connection Guide

Follow these steps to connect your application to MongoDB.

## Step 1: Install MongoDB (Choose One Option)

### Option A: Local MongoDB Installation

**For macOS:**
```bash
# Install MongoDB using Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community
```

**For Linux (Ubuntu/Debian):**
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

**For Windows:**
1. Download MongoDB from: https://www.mongodb.com/try/download/community
2. Run the installer
3. MongoDB will start automatically as a Windows service

### Option B: Use MongoDB Atlas (Cloud - Free Tier Available)

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Try Free" or "Sign Up"
3. Create an account
4. Create a free cluster (M0 - Free tier)
5. Wait for cluster to be created (2-3 minutes)
6. Click "Connect" on your cluster
7. Choose "Connect your application"
8. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

## Step 2: Verify MongoDB is Running

**For Local MongoDB:**
```bash
# Test connection
mongosh
# or
mongo

# If connected, you'll see MongoDB shell prompt
# Type 'exit' to quit
```

**For MongoDB Atlas:**
- Your cluster should show as "Running" in the Atlas dashboard

## Step 3: Create .env File

1. Navigate to your project directory:
   ```bash
   cd "/Users/sai/Desktop/Info Systems Project"
   ```

2. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

3. Open the `.env` file in a text editor and add:

   **For Local MongoDB:**
   ```bash
   # Flask Configuration
   FCH_SECRET_KEY=your-secret-key-change-this-in-production
   FCH_JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

   # Database Configuration
   FCH_USE_MOCK_DB=false
   FCH_MONGO_URI=mongodb://localhost:27017/
   FCH_DB_NAME=freelance_clienthub
   ```

   **For MongoDB Atlas:**
   ```bash
   # Flask Configuration
   FCH_SECRET_KEY=your-secret-key-change-this-in-production
   FCH_JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

   # Database Configuration
   FCH_USE_MOCK_DB=false
   FCH_MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   FCH_DB_NAME=freelance_clienthub
   ```

   **Important:** Replace `username` and `password` in the Atlas connection string with your actual MongoDB Atlas credentials.

## Step 4: Test MongoDB Connection

Run this command to test if MongoDB is accessible:

```bash
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); uri = os.getenv('FCH_MONGO_URI', 'mongodb://localhost:27017/'); client = MongoClient(uri, serverSelectionTimeoutMS=5000); client.admin.command('ping'); print('✅ MongoDB connection successful!')"
```

**Expected output:**
- `✅ MongoDB connection successful!` - Connection works!
- Error message - Check your MongoDB setup and connection string

## Step 5: Test Application Database Connection

Test if the application can connect:

```bash
python -c "from app.repositories.db import get_db; db = get_db(); print('✅ Database connection test:', 'SUCCESS' if db else 'FAILED')"
```

**Expected output:**
- `✅ Database connection test: SUCCESS` - Everything works!
- Warning about mock database - MongoDB connection failed, check your setup

## Step 6: Run the Application

```bash
python run.py
```

**What to look for:**
- ✅ No "Warning: MONGO_URI not set" message = MongoDB connected
- ✅ No "Warning: MongoDB client is None" message = MongoDB connected
- ⚠️ If you see warnings, MongoDB connection failed (check Step 4)

## Step 7: Verify It's Working

1. Open your browser and go to: http://localhost:5000
2. Register a new account or login
3. Create a client, project, or invoice
4. Check if data persists after restarting the app

**To verify data is in MongoDB:**

**For Local MongoDB:**
```bash
mongosh
use freelance_clienthub
show collections
db.users.find().pretty()
```

**For MongoDB Atlas:**
- Go to your Atlas dashboard
- Click "Browse Collections"
- You should see your database and collections

## Troubleshooting

### Problem: "MongoDB connection error" in console

**Solutions:**
1. Check if MongoDB is running:
   ```bash
   # macOS
   brew services list | grep mongodb
   
   # Linux
   sudo systemctl status mongod
   ```

2. Verify connection string in `.env` file
3. Check if port 27017 is accessible (for local MongoDB)
4. For Atlas: Check if your IP is whitelisted in Network Access

### Problem: "Warning: MONGO_URI not set"

**Solution:**
- Make sure `.env` file exists in project root
- Check that `FCH_MONGO_URI` is set in `.env`
- Restart the application after creating/editing `.env`

### Problem: Connection timeout

**Solutions:**
1. For local MongoDB: Make sure MongoDB service is running
2. For Atlas: Check your internet connection and firewall settings
3. Verify connection string is correct

### Problem: Authentication failed (Atlas)

**Solutions:**
1. Make sure username and password in connection string are correct
2. Check if database user exists in Atlas
3. Verify database user has proper permissions

## Quick Reference

**Start MongoDB (Local):**
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

**Stop MongoDB (Local):**
```bash
# macOS
brew services stop mongodb-community

# Linux
sudo systemctl stop mongod
```

**Check MongoDB Status:**
```bash
# macOS
brew services list | grep mongodb

# Linux
sudo systemctl status mongod
```

**Use Mock Database (Fallback):**
```bash
# In .env file
FCH_USE_MOCK_DB=true
```

## Next Steps After Connection

Once connected:
1. ✅ Test creating a user account
2. ✅ Test creating clients, projects, invoices
3. ✅ Test search and filtering features
4. ✅ Verify data persists after app restart
5. ✅ Check MongoDB collections to see your data

---

**Need Help?**
- Check `MONGODB_SETUP.md` for detailed information
- Check `DEBUG_FIXES.md` for known issues and fixes
- MongoDB Documentation: https://docs.mongodb.com/

