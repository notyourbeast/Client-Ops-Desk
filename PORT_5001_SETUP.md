# Port 5001 Configuration for Google OAuth

## Important: Your app runs on port 5001

Make sure your Google OAuth configuration matches this port!

## Google Cloud Console Settings

### 1. Authorized JavaScript Origins
```
http://localhost:5001
```

### 2. Authorized Redirect URIs
```
http://localhost:5001/auth/google/callback
```

**Important:**
- Must match exactly (no trailing slash)
- Must use `http://` (not `https://`)
- Must include port `5001`

## How to Update in Google Console

1. Go to: **https://console.cloud.google.com/**
2. Select your project
3. Go to: **APIs & Services** → **Credentials**
4. Click on your **OAuth 2.0 Client ID**
5. Update:
   - **Authorized JavaScript origins:** `http://localhost:5001`
   - **Authorized redirect URIs:** `http://localhost:5001/auth/google/callback`
6. Click **"SAVE"**
7. Wait 1-2 minutes for changes to propagate

## Your Application URLs

- **Main app:** http://localhost:5001
- **Login page:** http://localhost:5001/auth/login
- **Dashboard:** http://localhost:5001/dashboard

## Running Your App

```bash
PORT=5001 python run.py
```

Or if you have it set in your environment:
```bash
python run.py
```

## Common Issues

### "redirect_uri_mismatch" Error
**Cause:** Redirect URI in Google Console doesn't match port 5001

**Fix:** Update Google Console to use `http://localhost:5001/auth/google/callback`

### "Access blocked" Error
**Cause:** JavaScript origin doesn't match

**Fix:** Update Google Console to use `http://localhost:5001` in JavaScript origins

## Quick Checklist

- [ ] JavaScript origin in Google Console: `http://localhost:5001`
- [ ] Redirect URI in Google Console: `http://localhost:5001/auth/google/callback`
- [ ] App running on port 5001
- [ ] Changes saved in Google Console
- [ ] Waited 1-2 minutes after saving

---

**Remember:** All Google OAuth settings must use port **5001**, not 5000!

