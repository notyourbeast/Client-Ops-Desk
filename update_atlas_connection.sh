#!/bin/bash
# Script to update .env file with MongoDB Atlas connection string

echo "=========================================="
echo "MongoDB Atlas Connection Setup"
echo "=========================================="
echo ""
echo "Please enter your MongoDB Atlas password:"
read -s ATLAS_PASSWORD

if [ -z "$ATLAS_PASSWORD" ]; then
    echo " Password cannot be empty!"
    exit 1
fi

# URL encode the password (basic encoding for common special characters)
ENCODED_PASSWORD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$ATLAS_PASSWORD'))")

# Create/update .env file
cat > .env << EOF
# Flask Configuration
FCH_SECRET_KEY=dev-secret-key-change-in-production
FCH_JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production

# Database Configuration
# Set to false to use MongoDB, true to use mock database
FCH_USE_MOCK_DB=false

# MongoDB Atlas Connection String
# Replace YOUR_PASSWORD with your actual password if needed
FCH_MONGO_URI=mongodb+srv://notyourbeast10:${ENCODED_PASSWORD}@cluster0.52ms49f.mongodb.net/?appName=Cluster0

# Database Name (optional, defaults to 'freelance_clienthub')
FCH_DB_NAME=freelance_clienthub
EOF

echo ""
echo ".env file updated with Atlas connection string!"
echo ""
echo "Next steps:"
echo "1. Make sure your IP is whitelisted in Atlas Network Access"
echo "2. Run: python verify_connection.py"
echo "3. Run: python run.py"

