"""
Main Flask application for webhook-based Telegram bot deployment on Render.com
"""
import os
import logging
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from telegram import Update
from bot import create_bot, setup_webhook

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Initialize bot with proper async handling
bot, application = create_bot()

# Global thread pool for async operations
executor = ThreadPoolExecutor(max_workers=10)

# Initialize application in a thread-safe way
def initialize_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(application.initialize())
        logger.info("Bot application initialized successfully")
    except Exception as e:
        logger.error(f"Bot initialization error: {e}")
    finally:
        loop.close()

# Initialize bot on startup
init_thread = threading.Thread(target=initialize_bot)
init_thread.start()
init_thread.join()  # Wait for initialization to complete

# Get webhook URL
WEBHOOK_URL = os.getenv('RENDER_EXTERNAL_URL', 'https://your-app.onrender.com') + '/webhook'

@app.route('/')
def index():
    """Health check endpoint"""
    return "🤖 Telegram Automation Bot is running! | बॉट चालू है!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram updates"""
    try:
        update_data = request.get_json()
        if update_data:
            logger.info(f"Received webhook update")
            
            # Process update in thread pool
            def process_update():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    update = Update.de_json(update_data, bot)
                    loop.run_until_complete(application.process_update(update))
                    logger.info("Update processed successfully")
                except Exception as e:
                    logger.error(f"Update processing error: {e}")
                finally:
                    loop.close()
            
            # Submit to thread pool and don't wait for completion
            executor.submit(process_update)
            
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/set_webhook')
def set_webhook_endpoint():
    """Set up webhook for the bot"""
    try:
        webhook_url = WEBHOOK_URL
        logger.info(f"Setting webhook to: {webhook_url}")
        
        success = setup_webhook(webhook_url)
        if success:
            return jsonify({
                "status": "success",
                "message": "Webhook set successfully!",
                "webhook_url": webhook_url
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to set webhook"
            }), 500
    except Exception as e:
        logger.error(f"Set webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "bot_token": "configured" if os.getenv('BOT_TOKEN') else "missing",
        "webhook_url": WEBHOOK_URL,
        "timestamp": "healthy"
    })

# Auto scanner initialization
def start_auto_scanner():
    from utils.auto_scanner import AutoScanner
    auto_scanner = AutoScanner(bot)
    
    def scanner_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(auto_scanner.start_auto_scan())
        except Exception as e:
            logger.error(f"Auto scanner error: {e}")
        finally:
            loop.close()
    
    scanner_thread = threading.Thread(target=scanner_loop, daemon=True)
    scanner_thread.start()
    logger.info("Auto scanner started in background")

# Start auto scanner
start_auto_scanner()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Auto-setup webhook on startup if RENDER_EXTERNAL_URL is available
    if os.getenv('RENDER_EXTERNAL_URL'):
        try:
            setup_webhook(WEBHOOK_URL)
            logger.info(f"Auto-configured webhook: {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Auto webhook setup failed: {e}")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
