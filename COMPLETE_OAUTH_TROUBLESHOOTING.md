# Complete Google OAuth Troubleshooting Guide

## Current Status Check

Run this to check your configuration:
```bash
python test_oauth.py
```

## Common Issues and Solutions

### Issue 1: "Error 401: invalid_client"
**Cause:** Client ID or Secret is wrong

**Fix:**
1. Go to Google Cloud Console → Credentials
2. Copy the Client ID fresh (make sure it ends with `.apps.googleusercontent.com` only once)
3. If you lost the secret, create new credentials
4. Update `.env` file
5. Restart app

### Issue 2: "Redirect URI mismatch"
**Cause:** Redirect URI in Google Console doesn't match

**Fix:**
1. Run `python test_oauth.py` to see your redirect URI
2. Go to Google Cloud Console → Credentials → Your OAuth Client
3. Add the exact redirect URI shown in the test output
4. Make sure there are no trailing slashes
5. Save and try again

### Issue 3: "Access blocked" or "This app isn't verified"
**Cause:** App is in testing mode and you're not a test user

**Fix Option A (Add as Test User):**
1. Go to: OAuth consent screen → Test users
2. Click "+ ADD USERS"
3. Add your Google email
4. Save

**Fix Option B (Publish App):**
1. Go to: OAuth consent screen
2. Click "PUBLISH APP"
3. Confirm
4. Now any user can sign in

### Issue 4: "flowName=GeneralOAuthFlow"
**Cause:** OAuth consent screen not fully configured

**Fix:**
1. Complete all steps in OAuth consent screen:
   - App name
   - User support email
   - Scopes (email, profile, openid)
   - Test users (if in testing mode)
2. Save all steps
3. Try again

### Issue 5: Nothing happens when clicking "Continue with Google"
**Cause:** JavaScript error or OAuth not initialized

**Fix:**
1. Check browser console (F12) for errors
2. Check server logs for errors
3. Verify credentials are in `.env` file
4. Restart the application

## Step-by-Step Verification

### Step 1: Verify Credentials Format
```bash
python -c "from app.config import Config; print('Client ID:', Config.GOOGLE_CLIENT_ID); print('Secret:', Config.GOOGLE_CLIENT_SECRET[:10] + '...')"
```

Should show:
- Client ID ending with `.apps.googleusercontent.com`
- Secret starting with `GOCSPX-`

### Step 2: Verify Redirect URI
```bash
python test_oauth.py
```

Copy the redirect URI shown and verify it's in Google Console.

### Step 3: Check Google Console Settings

**In Google Cloud Console:**

1. **OAuth Consent Screen:**
   - App name: Set
   - User support email: Set
   - Scopes: email, profile, openid
   - Test users: Your email added (if in testing mode)
   - OR: App is published

2. **Credentials:**
   - OAuth 2.0 Client ID exists
   - Authorized JavaScript origins: `http://localhost:5000`
   - Authorized redirect URIs: `http://localhost:5000/auth/google/callback` (exact match)

### Step 4: Test the Flow

1. Start your app: `python run.py`
2. Go to: `http://localhost:5000/auth/login`
3. Click "Continue with Google"
4. Should redirect to Google login
5. Sign in with Google
6. Should redirect back to your app

## Complete Checklist

Before trying again, verify ALL of these:

- [ ] Client ID is correct in `.env` (ends with `.apps.googleusercontent.com`)
- [ ] Client Secret is correct in `.env` (starts with `GOCSPX-`)
- [ ] No extra spaces in `.env` file
- [ ] Application restarted after changing `.env`
- [ ] Redirect URI matches exactly in Google Console
- [ ] JavaScript origin is set: `http://localhost:5000`
- [ ] OAuth consent screen is configured
- [ ] You're added as test user (if in testing mode)
- [ ] OR app is published (if not in testing mode)
- [ ] Scopes are added: email, profile, openid

## Still Not Working?

If nothing above works:

1. **Create new OAuth credentials:**
   - Delete old OAuth client in Google Console
   - Create new one
   - Copy fresh Client ID and Secret
   - Update `.env` file
   - Restart app

2. **Check server logs:**
   - Look for any Python errors
   - Check for OAuth-related errors

3. **Check browser console:**
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

4. **Try different browser:**
   - Sometimes browser cache causes issues
   - Try incognito/private mode

5. **Verify port:**
   - Make sure you're using the same port everywhere
   - If using port 5001, update all references

## Quick Test Commands

```bash
# Test configuration
python test_oauth.py

# Check credentials
python -c "from app.config import Config; print('ID:', Config.GOOGLE_CLIENT_ID); print('Secret:', 'Set' if Config.GOOGLE_CLIENT_SECRET else 'Missing')"

# Test app loads
python -c "from app import create_app; app = create_app(); print('✅ App loads')"
```

---

**Most Common Issues:**
1. Redirect URI doesn't match exactly
2. Not added as test user (if in testing mode)
3. Credentials have typos or extra spaces
4. Application not restarted after changing `.env`

