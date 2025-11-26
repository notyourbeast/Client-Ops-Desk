# Fix: "Request details: flowName=GeneralOAuthFlow" Error

## What This Error Means

This error appears when:
1. **OAuth consent screen is not fully configured**
2. **App is in "Testing" mode and you're not added as a test user**
3. **Redirect URI doesn't match exactly**

## Quick Fix Steps

### Step 1: Check OAuth Consent Screen Status

1. Go to: **https://console.cloud.google.com/**
2. Select your project
3. Go to: **APIs & Services** → **OAuth consent screen**

**Check these:**
- ✅ Is the consent screen **published** or in **testing** mode?
- ✅ Are you added as a **test user** (if in testing mode)?

### Step 2: Add Yourself as Test User (If in Testing Mode)

1. In **OAuth consent screen**, go to **"Test users"** section
2. Click **"+ ADD USERS"**
3. Add your Google email address
4. Click **"ADD"**
5. **Save**

### Step 3: Verify Redirect URI Matches Exactly

1. Go to: **APIs & Services** → **Credentials**
2. Click on your **OAuth 2.0 Client ID**
3. Check **"Authorized redirect URIs"**:
   - Should be exactly: `http://localhost:5000/auth/google/callback`
   - Or if using port 5001: `http://localhost:5001/auth/google/callback`
   - **No trailing slashes!**
   - **Must match exactly** (case-sensitive)

### Step 4: Publish Your App (Recommended for Testing)

**Option A: Keep in Testing Mode (Easier)**
- Make sure you're added as a test user (Step 2)

**Option B: Publish App (No test users needed)**
1. In **OAuth consent screen**, click **"PUBLISH APP"**
2. Confirm publishing
3. This allows any Google user to sign in (for testing)

### Step 5: Verify Scopes Are Added

1. In **OAuth consent screen**, go to **"Scopes"**
2. Make sure these scopes are added:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
   - `openid`
3. If missing, click **"ADD OR REMOVE SCOPES"** and add them

### Step 6: Restart Your Application

After making changes:
```bash
# Stop your app (Ctrl+C)
# Then restart:
python run.py
```

## Common Issues and Solutions

### Issue 1: "Access blocked: This app's request is invalid"
**Solution:**
- Check redirect URI matches exactly
- Check JavaScript origin is set: `http://localhost:5000`
- Make sure no extra spaces or characters

### Issue 2: "Error 400: redirect_uri_mismatch"
**Solution:**
- The redirect URI in Google Console must match exactly
- Check for trailing slashes
- Check for `http://` vs `https://`
- Check port number matches

### Issue 3: "This app isn't verified"
**Solution:**
- This is normal for testing
- Click **"Advanced"** → **"Go to ClientHub (unsafe)"**
- Or publish your app (Step 4, Option B)

### Issue 4: "flowName=GeneralOAuthFlow" still appears
**Solution:**
1. Clear browser cache and cookies
2. Try in incognito/private mode
3. Make sure you're using the correct Google account
4. Verify all steps above are completed

## Complete Checklist

Before trying again, verify:

- [ ] OAuth consent screen is configured
- [ ] App name is set: "ClientHub"
- [ ] User support email is set
- [ ] Scopes are added (email, profile, openid)
- [ ] You're added as test user (if in testing mode)
- [ ] OR app is published (if not in testing mode)
- [ ] Redirect URI matches exactly: `http://localhost:5000/auth/google/callback`
- [ ] JavaScript origin is set: `http://localhost:5000`
- [ ] Credentials are in `.env` file
- [ ] Application restarted after changes

## Testing the Fix

1. **Start your app:**
   ```bash
   python run.py
   ```

2. **Open in browser:**
   - Go to: `http://localhost:5000/auth/login`

3. **Click "Continue with Google"**

4. **Expected flow:**
   - Redirects to Google login
   - Shows consent screen (may show "unverified" - that's OK)
   - Click "Continue" or "Allow"
   - Redirects back to your app
   - You're logged in! ✅

## Still Not Working?

If you still see the error:

1. **Check the exact error message** - copy the full error
2. **Check browser console** (F12) for any JavaScript errors
3. **Check server logs** for any Python errors
4. **Verify credentials** are correct in `.env` file
5. **Try a different browser** or incognito mode

## Need More Help?

Common mistakes:
- ❌ Redirect URI has trailing slash: `http://localhost:5000/auth/google/callback/`
- ❌ Wrong port: Using 5001 but configured for 5000
- ❌ Not added as test user (if in testing mode)
- ❌ Credentials not saved in `.env` file
- ❌ Application not restarted after adding credentials

---

**Most Common Fix:** Add yourself as a test user in OAuth consent screen! 🎯

