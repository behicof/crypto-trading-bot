import ccxt
import time

# تنظیمات اولیه
API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
PAIR = 'BTC/USDT'  # جفت‌ارز مورد معامله
TRADE_AMOUNT = 0.001  # مقدار معامله
TARGET_PROFIT = 0.01  # هدف سود (۱٪)
STOP_LOSS = 0.01  # حد ضرر (۱٪)

# اتصال به صرافی (Binance)
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True
})

# تابع جمع‌آوری داده‌های بلادرنگ
def get_market_data(pair):
    ticker = exchange.fetch_ticker(pair)
    return ticker['last']

# تابع اجرای سفارش خرید
def place_buy_order(pair, amount):
    order = exchange.create_market_buy_order(pair, amount)
    print(f"Buy Order Placed: {order}")
    return order

# تابع اجرای سفارش فروش
def place_sell_order(pair, amount):
    order = exchange.create_market_sell_order(pair, amount)
    print(f"Sell Order Placed: {order}")
    return order

# اجرای استراتژی معاملاتی
def trade():
    print("Starting trading bot...")
    buy_price = get_market_data(PAIR)
    print(f"Initial Buy Price: {buy_price}")
    
    # اجرای سفارش خرید
    place_buy_order(PAIR, TRADE_AMOUNT)

    while True:
        current_price = get_market_data(PAIR)
        print(f"Current Price: {current_price}")

        # بررسی هدف سود
        if current_price >= buy_price * (1 + TARGET_PROFIT):
            print("Target profit reached. Selling...")
            place_sell_order(PAIR, TRADE_AMOUNT)
            break

        # بررسی حد ضرر
        if current_price <= buy_price * (1 - STOP_LOSS):
            print("Stop loss triggered. Selling...")
            place_sell_order(PAIR, TRADE_AMOUNT)
            break

        time.sleep(5)  # وقفه بین درخواست‌ها (۵ ثانیه)

# اجرای برنامه
if __name__ == "__main__":
    trade()