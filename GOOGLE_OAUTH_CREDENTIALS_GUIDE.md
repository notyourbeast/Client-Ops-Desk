# Google OAuth Credentials - Step-by-Step Guide

Follow these steps to get your Google OAuth credentials and enable Google login.

## Step 1: Go to Google Cloud Console

1. Open your web browser
2. Go to: **https://console.cloud.google.com/**
3. Sign in with your Google account

## Step 2: Create a New Project

1. Click on the **project dropdown** at the top (it may show "Select a project" or an existing project name)
2. Click **"New Project"**
3. Enter project details:
   - **Project name:** `ClientHub` (or any name you prefer)
   - **Organization:** Leave as default (if applicable)
   - **Location:** Leave as default
4. Click **"Create"**
5. Wait a few seconds for the project to be created
6. **Select the new project** from the dropdown (if not automatically selected)

## Step 3: Configure OAuth Consent Screen

1. In the left sidebar, click **"APIs & Services"**
2. Click **"OAuth consent screen"**

### For External Users (Recommended for testing):
1. Select **"External"** (unless you have Google Workspace)
2. Click **"Create"**

3. Fill in the required information:
   - **App name:** `ClientHub`
   - **User support email:** Select your email from dropdown
   - **App logo:** (Optional - skip for now)
   - **Application home page:** `http://localhost:5000` (or your domain)
   - **Application privacy policy link:** (Optional - skip for now)
   - **Application terms of service link:** (Optional - skip for now)
   - **Authorized domains:** (Leave empty for localhost)
   - **Developer contact information:** Enter your email

4. Click **"Save and Continue"**

5. **Scopes** (Step 2):
   - Click **"Add or Remove Scopes"**
   - You should see default scopes already added:
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
     - `openid`
   - If not, add them manually
   - Click **"Update"**
   - Click **"Save and Continue"**

6. **Test users** (Step 3):
   - For testing, you can add your email as a test user
   - Click **"Add Users"**
   - Enter your email address
   - Click **"Add"**
   - Click **"Save and Continue"**

7. **Summary** (Step 4):
   - Review the information
   - Click **"Back to Dashboard"**

## Step 4: Create OAuth 2.0 Credentials

1. In the left sidebar, click **"APIs & Services"** → **"Credentials"**

2. Click the **"+ CREATE CREDENTIALS"** button at the top

3. Select **"OAuth client ID"**

4. If prompted, select **"Web application"** as the application type

5. Fill in the OAuth client form:

   **Name:** `ClientHub Web Client`

   **Authorized JavaScript origins:**
   - Click **"+ ADD URI"**
   - Add: `http://localhost:5000`
   - (If using a different port, use that instead, e.g., `http://localhost:5001`)
   - Click **"+ ADD URI"** again if you want to add `http://127.0.0.1:5000`

   **Authorized redirect URIs:**
   - Click **"+ ADD URI"**
   - Add: `http://localhost:5000/auth/google/callback`
   - (If using port 5001, use: `http://localhost:5001/auth/google/callback`)
   - **Important:** The URI must match exactly!

6. Click **"CREATE"**

7. **IMPORTANT - Copy Your Credentials:**
   - A popup will appear with:
     - **Your Client ID** (looks like: `123456789-abc123def456.apps.googleusercontent.com`)
     - **Your Client Secret** (looks like: `GOCSPX-abc123def456xyz789`)
   - **Copy both values immediately** - you won't be able to see the secret again!
   - If you lose the secret, you'll need to create new credentials

## Step 5: Add Credentials to Your .env File

1. Open your `.env` file in the project root

2. Add these two lines (replace with your actual values):

```bash
FCH_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=your-client-secret-here
```

**Example:**
```bash
FCH_GOOGLE_CLIENT_ID=123456789-abc123def456ghi789jkl.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456xyz789
```

3. **Save the file**

## Step 6: Verify Your .env File

Your complete `.env` file should look like this:

```bash
# Flask Configuration
FCH_SECRET_KEY=dev-secret-key-change-in-production
FCH_JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production

# Database Configuration
FCH_MONGO_URI=mongodb+srv://notyourbeast10:qwerty123@cluster0.52ms49f.mongodb.net/?appName=Cluster0
FCH_DB_NAME=freelance_clienthub

# Google OAuth Configuration
FCH_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=your-client-secret-here
```

## Step 7: Test the Integration

1. **Start your application:**
   ```bash
   python run.py
   ```
   Or if port 5000 is busy:
   ```bash
   PORT=5001 python run.py
   ```

2. **Open your browser:**
   - Go to: `http://localhost:5000/auth/login` (or your port)

3. **Click "Continue with Google"**
   - You should be redirected to Google login
   - Sign in with your Google account
   - Grant permissions
   - You'll be redirected back and logged in!

## Troubleshooting

### "Redirect URI mismatch"
**Problem:** The redirect URI in Google Console doesn't match your application URL.

**Solution:**
- Check your redirect URI in Google Console
- Make sure it's exactly: `http://localhost:5000/auth/google/callback`
- If using a different port, update both:
  - Google Console redirect URI
  - Your application port

### "Access blocked: This app's request is invalid"
**Problem:** JavaScript origins not configured correctly.

**Solution:**
- In Google Console → Credentials → Your OAuth Client
- Make sure `http://localhost:5000` is in "Authorized JavaScript origins"
- Click "Save"

### "OAuth is not configured"
**Problem:** Credentials not found in `.env` file.

**Solution:**
- Check `.env` file exists in project root
- Verify `FCH_GOOGLE_CLIENT_ID` and `FCH_GOOGLE_CLIENT_SECRET` are set
- Restart the application after adding credentials

### "Invalid client" or "Invalid credentials"
**Problem:** Client ID or Secret is incorrect.

**Solution:**
- Double-check you copied the credentials correctly
- Make sure there are no extra spaces in `.env` file
- Verify the credentials in Google Console

## Quick Checklist

- [ ] Created Google Cloud project
- [ ] Configured OAuth consent screen
- [ ] Created OAuth 2.0 credentials
- [ ] Copied Client ID and Client Secret
- [ ] Added credentials to `.env` file
- [ ] Set authorized redirect URI: `http://localhost:5000/auth/google/callback`
- [ ] Set authorized JavaScript origin: `http://localhost:5000`
- [ ] Restarted application
- [ ] Tested "Continue with Google" button

## Security Notes

⚠️ **Important:**
- Never commit your `.env` file to version control
- Never share your Client Secret publicly
- For production, use HTTPS and update redirect URIs accordingly
- Keep your credentials secure

## Where to Find Your Credentials Later

If you need to view your credentials again:

1. Go to: https://console.cloud.google.com/
2. Select your project
3. Go to: **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID
5. You can see the Client ID (but not the secret - you'll need to create new credentials if you lose it)

---

**Ready to set up?** Follow the steps above to get your Google OAuth credentials! 🚀

