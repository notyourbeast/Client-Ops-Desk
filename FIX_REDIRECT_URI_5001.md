# Fix: redirect_uri_mismatch Error (Port 5001)

## The Problem

You're getting `Error 400: redirect_uri_mismatch` because:
- Your app is running on **port 5001**
- But Google Console has redirect URI for **port 5000** (or wrong URI)

## The Solution

### Step 1: Check What Your App Is Sending

Your app generates this redirect URI:
```
http://localhost:5001/auth/google/callback
```

### Step 2: Update Google Cloud Console

1. **Go to:** https://console.cloud.google.com/
2. **Select your project**
3. **Go to:** APIs & Services → Credentials
4. **Click on your OAuth 2.0 Client ID**

5. **In "Authorized redirect URIs":**
   - **Remove** any URI with port 5000
   - **Add** (if not present):
     ```
     http://localhost:5001/auth/google/callback
     ```
   - **Important:**
     - No trailing slash!
     - Must be exactly: `http://localhost:5001/auth/google/callback`
     - NOT: `http://localhost:5000/auth/google/callback`

6. **In "Authorized JavaScript origins":**
   - **Remove** `http://localhost:5000` (if present)
   - **Add** (if not present):
     ```
     http://localhost:5001
     ```
   - **Important:**
     - No trailing slash!
     - No `/auth/google/callback` part
     - Just: `http://localhost:5001`

7. **Click "SAVE"**

8. **Wait 1-2 minutes** for changes to propagate

### Step 3: Verify Your App Port

Make sure your app is actually running on port 5001:

```bash
# Check what port your app is using
PORT=5001 python run.py
```

Or if you have it set in environment:
```bash
python run.py
```

### Step 4: Test Again

1. **Restart your app** (if needed)
2. **Go to:** http://localhost:5001/auth/login
3. **Click "Continue with Google"**
4. Should work now! ✅

## Common Mistakes

### ❌ Wrong Redirect URI
```
http://localhost:5000/auth/google/callback  # Wrong port!
http://localhost:5001/auth/google/callback/  # Trailing slash!
https://localhost:5001/auth/google/callback  # Wrong scheme!
```

### ✅ Correct Redirect URI
```
http://localhost:5001/auth/google/callback
```

### ❌ Wrong JavaScript Origin
```
http://localhost:5000  # Wrong port!
http://localhost:5001/  # Trailing slash!
http://localhost:5001/auth/google/callback  # Too much!
```

### ✅ Correct JavaScript Origin
```
http://localhost:5001
```

## Quick Checklist

Before trying again:

- [ ] Removed all port 5000 URIs from Google Console
- [ ] Added redirect URI: `http://localhost:5001/auth/google/callback`
- [ ] Added JavaScript origin: `http://localhost:5001`
- [ ] No trailing slashes
- [ ] Saved changes in Google Console
- [ ] Waited 1-2 minutes
- [ ] App is running on port 5001
- [ ] Restarted app (if needed)

## Still Not Working?

If you still see the error:

1. **Double-check the exact redirect URI:**
   - Copy it from your server logs (if logged)
   - Or use: `http://localhost:5001/auth/google/callback`

2. **Clear browser cache:**
   - Or try incognito/private mode

3. **Verify port in Google Console:**
   - Make sure it says `5001`, not `5000`

4. **Check for typos:**
   - `localhost` (not `127.0.0.1`)
   - `http://` (not `https://`)
   - No extra spaces

---

**Most Common Issue:** Google Console still has port 5000 instead of 5001! 🎯

