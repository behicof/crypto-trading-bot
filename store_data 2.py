import ccxt
import psycopg2
from datetime import datetime

# تنظیمات اتصال به پایگاه داده
DB_NAME = 'crypto_db'
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'

# تنظیمات صرافی
exchange = ccxt.binance({
    'rateLimit': True,
    'enableRateLimit': True
})

# تابع اتصال به پایگاه داده
def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# تابع ذخیره داده در پایگاه داده
def store_data(pair, price, timestamp):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO market_data (pair, price, timestamp)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (pair, price, timestamp))
    conn.commit()
    cursor.close()
    conn.close()

# تابع جمع‌آوری داده از صرافی
def collect_and_store_data(pair):
    ticker = exchange.fetch_ticker(pair)
    price = ticker['last']
    timestamp = datetime.now()
    print(f"Storing data: {pair} - {price} - {timestamp}")
    store_data(pair, price, timestamp)

# اجرای برنامه
if __name__ == "__main__":
    pair = 'BTC/USDT'
    collect_and_store_data(pair)