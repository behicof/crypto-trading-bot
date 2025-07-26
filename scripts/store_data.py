import ccxt
import psycopg2
import logging
import random
import time
import sys
import os
from datetime import datetime

# اضافه کردن مسیر config به sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))

try:
    from settings import DATABASE_CONFIG, SIMULATION_MODE, LOG_CONFIG
except ImportError:
    # تنظیمات پیش‌فرض
    DATABASE_CONFIG = {
        'dbname': 'crypto_db',
        'user': 'postgres',
        'password': 'your_password',
        'host': 'localhost',
        'port': '5432',
        'enabled': False,
    }
    SIMULATION_MODE = True
    LOG_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
    }

# تنظیم لاگ
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['level']),
    format=LOG_CONFIG['format']
)
logger = logging.getLogger(__name__)

# کلاس شبیه‌سازی برای ذخیره داده
class SimulatedDatabase:
    def __init__(self):
        self.data = []
        logger.info("Using simulated database storage")
    
    def store_data(self, pair, price, timestamp):
        entry = {'pair': pair, 'price': price, 'timestamp': timestamp}
        self.data.append(entry)
        logger.info(f"[SIMULATION DB] Stored: {pair} - ${price:.2f} - {timestamp}")
        
    def get_recent_data(self, limit=5):
        return self.data[-limit:] if self.data else []

# کلاس شبیه‌سازی صرافی
class SimulatedExchange:
    def __init__(self, initial_price=50000):
        self.current_price = initial_price
        self.price_volatility = 0.002
        
    def fetch_ticker(self, pair):
        change = random.uniform(-self.price_volatility, self.price_volatility)
        self.current_price *= (1 + change)
        return {'last': self.current_price}

# انتخاب نوع ذخیره‌سازی
if DATABASE_CONFIG.get('enabled', False) and not SIMULATION_MODE:
    use_real_db = True
else:
    use_real_db = False
    simulated_db = SimulatedDatabase()

# انتخاب نوع صرافی
if SIMULATION_MODE:
    exchange = SimulatedExchange()
    logger.info("Using simulated exchange")
else:
    exchange = ccxt.binance({
        'rateLimit': True,
        'enableRateLimit': True
    })
    logger.info("Using real Binance exchange")

# تابع اتصال به پایگاه داده
def connect_db():
    if not use_real_db:
        return None
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG['dbname'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port']
        )
        logger.info("Connected to PostgreSQL database")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

# تابع ذخیره داده در پایگاه داده
def store_data(pair, price, timestamp):
    if use_real_db:
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                INSERT INTO market_data (pair, price, timestamp)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (pair, price, timestamp))
                conn.commit()
                cursor.close()
                conn.close()
                logger.info(f"Stored to database: {pair} - ${price:.2f} - {timestamp}")
            except Exception as e:
                logger.error(f"Error storing to database: {e}")
                conn.close()
        else:
            logger.warning("Database not available, using simulation")
            simulated_db.store_data(pair, price, timestamp)
    else:
        simulated_db.store_data(pair, price, timestamp)

# تابع جمع‌آوری داده از صرافی
def collect_and_store_data(pair, iterations=10):
    logger.info(f"Starting data collection for {pair}")
    
    for i in range(iterations):
        try:
            ticker = exchange.fetch_ticker(pair)
            price = ticker['last']
            timestamp = datetime.now()
            
            logger.info(f"[{i+1}/{iterations}] Collecting data: {pair} - ${price:.2f}")
            store_data(pair, price, timestamp)
            
            if i < iterations - 1:  # Don't sleep on last iteration
                time.sleep(2)  # فاصله بین جمع‌آوری داده‌ها
                
        except Exception as e:
            logger.error(f"Error collecting data for {pair}: {e}")
            time.sleep(2)
    
    logger.info(f"Data collection completed for {pair}")
    
    # نمایش آمار در حالت شبیه‌سازی
    if not use_real_db and hasattr(simulated_db, 'data'):
        recent_data = simulated_db.get_recent_data()
        if recent_data:
            logger.info("Recent data collected:")
            for entry in recent_data:
                logger.info(f"  {entry['pair']}: ${entry['price']:.2f} at {entry['timestamp']}")

# اجرای برنامه
if __name__ == "__main__":
    pairs = ['BTC/USDT', 'ETH/USDT']  # چندین جفت ارز برای تست
    
    for pair in pairs:
        logger.info(f"Processing {pair}...")
        collect_and_store_data(pair)
        if len(pairs) > 1:
            time.sleep(1)  # فاصله بین پردازش جفت‌های مختلف
    
    logger.info("All data collection tasks completed")