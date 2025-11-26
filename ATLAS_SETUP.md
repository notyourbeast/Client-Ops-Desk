# MongoDB Atlas Connection Setup

## Step 1: Get Your Connection String

Your MongoDB Atlas connection string is:
```
mongodb+srv://notyourbeast10:<db_password>@cluster0.52ms49f.mongodb.net/?appName=Cluster0
```

**Important:** Replace `<db_password>` with your actual database password.

## Step 2: Update .env File

Update your `.env` file with the Atlas connection string:

```bash
FCH_USE_MOCK_DB=false
FCH_MONGO_URI=mongodb+srv://notyourbeast10:YOUR_PASSWORD@cluster0.52ms49f.mongodb.net/?appName=Cluster0
FCH_DB_NAME=freelance_clienthub
FCH_SECRET_KEY=dev-secret-key-change-in-production
FCH_JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
```

**Replace `YOUR_PASSWORD` with your actual password.**

## Step 3: Network Access

Make sure your IP address is whitelisted in MongoDB Atlas:
1. Go to MongoDB Atlas Dashboard
2. Click "Network Access" in the left sidebar
3. Click "Add IP Address"
4. Click "Add Current IP Address" or "Allow Access from Anywhere" (0.0.0.0/0) for development

## Step 4: Database User

Ensure your database user has proper permissions:
- Username: `notyourbeast10`
- Password: (your password)
- Role: At minimum "Read and write to any database"

## Step 5: Test Connection

Run the verification script:
```bash
python verify_connection.py
```

Or test manually:
```bash
python -c "from pymongo import MongoClient; from pymongo.server_api import ServerApi; uri = 'mongodb+srv://notyourbeast10:YOUR_PASSWORD@cluster0.52ms49f.mongodb.net/?appName=Cluster0'; client = MongoClient(uri, server_api=ServerApi('1')); client.admin.command('ping'); print('✅ Connected to Atlas!')"
```

## Troubleshooting

### SSL Certificate Errors
If you see SSL errors, the code has been updated to handle Atlas connections properly.

### Connection Timeout
- Check your internet connection
- Verify IP address is whitelisted in Atlas
- Check firewall settings

### Authentication Failed
- Verify username and password are correct
- Ensure password is URL-encoded if it contains special characters
- Check database user permissions

### Network Access Denied
- Add your IP address to Atlas Network Access whitelist
- Wait a few minutes after adding IP for changes to propagate

