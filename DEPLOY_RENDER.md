# Deploy Flask Backend to Render

This guide will help you deploy your Flask application to Render.

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- MongoDB Atlas account (for production database)
- Google Cloud Console (for OAuth credentials)

---

## Step 1: Prepare Your Application

### 1.1 Create a Procfile

Create a `Procfile` in your project root:

```bash
web: gunicorn run:app
```

### 1.2 Update requirements.txt

Add `gunicorn` to your requirements:

```txt
Flask==3.0.0
pymongo==4.6.0
python-dotenv==1.0.0
PyJWT==2.8.0
Werkzeug==3.0.1
Authlib==1.3.0
requests==2.31.0
gunicorn==21.2.0
```

### 1.3 Update run.py for Production

Update `run.py` to work with Gunicorn:

```python
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
```

### 1.4 Update Config for Production

Update `app/config.py` to handle production settings:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('FCH_SECRET_KEY', 'dev-secret')
    MONGO_URI = os.environ.get('FCH_MONGO_URI', '')
    JWT_SECRET_KEY = os.environ.get('FCH_JWT_SECRET_KEY', 'dev-jwt-secret')
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('FCH_GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('FCH_GOOGLE_CLIENT_SECRET', '')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # Flask URL configuration for OAuth redirects
    SERVER_NAME = os.environ.get('FCH_SERVER_NAME', None)
    PREFERRED_URL_SCHEME = os.environ.get('FCH_URL_SCHEME', 'https')
```

---

## Step 2: Push to GitHub

### 2.1 Initialize Git (if not already done)

```bash
cd "/Users/sai/Desktop/Info Systems Project"
git init
git add .
git commit -m "Initial commit - ready for deployment"
```

### 2.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `clienthub-app`)
3. **Don't** initialize with README, .gitignore, or license

### 2.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/clienthub-app.git
git branch -M main
git push -u origin main
```

---

## Step 3: Set Up MongoDB Atlas (Production)

### 3.1 Create Production Database

1. Go to https://cloud.mongodb.com
2. Create a new cluster (or use existing)
3. Go to **Database Access** → Create database user
4. Go to **Network Access** → Add IP Address
   - For Render: Add `0.0.0.0/0` (allow all IPs) OR add Render's IP ranges
5. Go to **Database** → **Connect** → **Connect your application**
6. Copy the connection string (it will look like):
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

### 3.2 Update Connection String

Add your database name to the connection string:
```
mongodb+srv://username:password@cluster.mongodb.net/freelance_clienthub?retryWrites=true&w=majority
```

---

## Step 4: Update Google OAuth for Production

### 4.1 Update Google Cloud Console

1. Go to https://console.cloud.google.com
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID
5. Update **Authorized JavaScript origins**:
   - Add: `https://your-app-name.onrender.com`
6. Update **Authorized redirect URIs**:
   - Add: `https://your-app-name.onrender.com/auth/google/callback`
7. Click **Save**

---

## Step 5: Deploy to Render

### 5.1 Create New Web Service

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect your GitHub account (if not already connected)
4. Select your repository (`clienthub-app`)

### 5.2 Configure Service

Fill in the following:

- **Name**: `clienthub-app` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`

### 5.3 Add Environment Variables

Click **Add Environment Variable** and add:

```
FCH_SECRET_KEY=your-super-secret-key-here-generate-random-string
FCH_MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/freelance_clienthub?retryWrites=true&w=majority
FCH_JWT_SECRET_KEY=your-jwt-secret-key-generate-random-string
FCH_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
FCH_GOOGLE_CLIENT_SECRET=your-google-client-secret
FCH_SERVER_NAME=your-app-name.onrender.com
FCH_URL_SCHEME=https
PORT=10000
```

**Important Notes:**
- Generate random strings for `FCH_SECRET_KEY` and `FCH_JWT_SECRET_KEY`
- Use your actual MongoDB Atlas connection string
- Use your actual Google OAuth credentials
- Replace `your-app-name` with your actual Render app name

### 5.4 Create Service

Click **Create Web Service**

Render will:
1. Clone your repository
2. Install dependencies
3. Start your application
4. Give you a URL like: `https://your-app-name.onrender.com`

---

## Step 6: Verify Deployment

### 6.1 Check Logs

1. In Render dashboard, go to your service
2. Click **Logs** tab
3. Check for any errors

### 6.2 Test Your Application

1. Visit your Render URL
2. Test registration/login
3. Test Google OAuth
4. Test creating clients/projects/invoices

---

## Step 7: Set Up MongoDB Indexes

### 7.1 Run Setup Script

You can either:
- Run `setup_mongodb.py` locally (pointing to production DB)
- Or manually create indexes in MongoDB Atlas

---

## Troubleshooting

### Issue: Application won't start

**Solution:**
- Check logs in Render dashboard
- Ensure `gunicorn` is in requirements.txt
- Verify start command is correct

### Issue: Database connection fails

**Solution:**
- Verify MongoDB Atlas IP whitelist includes Render IPs
- Check connection string is correct
- Ensure database user has proper permissions

### Issue: Google OAuth redirect error

**Solution:**
- Verify redirect URI in Google Console matches Render URL
- Check `FCH_SERVER_NAME` and `FCH_URL_SCHEME` environment variables
- Ensure URL uses `https://`

### Issue: Static files not loading

**Solution:**
- Ensure static files are in `app/static/` directory
- Check Flask static folder configuration

---

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Enable auto-deploy from GitHub
3. Set up monitoring/alerts
4. Configure backups for MongoDB

---

## Security Checklist

- [ ] Use strong, random `FCH_SECRET_KEY`
- [ ] Use strong, random `FCH_JWT_SECRET_KEY`
- [ ] MongoDB connection string is secure
- [ ] Google OAuth credentials are correct
- [ ] Environment variables are set in Render (not in code)
- [ ] HTTPS is enabled (Render does this automatically)
- [ ] Database IP whitelist is configured

---

**Your app should now be live at: `https://your-app-name.onrender.com`** 🎉

