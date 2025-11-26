# How to Add Google OAuth Credentials to .env File

## What You Need to Replace

You need to replace these **placeholder values** with your **actual credentials** from Google Cloud Console:

```bash
FCH_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=your-client-secret-here
```

## Step-by-Step Instructions

### Step 1: Get Your Credentials from Google Cloud Console

1. Go to: **https://console.cloud.google.com/**
2. Select your project (or create one)
3. Go to: **APIs & Services** → **Credentials**
4. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
5. Fill in:
   - **Application type:** Web application
   - **Name:** ClientHub Web Client
   - **Authorized JavaScript origins:** `http://localhost:5000`
   - **Authorized redirect URIs:** `http://localhost:5000/auth/google/callback`
6. Click **"CREATE"**
7. **Copy these two values:**
   - **Your Client ID** (looks like: `123456789-abc123def456.apps.googleusercontent.com`)
   - **Your Client Secret** (looks like: `GOCSPX-abc123def456xyz789`)

### Step 2: Open Your .env File

Open the `.env` file in your project root directory.

### Step 3: Add or Replace the Credentials

**If the lines don't exist yet**, add these two lines at the end of your `.env` file:

```bash
FCH_GOOGLE_CLIENT_ID=your-actual-client-id-here
FCH_GOOGLE_CLIENT_SECRET=your-actual-client-secret-here
```

**Replace the values:**
- Replace `your-actual-client-id-here` with your **Client ID** from Google Console
- Replace `your-actual-client-secret-here` with your **Client Secret** from Google Console

### Step 4: Example

**Before (placeholder):**
```bash
FCH_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=your-client-secret-here
```

**After (with real values):**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456ghi789jkl.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456xyz789
```

**Important:**
- ✅ Keep the variable names exactly as shown (`FCH_GOOGLE_CLIENT_ID` and `FCH_GOOGLE_CLIENT_SECRET`)
- ✅ Replace ONLY the values after the `=` sign
- ✅ Don't add quotes around the values
- ✅ Don't add extra spaces
- ✅ Make sure there are no blank lines between them

### Step 5: Save the File

Save your `.env` file after adding the credentials.

### Step 6: Verify It Works

1. Restart your application:
   ```bash
   python run.py
   ```

2. Go to: `http://localhost:5000/auth/login`

3. Click "Continue with Google"

4. If it redirects to Google login, it's working! ✅

## Complete .env File Example

Your `.env` file should look something like this (with your actual values):

```bash
# Flask Configuration
FCH_SECRET_KEY=dev-secret-key-change-in-production
FCH_JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production

# Database Configuration
FCH_MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
FCH_DB_NAME=freelance_clienthub

# Google OAuth Configuration
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456ghi789jkl.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456xyz789
```

## Common Mistakes to Avoid

❌ **Don't do this:**
```bash
FCH_GOOGLE_CLIENT_ID="123456789-abc123def456.apps.googleusercontent.com"  # No quotes!
FCH_GOOGLE_CLIENT_ID = 123456789-abc123def456.apps.googleusercontent.com  # No spaces around =
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com   # Extra spaces
```

✅ **Do this:**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
```

## Still Need Help?

If you haven't created the Google OAuth credentials yet, follow the guide:
- **GOOGLE_OAUTH_CREDENTIALS_GUIDE.md** - Complete step-by-step guide

---

**Quick Summary:**
1. Get Client ID and Secret from Google Cloud Console
2. Open `.env` file
3. Add/replace the two lines with your actual values
4. Save the file
5. Restart the application
6. Test it!

