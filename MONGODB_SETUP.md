# MongoDB Setup Guide

This guide will help you connect the application to MongoDB.

## Prerequisites

1. **Install MongoDB** (if using local MongoDB):
   - macOS: `brew install mongodb-community`
   - Linux: Follow [MongoDB Installation Guide](https://www.mongodb.com/docs/manual/installation/)
   - Windows: Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

2. **Or use MongoDB Atlas** (cloud):
   - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster
   - Get your connection string

## Configuration

### Option 1: Using Environment Variables

Create a `.env` file in the project root:

```bash
# Flask Configuration
FCH_SECRET_KEY=your-secret-key-here-change-in-production
FCH_JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production

# Database Configuration
# Set to false to use MongoDB, true to use mock database
FCH_USE_MOCK_DB=false

# MongoDB Connection String
# Local MongoDB:
FCH_MONGO_URI=mongodb://localhost:27017/

# MongoDB Atlas (example):
# FCH_MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Database Name (optional, defaults to 'freelance_clienthub')
FCH_DB_NAME=freelance_clienthub
```

### Option 2: Using System Environment Variables

```bash
export FCH_USE_MOCK_DB=false
export FCH_MONGO_URI=mongodb://localhost:27017/
export FCH_SECRET_KEY=your-secret-key
export FCH_JWT_SECRET_KEY=your-jwt-secret-key
```

## Testing the Connection

1. **Start MongoDB** (if using local):
   ```bash
   # macOS with Homebrew
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   
   # Windows
   # MongoDB should start automatically as a service
   ```

2. **Test the connection**:
   ```bash
   python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); client.admin.command('ping'); print('Connected!')"
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

## Troubleshooting

### Connection Errors

If you see "MongoDB connection error" in the console:
- Check if MongoDB is running: `mongosh` or `mongo`
- Verify the connection string is correct
- Check firewall settings (for remote MongoDB)
- For MongoDB Atlas, ensure your IP is whitelisted

### Fallback to Mock Database

If MongoDB connection fails, the application will automatically fall back to the mock database. You'll see a warning message in the console.

### Switching Between Mock and MongoDB

- **Use Mock DB**: Set `FCH_USE_MOCK_DB=true` in `.env` or environment
- **Use MongoDB**: Set `FCH_USE_MOCK_DB=false` and provide `FCH_MONGO_URI`

## Database Collections

The application will automatically create these collections when you start using them:
- `users` - User accounts
- `clients` - Client information
- `projects` - Project details
- `invoices` - Invoice records
- `time_logs` - Time tracking logs

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique secret keys in production
- For MongoDB Atlas, use strong passwords and enable network access restrictions
- Consider using MongoDB authentication: `mongodb://username:password@host:port/`

