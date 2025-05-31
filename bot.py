"""
Main bot initialization and setup
"""
import os
import asyncio
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Bot
from config import Config
from handlers.commands import CommandHandlers
from handlers.callbacks import CallbackHandlers
from handlers.messages import MessageHandlers
from utils.auto_scanner import AutoScanner

logger = logging.getLogger(__name__)

def create_bot():
    """Create and configure the Telegram bot"""
    # Get bot token
    bot_token = os.getenv('BOT_TOKEN', '7934979055:AAFGcVsNbhYh6j3RpLiGbjIHmu1Zx-mFiwc')
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Initialize handlers
    command_handlers = CommandHandlers()
    callback_handlers = CallbackHandlers()
    message_handlers = MessageHandlers()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", command_handlers.start))
    application.add_handler(CommandHandler("help", command_handlers.help_command))
    application.add_handler(CommandHandler("todo", command_handlers.todo_menu))
    application.add_handler(CommandHandler("pdf", command_handlers.pdf_menu))
    application.add_handler(CommandHandler("scan", command_handlers.scan_menu))
    application.add_handler(CommandHandler("toolkit", command_handlers.toolkit_menu))
    application.add_handler(CommandHandler("storage", command_handlers.storage_info))
    
    # Add callback handlers
    application.add_handler(CallbackQueryHandler(callback_handlers.handle_callback))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_text))
    application.add_handler(MessageHandler(filters.Document.ALL, message_handlers.handle_document))
    
    # Auto scanner will be started separately to avoid async issues during startup
    
    bot = application.bot
    return bot, application

def setup_webhook(webhook_url):
    """Setup webhook for the bot"""
    try:
        bot_token = os.getenv('BOT_TOKEN', '7934979055:AAFGcVsNbhYh6j3RpLiGbjIHmu1Zx-mFiwc')
        
        import requests
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        data = {
            'url': webhook_url,
            'allowed_updates': ['message', 'callback_query']
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        logger.info(f"Webhook setup response: {result}")
        return result.get('ok', False)
        
    except Exception as e:
        logger.error(f"Webhook setup error: {e}")
        return False
