# Crypto Trading Bot
یک سیستم معاملاتی خودکار برای ارزهای دیجیتال.

## ویژگی‌ها
- جمع‌آوری داده‌های بلادرنگ از صرافی‌های مختلف.
- تحلیل داده‌ها و پیش‌بینی روند بازار.
- اجرای معاملات خودکار.

## ساختار پروژه
```
crypto-trading-bot/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
├── scripts/
│   ├── store_data.py
│   ├── trading_bot.py
├── config/
│   └── settings.py
└── docs/
    └── setup.md
```

## نحوه استفاده
۱. مخزن را کلون کنید:
   ```bash
   git clone https://github.com/behicof/crypto-trading-bot.git
   cd crypto-trading-bot
   ```

۲. وابستگی‌ها را نصب کنید:
   ```bash
   pip install -r requirements.txt
   ```

۳. اسکریپت‌ها را اجرا کنید:
   ```bash
   python scripts/store_data.py
   python scripts/trading_bot.py
   ```