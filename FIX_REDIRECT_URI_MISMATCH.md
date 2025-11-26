# Fix: Error 400: redirect_uri_mismatch

## What This Error Means

The redirect URI that your application is sending to Google doesn't match what's configured in Google Cloud Console.

## Quick Fix Steps

### Step 1: Check What Redirect URI Your App Is Using

When you start your app and click "Continue with Google", check your server terminal. You should see a log message like:
```
OAuth redirect URI: http://localhost:5000/auth/google/callback
```

**Copy this exact URI!**

### Step 2: Update Google Cloud Console

1. Go to: **https://console.cloud.google.com/**
2. Select your project
3. Go to: **APIs & Services** → **Credentials**
4. Click on your **OAuth 2.0 Client ID**
5. In **"Authorized redirect URIs"** section:
   - **Remove any existing redirect URIs** that don't match
   - Click **"+ ADD URI"**
   - Paste the exact URI from Step 1 (e.g., `http://localhost:5000/auth/google/callback`)
   - **Important:** 
     - No trailing slash!
     - Must match exactly (including `http://` vs `https://`)
     - Must match the port number (5000 or 5001)
6. Click **"SAVE"**

### Step 3: Common Redirect URI Formats

Depending on your setup, it might be one of these:

- `http://localhost:5000/auth/google/callback`
- `http://localhost:5001/auth/google/callback` (if using port 5001)
- `http://127.0.0.1:5000/auth/google/callback`

**Make sure the one in Google Console matches exactly what your app is using!**

### Step 4: Verify JavaScript Origin

Also check **"Authorized JavaScript origins"**:

- Should be: `http://localhost:5000` (or `http://localhost:5001` if using that port)
- No trailing slash
- No `/auth/google/callback` part (just the base URL)

### Step 5: Restart and Test

1. **Save changes in Google Console**
2. **Wait 1-2 minutes** for changes to propagate
3. **Restart your application:**
   ```bash
   python run.py
   ```
4. **Try again** - click "Continue with Google"

## Still Not Working?

### Check Your Port

If you're running on a different port (like 5001), make sure:

1. **Google Console** has the redirect URI for that port:
   - `http://localhost:5001/auth/google/callback`

2. **Your app** is actually running on that port:
   ```bash
   PORT=5001 python run.py
   ```

### Check for Multiple Redirect URIs

If you have multiple redirect URIs in Google Console:
- Remove all of them
- Add only the one your app is actually using
- Save

### Try Both localhost and 127.0.0.1

Sometimes it helps to add both:

1. `http://localhost:5000/auth/google/callback`
2. `http://127.0.0.1:5000/auth/google/callback`

But make sure the one your app uses is there!

## Verification Checklist

Before trying again:

- [ ] Checked server logs for the exact redirect URI
- [ ] Added that exact URI to Google Console
- [ ] Removed any incorrect/old redirect URIs
- [ ] JavaScript origin is set correctly
- [ ] Saved changes in Google Console
- [ ] Waited 1-2 minutes for propagation
- [ ] Restarted the application
- [ ] Tried again

## Debug: See What URI Is Being Sent

The app now logs the redirect URI. Check your server terminal when you click "Continue with Google" - you'll see:
```
OAuth redirect URI: http://localhost:5000/auth/google/callback
```

Use that exact value in Google Console!

---

**Most Common Issue:** The redirect URI in Google Console has a trailing slash or uses a different port/hostname than your app.

