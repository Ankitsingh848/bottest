# Render.com Deployment Commands

## Build Command:
```bash
pip install python-telegram-bot==20.8 flask==3.1.1 reportlab==4.4.1 qrcode==8.2 requests==2.32.3 gunicorn==23.0.0 pillow==11.2.1
```

## Start Command:
```bash
gunicorn --bind 0.0.0.0:$PORT main:app
```

## Alternative Start Commands:
```bash
# Option 1 (Recommended):
gunicorn --bind 0.0.0.0:$PORT main:app --workers 1 --timeout 60

# Option 2:
python main.py

# Option 3:
gunicorn main:app --bind 0.0.0.0:$PORT --log-level info
```

## Environment Variables (Required):
```
BOT_TOKEN = 7934979055:AAFGcVsNbhYh6j3RpLiGbjIHmu1Zx-mFiwc
PORT = 5000
RENDER_EXTERNAL_URL = https://your-app-name.onrender.com
ENABLE_AUTO_SCAN = true
ENABLE_ANIMATIONS = true
DEFAULT_SCAN_INTERVAL = 10
LOG_LEVEL = INFO
DEBUG = false
```

## Files Structure (Ready):
```
project/
├── main.py              # Flask app (Fixed)
├── bot.py               # Bot handlers (Working)
├── requirements.txt     # Dependencies (Ready)
├── render.yaml          # Auto-deploy config
├── Procfile            # Alternative config
├── handlers/           # Command handlers
│   ├── commands.py
│   ├── callbacks.py
│   └── messages.py
└── utils/              # Bot utilities
    ├── animations.py
    ├── auto_scanner.py
    ├── pdf_generator.py
    ├── telegram_storage.py
    └── toolkit.py
```

## Deployment Steps:
1. Push files to GitHub repository
2. Create web service on Render.com
3. Set build and start commands above
4. Add environment variables
5. Deploy and wait for completion
6. Visit: `https://your-app.onrender.com/set_webhook`

## Post-Deploy Testing:
1. Bot URL: `https://your-app.onrender.com/`
2. Webhook setup: `https://your-app.onrender.com/set_webhook`
3. Health check: `https://your-app.onrender.com/health`
4. Telegram bot: Search your bot and send `/start`

Your bot will work perfectly on Render.com with proper webhook setup.