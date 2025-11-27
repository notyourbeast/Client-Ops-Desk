# Quick Deployment Guide

## 🚀 Recommended: Deploy Everything on Render

Your Flask application is a **monolithic app** (backend + frontend together). The simplest and recommended approach is to deploy everything on Render.

### Why Render Only?

✅ Your Flask app already serves HTML templates  
✅ No need to separate frontend/backend  
✅ Single deployment = easier maintenance  
✅ All features work as-is  
✅ Faster to deploy  

---

## 📋 Quick Steps

### 1. Prepare Files (Already Done ✅)

- ✅ `Procfile` created
- ✅ `gunicorn` added to requirements.txt
- ✅ `run.py` updated for production
- ✅ `config.py` updated for HTTPS

### 2. Push to GitHub

```bash
cd "/Users/sai/Desktop/Info Systems Project"
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/clienthub-app.git
git push -u origin main
```

### 3. Deploy on Render

1. Go to https://render.com → Sign up/Login
2. Click **New +** → **Web Service**
3. Connect GitHub → Select your repository
4. Configure:
   - **Name**: `clienthub-app`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
5. Add Environment Variables (see below)
6. Click **Create Web Service**

### 4. Environment Variables in Render

Add these in Render dashboard:

```
FCH_SECRET_KEY=<generate-random-string>
FCH_MONGO_URI=<your-mongodb-atlas-connection-string>
FCH_JWT_SECRET_KEY=<generate-random-string>
FCH_GOOGLE_CLIENT_ID=<your-google-client-id>
FCH_GOOGLE_CLIENT_SECRET=<your-google-client-secret>
FCH_SERVER_NAME=<your-app-name.onrender.com>
FCH_URL_SCHEME=https
PORT=10000
```

### 5. Update Google OAuth

1. Go to Google Cloud Console
2. Update **Authorized redirect URIs**:
   - Add: `https://your-app-name.onrender.com/auth/google/callback`
3. Update **Authorized JavaScript origins**:
   - Add: `https://your-app-name.onrender.com`

### 6. Done! 🎉

Your app will be live at: `https://your-app-name.onrender.com`

---

## 📚 Detailed Guides

- **DEPLOY_RENDER.md** - Complete Render deployment guide
- **DEPLOY_NETLIFY.md** - Guide for separate frontend (if needed)

---

## ⚠️ Important Notes

1. **MongoDB Atlas**: Make sure your database allows connections from Render IPs
2. **Google OAuth**: Update redirect URIs to match your Render URL
3. **Environment Variables**: Never commit `.env` file to GitHub
4. **HTTPS**: Render automatically provides HTTPS

---

## 🔒 Security Checklist

- [ ] Strong `FCH_SECRET_KEY` (random string)
- [ ] Strong `FCH_JWT_SECRET_KEY` (random string)
- [ ] MongoDB connection string is secure
- [ ] Google OAuth credentials updated
- [ ] Environment variables set in Render
- [ ] Database IP whitelist configured

---

## 🆘 Troubleshooting

### App won't start
- Check Render logs
- Verify `gunicorn` is in requirements.txt
- Check start command is correct

### Database connection fails
- Check MongoDB Atlas IP whitelist
- Verify connection string
- Check database user permissions

### OAuth doesn't work
- Verify redirect URI in Google Console
- Check `FCH_SERVER_NAME` and `FCH_URL_SCHEME`
- Ensure URL uses `https://`

---

**Need help?** See detailed guides:
- `DEPLOY_RENDER.md` for complete Render setup
- `DEPLOY_NETLIFY.md` if you want separate frontend

