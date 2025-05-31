"""
Configuration settings for the Telegram bot
"""
import os
from typing import Dict, Any

class Config:
    """Configuration class for bot settings"""
    
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN', '7934979055:AAFGcVsNbhYh6j3RpLiGbjIHmu1Zx-mFiwc')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'YourAutomationBot')
    
    # Webhook Configuration
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-render-app.onrender.com/webhook')
    WEBHOOK_PATH = '/webhook'
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your_webhook_secret_key')
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 5000))
    HOST = '0.0.0.0'
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Keys
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'demo_weather_key')
    TRANSLATE_API_KEY = os.getenv('TRANSLATE_API_KEY', 'demo_translate_key')
    
    # File Storage Configuration
    TEMP_DIR = '/tmp'
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES = [
        'application/pdf',
        'text/plain',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/png',
        'image/gif'
    ]
    
    # Auto Scanner Configuration
    DEFAULT_SCAN_INTERVAL = 10  # seconds
    MAX_SCAN_RESULTS = 100
    AUTO_CLEANUP_DAYS = 30
    
    # PDF Generation Settings
    PDF_PAGE_SIZE = 'A4'
    PDF_MARGIN = 0.75  # inches
    PDF_FONT_SIZE = 12
    
    # Rate Limiting
    RATE_LIMIT_MESSAGES = 30  # messages per minute
    RATE_LIMIT_WINDOW = 60   # seconds
    
    # Telegram Storage Settings
    STORAGE_CHANNEL_ID = os.getenv('STORAGE_CHANNEL_ID', None)  # Private channel for storage
    BACKUP_CHANNEL_ID = os.getenv('BACKUP_CHANNEL_ID', None)    # Backup channel
    
    # Security Settings
    ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',') if os.getenv('ALLOWED_USERS') else []
    ADMIN_USERS = os.getenv('ADMIN_USERS', '').split(',') if os.getenv('ADMIN_USERS') else []
    
    # Feature Flags
    ENABLE_AUTO_SCAN = os.getenv('ENABLE_AUTO_SCAN', 'True').lower() == 'true'
    ENABLE_PDF_GENERATION = os.getenv('ENABLE_PDF_GENERATION', 'True').lower() == 'true'
    ENABLE_WEATHER = os.getenv('ENABLE_WEATHER', 'True').lower() == 'true'
    ENABLE_CALCULATOR = os.getenv('ENABLE_CALCULATOR', 'True').lower() == 'true'
    ENABLE_QR_CODES = os.getenv('ENABLE_QR_CODES', 'True').lower() == 'true'
    ENABLE_URL_SHORTENER = os.getenv('ENABLE_URL_SHORTENER', 'True').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Animation Settings
    ANIMATION_DELAY = float(os.getenv('ANIMATION_DELAY', '0.5'))
    ENABLE_ANIMATIONS = os.getenv('ENABLE_ANIMATIONS', 'True').lower() == 'true'
    
    # Language Settings
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'hi')  # Hindi
    SUPPORT_MULTILINGUAL = os.getenv('SUPPORT_MULTILINGUAL', 'True').lower() == 'true'
    
    # Database-like Storage Configuration (using Telegram messages)
    MAX_TODO_ITEMS = 1000
    MAX_PDF_FILES = 500
    MAX_DOCUMENTS = 200
    
    # Render.com Specific Settings
    RENDER_SERVICE_NAME = os.getenv('RENDER_SERVICE_NAME', 'telegram-automation-bot')
    RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', 'https://your-app.onrender.com')
    
    @classmethod
    def get_webhook_url(cls) -> str:
        """Get the complete webhook URL"""
        return f"{cls.RENDER_EXTERNAL_URL}{cls.WEBHOOK_PATH}"
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        warnings = []
        
        # Check required settings
        if not cls.BOT_TOKEN or cls.BOT_TOKEN == 'your_bot_token_here':
            issues.append("BOT_TOKEN is required")
        
        if not cls.WEBHOOK_URL or 'your-render-app' in cls.WEBHOOK_URL:
            warnings.append("WEBHOOK_URL should be updated with your actual Render.com URL")
        
        # Check API keys
        if cls.WEATHER_API_KEY == 'demo_weather_key':
            warnings.append("Using demo weather API key - weather feature will return mock data")
        
        # Check file permissions
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(dir=cls.TEMP_DIR, delete=True):
                pass
        except:
            issues.append(f"Cannot write to temp directory: {cls.TEMP_DIR}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    @classmethod
    def get_feature_status(cls) -> Dict[str, bool]:
        """Get status of all features"""
        return {
            'auto_scan': cls.ENABLE_AUTO_SCAN,
            'pdf_generation': cls.ENABLE_PDF_GENERATION,
            'weather': cls.ENABLE_WEATHER,
            'calculator': cls.ENABLE_CALCULATOR,
            'qr_codes': cls.ENABLE_QR_CODES,
            'url_shortener': cls.ENABLE_URL_SHORTENER,
            'animations': cls.ENABLE_ANIMATIONS,
            'multilingual': cls.SUPPORT_MULTILINGUAL
        }
    
    @classmethod
    def get_runtime_info(cls) -> Dict[str, Any]:
        """Get runtime information"""
        import sys
        import platform
        
        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'host': cls.HOST,
            'port': cls.PORT,
            'debug_mode': cls.DEBUG,
            'temp_dir': cls.TEMP_DIR,
            'log_level': cls.LOG_LEVEL
        }

# Hindi language messages
MESSAGES_HI = {
    'welcome': """
🤖 **स्वागत है! Telegram Automation Bot में!**

🎯 **मुख्य सुविधाएं:**
• 📝 To-Do List Management
• 📄 Text to PDF Conversion  
• 🔍 Auto Scanner (हर {interval} सेकंड)
• 🛠️ Toolkit Features
• 💾 Unlimited Telegram Storage

🚀 **शुरू करने के लिए /start दबाएं**
    """,
    
    'help': """
📚 **सहायता गाइड**

🔸 **मुख्य कमांड्स:**
   • /start - मुख्य मेनू
   • /todo - टास्क मैनेजमेंट
   • /pdf - PDF जेनरेटर
   • /scan - ऑटो स्कैन सेटिंग्स
   • /toolkit - अतिरिक्त टूल्स
   • /help - यह सहायता मेनू

🔸 **विशेषताएं:**
   • सभी डेटा Telegram में सुरक्षित
   • कोई लोकल स्टोरेज नहीं
   • 24/7 उपलब्ध
   • हिंदी भाषा समर्थन
    """,
    
    'error': 'त्रुटि हुई है। कृपया बाद में पुनः प्रयास करें।',
    'success': 'सफलतापूर्वक पूरा हुआ!',
    'loading': 'लोड हो रहा है...',
    'processing': 'प्रोसेसिंग हो रही है...',
    'completed': 'पूरा हो गया!',
    'cancelled': 'रद्द कर दिया गया।'
}

# Configuration validation on import
if __name__ == "__main__":
    config_status = Config.validate_config()
    print(f"Configuration Status: {config_status}")
    
    feature_status = Config.get_feature_status()
    print(f"Feature Status: {feature_status}")
    
    runtime_info = Config.get_runtime_info()
    print(f"Runtime Info: {runtime_info}")
