# تنظیمات پروژه معاملات کریپتو
import os

# تنظیمات صرافی
EXCHANGE_CONFIG = {
    'api_key': os.getenv('BINANCE_API_KEY', 'YOUR_API_KEY'),
    'secret_key': os.getenv('BINANCE_SECRET_KEY', 'YOUR_SECRET_KEY'),
    'sandbox': True,  # حالت آزمایشی
    'testnet': True,  # استفاده از testnet
}

# تنظیمات معاملات
TRADING_CONFIG = {
    'pair': os.getenv('TRADING_PAIR', 'BTC/USDT'),        # جفت‌ارز مورد معامله
    'trade_amount': float(os.getenv('TRADE_AMOUNT', '0.001')),     # مقدار معامله
    'target_profit': float(os.getenv('TARGET_PROFIT', '0.01')),     # هدف سود (۱٪)
    'stop_loss': float(os.getenv('STOP_LOSS', '0.01')),         # حد ضرر (۱٪)
    'check_interval': int(os.getenv('CHECK_INTERVAL', '5')),       # فاصله بررسی (ثانیه)
}

# تنظیمات پایگاه داده
DATABASE_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'crypto_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'enabled': os.getenv('DB_ENABLED', 'False').lower() == 'true',
}

# حالت شبیه‌سازی - می‌توان با متغیر محیطی تغییر داد
SIMULATION_MODE = os.getenv('FORCE_REAL_MODE', '0') != '1'

# تنظیمات لاگ
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(levelname)s - %(message)s',
}