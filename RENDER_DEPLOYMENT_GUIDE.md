# Render.com Deployment Guide - Telegram Automation Bot

## Files Created for Render.com:

### 1. `requirements.txt` (Required)
```
python-telegram-bot==20.8
flask==3.1.1
reportlab==4.4.1
qrcode==8.2
requests==2.32.3
gunicorn==23.0.0
pillow==11.2.1
```

### 2. `render.yaml` (Recommended)
```yaml
services:
  - type: web
    name: telegram-automation-bot
    env: python
    plan: free
    buildCommand: pip install python-telegram-bot==20.8 flask==3.1.1 reportlab==4.4.1 qrcode==8.2 requests==2.32.3 gunicorn==23.0.0 pillow==11.2.1
    startCommand: gunicorn --bind 0.0.0.0:$PORT main:app
    envVars:
      - key: BOT_TOKEN
        value: 7934979055:AAFGcVsNbhYh6j3RpLiGbjIHmu1Zx-mFiwc
      - key: RENDER_EXTERNAL_URL
        fromService:
          type: web
          name: telegram-automation-bot
          property: url
    healthCheckPath: /
```

### 3. `Procfile` (Alternative)
```
web: gunicorn --bind 0.0.0.0:$PORT main:app
```

## Render.com Deployment Steps:

### Method 1: Using render.yaml (Recommended)
1. **GitHub Repository Setup:**
   - Push all files to your GitHub repository
   - Make sure `render.yaml` is in root directory

2. **Render.com Dashboard:**
   - Go to https://render.com
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository with your bot code
   - Render will automatically detect `render.yaml`

### Method 2: Manual Web Service
1. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT main:app`
     - **Environment:** Python 3

2. **Environment Variables:**
   ```
   BOT_TOKEN = 7934979055:AAFGcVsNbhYh6j3RpLiGbjIHmu1Zx-mFiwc
   PORT = 5000
   ENABLE_AUTO_SCAN = true
   ENABLE_ANIMATIONS = true
   DEFAULT_SCAN_INTERVAL = 10
   ```

## Important URLs After Deployment:

1. **Health Check:** `https://your-app.onrender.com/`
2. **Webhook Setup:** `https://your-app.onrender.com/set_webhook`
3. **Health Status:** `https://your-app.onrender.com/health`

## Post-Deployment Setup:

### Step 1: Get Your Render URL
After deployment, you'll get a URL like: `https://telegram-automation-bot-xxxx.onrender.com`

### Step 2: Set Webhook
Visit: `https://your-app.onrender.com/set_webhook`
This will automatically configure your bot's webhook.

### Step 3: Test Bot
- Open Telegram
- Search for your bot: `@YourAutomationBot`
- Send `/start` command

## Features Available:

✅ **Auto Scanner** - Runs every 10 seconds
✅ **To-Do List** - Task management with Telegram storage
✅ **PDF Generator** - Text to PDF conversion
✅ **Toolkit** - Weather, calculator, QR codes
✅ **Animations** - Loading and scan animations
✅ **Hindi Support** - Full Hindi language interface
✅ **Unlimited Storage** - Uses Telegram messages for storage

## Troubleshooting:

### Bot Not Responding:
1. Check webhook status: `/health` endpoint
2. Manually set webhook: `/set_webhook` endpoint
3. Check logs in Render dashboard

### Port Binding Issues:
- Render automatically provides PORT environment variable
- App binds to `0.0.0.0:$PORT` (required for Render)

### Build Failures:
- Check `requirements.txt` dependencies
- Ensure Python 3.11 compatibility

## Commands for Users:

```
/start - Main menu with buttons
/todo - Task management
/pdf - PDF generator
/scan - Auto scan settings
/toolkit - Additional tools
/help - Help guide
```

## Auto Features:

- **Auto Scanner:** Runs every 10 seconds, checks user data
- **Auto Cleanup:** Removes old data automatically
- **Auto Webhook:** Sets up webhook on startup
- **Animations:** Loading, scanning, and progress animations

Your bot is production-ready for Render.com!