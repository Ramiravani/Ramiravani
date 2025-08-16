import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Admin user IDs (add your Telegram user ID here)
ADMIN_IDS = [6606774476]  # RAMI RAVANI

# Product categories
PRODUCT_CATEGORIES = {
    'digital': 'محصولات دیجیتال',
    'courses': 'دوره‌های آموزشی', 
    'ebooks': 'کتاب‌های الکترونیکی',
    'software': 'نرم‌افزار',
    'templates': 'قالب‌ها'
}

# Payment methods
PAYMENT_METHODS = {
    'card': 'پرداخت با کارت',
    'crypto': 'پرداخت با ارز دیجیتال',
    'bank': 'حواله بانکی'
}

# Database file
DATABASE_FILE = 'bot_database.json'

