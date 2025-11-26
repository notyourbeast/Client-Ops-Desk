# How to Start the Application

## Quick Start

```bash
python run.py
```

The application will start on: **http://127.0.0.1:5000**

## If Port 5000 is Busy

### Option 1: Use a Different Port

```bash
PORT=5001 python run.py
```

Then access at: **http://127.0.0.1:5001**

### Option 2: Free Up Port 5000

**On macOS, port 5000 is often used by AirPlay Receiver:**

1. Go to **System Preferences** (or **System Settings** on newer macOS)
2. Click **General** → **AirDrop & Handoff**
3. Turn off **AirPlay Receiver**

Or kill the process:
```bash
# Find the process
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)
```

### Option 3: Use Port 8000 (Common Alternative)

```bash
PORT=8000 python run.py
```

## MongoDB Connection

Before starting, make sure:
- ✅ MongoDB Atlas IP is whitelisted
- ✅ `.env` file has correct `FCH_MONGO_URI`
- ✅ Connection test passes: `python verify_connection.py`

## Troubleshooting

### "Address already in use"
- Use a different port: `PORT=5001 python run.py`
- Or disable AirPlay Receiver (macOS)

### "MongoDB connection error"
- Check IP whitelist in Atlas
- Verify `.env` file has correct connection string
- Run: `python verify_connection.py`

### Application starts but shows errors
- Check MongoDB connection: `python verify_connection.py`
- Verify collections are set up: `python setup_mongodb.py`

## Default Configuration

- **Host:** 127.0.0.1 (localhost)
- **Port:** 5000 (or set via PORT environment variable)
- **Debug Mode:** Enabled
- **Database:** MongoDB (required)

---

**Ready to start?** Run: `python run.py` 🚀

