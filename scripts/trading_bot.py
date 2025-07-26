import ccxt
import time
import random
import logging
import sys
import os

# اضافه کردن مسیر config به sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))

try:
    from settings import EXCHANGE_CONFIG, TRADING_CONFIG, SIMULATION_MODE, LOG_CONFIG
except ImportError:
    # تنظیمات پیش‌فرض در صورت عدم وجود فایل config
    EXCHANGE_CONFIG = {
        'api_key': 'YOUR_API_KEY',
        'secret_key': 'YOUR_SECRET_KEY',
        'sandbox': True,
        'testnet': True,
    }
    TRADING_CONFIG = {
        'pair': 'BTC/USDT',
        'trade_amount': 0.001,
        'target_profit': 0.01,
        'stop_loss': 0.01,
        'check_interval': 5,
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

# کلاس شبیه‌سازی برای تست
class SimulatedExchange:
    def __init__(self, initial_price=50000):
        self.current_price = initial_price
        self.price_volatility = 0.001  # تغییرات قیمت
        
    def fetch_ticker(self, pair):
        # شبیه‌سازی تغییرات قیمت
        change = random.uniform(-self.price_volatility, self.price_volatility)
        self.current_price *= (1 + change)
        return {'last': self.current_price}
    
    def create_market_buy_order(self, pair, amount):
        logger.info(f"[SIMULATION] Buy Order: {amount} {pair} at ${self.current_price:.2f}")
        return {'id': f'sim_buy_{int(time.time())}', 'amount': amount, 'price': self.current_price}
    
    def create_market_sell_order(self, pair, amount):
        logger.info(f"[SIMULATION] Sell Order: {amount} {pair} at ${self.current_price:.2f}")
        return {'id': f'sim_sell_{int(time.time())}', 'amount': amount, 'price': self.current_price}

# انتخاب نوع صرافی بر اساس حالت
if SIMULATION_MODE:
    logger.info("Starting in SIMULATION mode")
    exchange = SimulatedExchange()
else:
    # اتصال به صرافی واقعی (Binance)
    try:
        exchange = ccxt.binance({
            'apiKey': EXCHANGE_CONFIG['api_key'],
            'secret': EXCHANGE_CONFIG['secret_key'],
            'sandbox': EXCHANGE_CONFIG.get('sandbox', True),
            'enableRateLimit': True
        })
        if EXCHANGE_CONFIG.get('testnet', True):
            exchange.set_sandbox_mode(True)
        logger.info("Connected to Binance exchange")
    except Exception as e:
        logger.error(f"Failed to connect to exchange: {e}")
        logger.info("Falling back to simulation mode")
        exchange = SimulatedExchange()

# تابع جمع‌آوری داده‌های بلادرنگ
def get_market_data(pair):
    try:
        ticker = exchange.fetch_ticker(pair)
        return ticker['last']
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return None

# تابع اجرای سفارش خرید
def place_buy_order(pair, amount):
    try:
        order = exchange.create_market_buy_order(pair, amount)
        logger.info(f"Buy Order Placed: {order}")
        return order
    except Exception as e:
        logger.error(f"Error placing buy order: {e}")
        return None

# تابع اجرای سفارش فروش
def place_sell_order(pair, amount):
    try:
        order = exchange.create_market_sell_order(pair, amount)
        logger.info(f"Sell Order Placed: {order}")
        return order
    except Exception as e:
        logger.error(f"Error placing sell order: {e}")
        return None

# اجرای استراتژی معاملاتی
def trade():
    pair = TRADING_CONFIG['pair']
    trade_amount = TRADING_CONFIG['trade_amount']
    target_profit = TRADING_CONFIG['target_profit']
    stop_loss = TRADING_CONFIG['stop_loss']
    check_interval = TRADING_CONFIG['check_interval']
    
    logger.info("Starting trading bot...")
    logger.info(f"Trading pair: {pair}")
    logger.info(f"Trade amount: {trade_amount}")
    logger.info(f"Target profit: {target_profit*100}%")
    logger.info(f"Stop loss: {stop_loss*100}%")
    
    # دریافت قیمت اولیه
    buy_price = get_market_data(pair)
    if buy_price is None:
        logger.error("Cannot get initial market data. Exiting...")
        return
        
    logger.info(f"Initial Buy Price: ${buy_price:.2f}")
    
    # اجرای سفارش خرید
    buy_order = place_buy_order(pair, trade_amount)
    if buy_order is None:
        logger.error("Failed to place buy order. Exiting...")
        return

    iteration = 0
    max_iterations = 20  # حداکثر تعداد تکرار برای شبیه‌سازی
    
    while iteration < max_iterations:
        iteration += 1
        current_price = get_market_data(pair)
        
        if current_price is None:
            logger.error("Cannot get current market data. Continuing...")
            time.sleep(check_interval)
            continue
            
        logger.info(f"[{iteration}] Current Price: ${current_price:.2f}")
        
        profit_percentage = ((current_price - buy_price) / buy_price) * 100
        logger.info(f"[{iteration}] Current Profit/Loss: {profit_percentage:.2f}%")

        # بررسی هدف سود
        if current_price >= buy_price * (1 + target_profit):
            logger.info("🎯 Target profit reached. Selling...")
            sell_order = place_sell_order(pair, trade_amount)
            if sell_order:
                profit = (current_price - buy_price) * trade_amount
                logger.info(f"✅ Trade completed successfully! Profit: ${profit:.2f}")
            break

        # بررسی حد ضرر
        if current_price <= buy_price * (1 - stop_loss):
            logger.info("🛑 Stop loss triggered. Selling...")
            sell_order = place_sell_order(pair, trade_amount)
            if sell_order:
                loss = (buy_price - current_price) * trade_amount
                logger.info(f"❌ Trade stopped with loss: ${loss:.2f}")
            break

        time.sleep(check_interval)
    
    if iteration >= max_iterations:
        logger.info("🔄 Maximum iterations reached. Ending simulation.")
        logger.info("In real trading, the bot would continue monitoring.")

# اجرای برنامه
if __name__ == "__main__":
    trade()