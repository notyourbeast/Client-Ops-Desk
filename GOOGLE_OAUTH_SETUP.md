# Google OAuth Setup Guide

This guide will help you set up Google OAuth authentication for your ClientHub application.

## Step 1: Create Google OAuth Credentials

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project (or select existing):**
   - Click "Select a project" → "New Project"
   - Enter project name: "ClientHub" (or any name)
   - Click "Create"

3. **Enable Google+ API:**
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API" or "People API"
   - Click "Enable"

4. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Choose "External" (for testing) or "Internal" (for Google Workspace)
   - Fill in required fields:
     - App name: "ClientHub"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" (click "Save and Continue")
   - Skip "Test users" (click "Save and Continue")
   - Review and click "Back to Dashboard"

5. **Create OAuth 2.0 Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: **Web application**
   - Name: "ClientHub Web Client"
   - **Authorized JavaScript origins:**
     - For local development: `http://localhost:5000` or `http://127.0.0.1:5000`
     - For production: `https://yourdomain.com`
   - **Authorized redirect URIs:**
     - For local: `http://localhost:5000/auth/google/callback`
     - For production: `https://yourdomain.com/auth/google/callback`
   - Click "Create"
   - **Copy your Client ID and Client Secret** (you'll need these!)

## Step 2: Configure Your Application

Add the credentials to your `.env` file:

```bash
# Google OAuth Configuration
FCH_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=your-client-secret
```

**Important:** Replace `your-client-id` and `your-client-secret` with the actual values from Google Cloud Console.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `Authlib` and `requests` needed for OAuth.

## Step 4: Test the Integration

1. **Start your application:**
   ```bash
   python run.py
   ```

2. **Go to login/register page:**
   - Visit: http://localhost:5000/auth/login
   - Click "Continue with Google"
   - You should be redirected to Google login
   - After logging in, you'll be redirected back and logged in!

## How It Works

1. **User clicks "Continue with Google"**
   - Redirects to `/auth/google/login`
   - Initiates OAuth flow with Google

2. **Google Authentication**
   - User logs in with Google account
   - Google asks for permission to share email/name

3. **Callback**
   - Google redirects back to `/auth/google/callback`
   - Application receives user info (email, name)
   - Creates new user account (if first time) or logs in existing user
   - Sets authentication cookie
   - Redirects to dashboard

## Features

✅ **Automatic User Creation** - New users are created automatically  
✅ **Email-based Login** - Existing users with same email can log in  
✅ **No Password Required** - Google handles authentication  
✅ **Secure** - Uses OAuth 2.0 standard  
✅ **Works for Login and Signup** - Same button for both  

## Troubleshooting

### "Google OAuth is not configured"
- Make sure `FCH_GOOGLE_CLIENT_ID` and `FCH_GOOGLE_CLIENT_SECRET` are set in `.env`
- Restart the application after adding credentials

### "Redirect URI mismatch"
- Check that your redirect URI in Google Console matches exactly:
  - Local: `http://localhost:5000/auth/google/callback`
  - Or: `http://127.0.0.1:5000/auth/google/callback`
- Make sure the port matches your application port

### "Access blocked: This app's request is invalid"
- Check authorized JavaScript origins in Google Console
- Make sure `http://localhost:5000` (or your port) is added

### OAuth works but user not created
- Check MongoDB connection
- Check application logs for errors
- Verify database collections exist

## Security Notes

- **Never commit `.env` file** to version control
- **Keep Client Secret secure** - don't share it publicly
- **Use HTTPS in production** - OAuth requires secure connections
- **Update redirect URIs** when deploying to production

## Production Setup

For production deployment:

1. **Update Authorized JavaScript origins:**
   - Add: `https://yourdomain.com`

2. **Update Authorized redirect URIs:**
   - Add: `https://yourdomain.com/auth/google/callback`

3. **Update `.env` file:**
   ```bash
   FCH_GOOGLE_CLIENT_ID=your-production-client-id
   FCH_GOOGLE_CLIENT_SECRET=your-production-client-secret
   ```

4. **Use HTTPS** - Google OAuth requires HTTPS in production

---

**Ready to set up?** Follow the steps above to get Google OAuth working! 🚀

