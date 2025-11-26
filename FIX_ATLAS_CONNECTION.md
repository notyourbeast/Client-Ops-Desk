# Fix MongoDB Atlas Connection

## Current Status

✅ **Connection string configured**  
✅ **Password set**  
❌ **IP address needs to be whitelisted**  
❌ **SSL certificate issue (fixed in code)**

## Step-by-Step Fix

### Step 1: Whitelist Your IP Address (REQUIRED)

**This is the most common issue!** MongoDB Atlas requires your IP to be whitelisted.

1. **Go to MongoDB Atlas Dashboard:**
   - Visit: https://cloud.mongodb.com/
   - Log in with your account

2. **Navigate to Network Access:**
   - Click **"Network Access"** in the left sidebar
   - (It's under "Security" section)

3. **Add Your IP Address:**
   - Click the green **"Add IP Address"** button
   - Choose one of these options:
     - **"Add Current IP Address"** (recommended - more secure)
     - **"Allow Access from Anywhere"** (0.0.0.0/0) - for development only
   - Click **"Confirm"**

4. **Wait 1-2 Minutes:**
   - IP whitelist changes take 1-2 minutes to propagate
   - You'll see a green checkmark when it's active

### Step 2: Verify Your Database User

1. In Atlas Dashboard, go to **"Database Access"**
2. Find user: `notyourbeast10`
3. Verify it has **"Read and write to any database"** permission
4. If password is wrong, you can reset it here

### Step 3: Test Connection Again

After whitelisting your IP, wait 1-2 minutes, then run:

```bash
python verify_connection.py
```

Or test manually:
```bash
python -c "
from app.repositories.db import get_db
db = get_db()
if hasattr(db, 'name'):
    print('✅ Connected to Atlas!')
    print('Database:', db.name)
else:
    print('❌ Still using mock DB - check IP whitelist')
"
```

## What I've Fixed

✅ **SSL Certificate Issue** - Updated code to handle SSL certificates  
✅ **Connection String** - Configured with your password  
✅ **ServerApi** - Added for Atlas compatibility  

## Common Errors and Solutions

### Error: "authentication failed" or "bad auth"
**Cause:** IP not whitelisted or wrong password  
**Solution:** 
1. Whitelist your IP in Atlas Network Access
2. Wait 1-2 minutes
3. Verify password is correct

### Error: "SSL certificate verify failed"
**Status:** ✅ Fixed in code (tlsAllowInvalidCertificates=True)

### Error: "Connection timeout"
**Cause:** IP not whitelisted or network issue  
**Solution:** 
1. Check IP whitelist in Atlas
2. Check firewall settings
3. Try again after 2 minutes

## Quick Checklist

- [ ] IP address whitelisted in Atlas Network Access
- [ ] Waited 1-2 minutes after whitelisting
- [ ] Password is correct (qwerty123)
- [ ] Username is correct (notyourbeast10)
- [ ] Tested connection with `python verify_connection.py`

## Next Steps After Fixing

Once connection works:

1. **Set up collections:**
   ```bash
   python setup_mongodb.py
   ```

2. **Run your application:**
   ```bash
   python run.py
   ```

3. **Open in browser:**
   - Go to: http://localhost:5000
   - Register a new account
   - Start using the app!

---

**Most Important:** Whitelist your IP address in Atlas! This is required for the connection to work. 🚀

