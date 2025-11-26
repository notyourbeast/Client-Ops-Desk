# Fix: "Error 401: invalid_client" - OAuth Client Not Found

## What This Error Means

**Error 401: invalid_client** means:
- The Client ID or Client Secret in your `.env` file is **incorrect**
- There's a **typo** in the credentials
- The credentials **don't match** what's in Google Cloud Console
- There are **extra spaces** or characters in the `.env` file

## Step-by-Step Fix

### Step 1: Verify Credentials in Google Cloud Console

1. Go to: **https://console.cloud.google.com/**
2. Select your project
3. Go to: **APIs & Services** → **Credentials**
4. Find your **OAuth 2.0 Client ID**
5. Click on it to view details
6. **Copy the Client ID** (the full value)
7. **If you need the Client Secret:**
   - You can only see it when you first create it
   - If you lost it, you need to **create new credentials**

### Step 2: Check Your .env File

1. Open your `.env` file
2. Find these lines:
   ```bash
   FCH_GOOGLE_CLIENT_ID=...
   FCH_GOOGLE_CLIENT_SECRET=...
   ```

3. **Check for common mistakes:**
   - ❌ Extra spaces: `FCH_GOOGLE_CLIENT_ID = value` (space around `=`)
   - ❌ Quotes: `FCH_GOOGLE_CLIENT_ID="value"` (no quotes needed)
   - ❌ Trailing spaces: `FCH_GOOGLE_CLIENT_ID=value ` (space after value)
   - ❌ Missing parts: `FCH_GOOGLE_CLIENT_ID=123456789` (missing `.apps.googleusercontent.com`)

### Step 3: Correct Format

**Client ID should look like:**
```
123456789-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com
```

**Client Secret should look like:**
```
GOCSPX-abcdefghijklmnopqrstuvwxyz123456
```

### Step 4: Update Your .env File

**Correct format (no spaces, no quotes):**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456xyz789
```

**Important:**
- ✅ No spaces around `=`
- ✅ No quotes around values
- ✅ Complete Client ID (must end with `.apps.googleusercontent.com`)
- ✅ Complete Client Secret (usually starts with `GOCSPX-`)

### Step 5: If You Lost Your Client Secret

If you can't see your Client Secret (it's hidden after creation):

1. Go to: **APIs & Services** → **Credentials**
2. Click on your OAuth 2.0 Client ID
3. Click **"RESET SECRET"** or create a new OAuth client
4. **Copy the new Client Secret immediately**
5. Update your `.env` file with the new secret

### Step 6: Restart Your Application

After updating `.env`:
```bash
# Stop your app (Ctrl+C)
# Then restart:
python run.py
```

## Common Issues

### Issue 1: Client ID Missing `.apps.googleusercontent.com`
**Wrong:**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456
```

**Correct:**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
```

### Issue 2: Extra Spaces
**Wrong:**
```bash
FCH_GOOGLE_CLIENT_ID = 123456789-abc123def456.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_ID= 123456789-abc123def456.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com 
```

**Correct:**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
```

### Issue 3: Quotes Around Values
**Wrong:**
```bash
FCH_GOOGLE_CLIENT_ID="123456789-abc123def456.apps.googleusercontent.com"
FCH_GOOGLE_CLIENT_ID='123456789-abc123def456.apps.googleusercontent.com'
```

**Correct:**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
```

### Issue 4: Wrong Project Selected
Make sure you're:
- Using credentials from the **correct project** in Google Cloud Console
- The project is **active** and not deleted

## Verification Checklist

Before trying again:

- [ ] Client ID copied completely from Google Console
- [ ] Client ID ends with `.apps.googleusercontent.com`
- [ ] Client Secret copied completely (starts with `GOCSPX-`)
- [ ] No spaces around `=` in `.env` file
- [ ] No quotes around values
- [ ] No trailing spaces
- [ ] `.env` file saved
- [ ] Application restarted

## Testing the Fix

1. **Verify credentials format:**
   ```bash
   python -c "from app.config import Config; print('Client ID:', Config.GOOGLE_CLIENT_ID[:30] + '...' if len(Config.GOOGLE_CLIENT_ID) > 30 else Config.GOOGLE_CLIENT_ID)"
   ```

2. **Start your app:**
   ```bash
   python run.py
   ```

3. **Test Google login:**
   - Go to: `http://localhost:5000/auth/login`
   - Click "Continue with Google"
   - Should redirect to Google (not show invalid_client error)

## Still Not Working?

If you still see "invalid_client":

1. **Double-check the Client ID:**
   - Copy it fresh from Google Console
   - Make sure it's the complete value
   - Paste it directly (don't type it manually)

2. **Check Client Secret:**
   - If you lost it, create new credentials
   - Make sure it's the complete value

3. **Verify project:**
   - Make sure you're using the correct Google Cloud project
   - Check that the OAuth client exists and is enabled

4. **Check for hidden characters:**
   - Try retyping the credentials manually
   - Or copy from a text editor that shows all characters

---

**Most Common Fix:** Copy the credentials fresh from Google Console and make sure there are no extra spaces! 🎯

