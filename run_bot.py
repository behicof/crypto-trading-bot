#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات معاملات کریپتو - نقطه ورود اصلی
Crypto Trading Bot - Main Entry Point

این اسکریپت نقطه ورود اصلی برای ربات معاملات کریپتو است
This script is the main entry point for the crypto trading bot
"""

import sys
import os
import argparse
import logging

# اضافه کردن مسیرهای لازم
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'scripts'))
sys.path.append(os.path.join(current_dir, 'config'))

def main():
    parser = argparse.ArgumentParser(
        description='ربات معاملات کریپتو / Crypto Trading Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / نمونه‌ها:
  python run_bot.py --mode trade          # اجرای ربات معاملاتی
  python run_bot.py --mode collect        # جمع‌آوری داده
  python run_bot.py --mode trade --real   # اجرای واقعی (نیاز به API)
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['trade', 'collect'], 
        default='trade',
        help='حالت اجرا: trade (معامله) یا collect (جمع‌آوری داده)'
    )
    
    parser.add_argument(
        '--real', 
        action='store_true',
        help='استفاده از API واقعی به جای شبیه‌سازی'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='نمایش جزئیات بیشتر'
    )
    
    args = parser.parse_args()
    
    # تنظیم سطح لاگ
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger(__name__)
    
    # تغییر تنظیمات بر اساس آرگومان‌ها
    if args.real:
        logger.warning("⚠️  Real mode selected - requires valid API credentials")
        os.environ['FORCE_REAL_MODE'] = '1'
    else:
        logger.info("🎮 Simulation mode - safe for testing")
    
    try:
        if args.mode == 'trade':
            logger.info("🚀 Starting Trading Bot...")
            from trading_bot import trade
            trade()
            
        elif args.mode == 'collect':
            logger.info("📊 Starting Data Collection...")
            from store_data import collect_and_store_data
            # اجرای جمع‌آوری داده برای چندین جفت ارز
            pairs = ['BTC/USDT', 'ETH/USDT']
            for pair in pairs:
                logger.info(f"Collecting data for {pair}")
                collect_and_store_data(pair, iterations=5)
                
    except KeyboardInterrupt:
        logger.info("\n⏹️  Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()