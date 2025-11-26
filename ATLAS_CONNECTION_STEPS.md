# MongoDB Atlas Connection - Step by Step Guide

## Quick Setup (Automated)

**Option 1: Use the setup script**
```bash
./update_atlas_connection.sh
```
This will prompt you for your password and update the `.env` file automatically.

---

## Manual Setup

### Step 1: Update .env File

Open your `.env` file and update it with your Atlas connection string:

```bash
# Flask Configuration
FCH_SECRET_KEY=dev-secret-key-change-in-production
FCH_JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production

# Database Configuration
FCH_USE_MOCK_DB=false

# MongoDB Atlas Connection String
# IMPORTANT: Replace YOUR_PASSWORD with your actual database password
FCH_MONGO_URI=mongodb+srv://notyourbeast10:YOUR_PASSWORD@cluster0.52ms49f.mongodb.net/?appName=Cluster0

# Database Name
FCH_DB_NAME=freelance_clienthub
```

**⚠️ Important:** 
- Replace `YOUR_PASSWORD` with your actual MongoDB Atlas password
- If your password contains special characters, they need to be URL-encoded
- Example: `@` becomes `%40`, `#` becomes `%23`, etc.

### Step 2: Whitelist Your IP Address

1. Go to [MongoDB Atlas Dashboard](https://cloud.mongodb.com/)
2. Click on **"Network Access"** in the left sidebar
3. Click **"Add IP Address"**
4. Choose one:
   - **"Add Current IP Address"** (recommended for security)
   - **"Allow Access from Anywhere"** (0.0.0.0/0) - for development only
5. Click **"Confirm"**

**Note:** It may take 1-2 minutes for IP whitelist changes to take effect.

### Step 3: Verify Database User

1. In Atlas Dashboard, go to **"Database Access"**
2. Verify user `notyourbeast10` exists
3. Ensure it has **"Read and write to any database"** permission
4. If you forgot the password, you can reset it here

### Step 4: Test the Connection

```bash
# Test connection
python verify_connection.py
```

Or test manually:
```bash
python -c "
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('FCH_MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
client.admin.command('ping')
print('✅ Successfully connected to MongoDB Atlas!')
"
```

### Step 5: Set Up Collections

```bash
python setup_mongodb.py
```

This will create all necessary collections and indexes.

### Step 6: Run Your Application

```bash
python run.py
```

Then open http://localhost:5000 in your browser.

---

## Troubleshooting

### Error: "IP not whitelisted"
**Solution:** Add your IP address in Atlas Network Access settings

### Error: "Authentication failed"
**Solutions:**
- Verify password is correct
- Check if password needs URL encoding
- Verify username is `notyourbeast10`

### Error: "SSL certificate verify failed"
**Solution:** The code has been updated to handle this. If you still see errors, make sure you're using the latest code.

### Error: "Connection timeout"
**Solutions:**
- Check your internet connection
- Verify IP is whitelisted
- Check firewall settings
- Wait 1-2 minutes after adding IP to whitelist

### Password with Special Characters

If your password contains special characters, you need to URL-encode them:

| Character | Encoded |
|-----------|---------|
| `@` | `%40` |
| `#` | `%23` |
| `$` | `%24` |
| `%` | `%25` |
| `&` | `%26` |
| `+` | `%2B` |
| `=` | `%3D` |

**Example:**
- Password: `MyP@ss#123`
- Encoded: `MyP%40ss%23123`
- Connection string: `mongodb+srv://notyourbeast10:MyP%40ss%23123@cluster0.52ms49f.mongodb.net/...`

Or use the automated script which handles encoding automatically.

---

## Verification Checklist

- [ ] `.env` file updated with Atlas connection string
- [ ] Password replaced in connection string
- [ ] IP address whitelisted in Atlas
- [ ] Database user has proper permissions
- [ ] Connection test successful (`python verify_connection.py`)
- [ ] Collections set up (`python setup_mongodb.py`)
- [ ] Application runs without errors

---

## Quick Commands Reference

```bash
# Update connection (automated)
./update_atlas_connection.sh

# Verify connection
python verify_connection.py

# Set up collections
python setup_mongodb.py

# Run application
python run.py

# Test connection manually
python -c "from app.repositories.db import get_db; db = get_db(); print('Database:', db.name)"
```

---

## Your Connection Details

- **Cluster:** Cluster0
- **Username:** notyourbeast10
- **Connection String Format:** `mongodb+srv://notyourbeast10:PASSWORD@cluster0.52ms49f.mongodb.net/?appName=Cluster0`
- **Database Name:** freelance_clienthub

---

**Ready to connect!** Follow the steps above to set up your Atlas connection. 🚀

