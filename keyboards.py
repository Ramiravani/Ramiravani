from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import PRODUCT_CATEGORIES, PAYMENT_METHODS

def main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [KeyboardButton("🛍️ مشاهده محصولات"), KeyboardButton("🛒 سبد خرید")],
        [KeyboardButton("📋 سفارشات من"), KeyboardButton("ℹ️ درباره ما")],
        [KeyboardButton("📞 تماس با ما")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def categories_keyboard():
    """Product categories keyboard"""
    keyboard = []
    for category_id, category_name in PRODUCT_CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(category_name, callback_data=f"category_{category_id}")])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

def products_keyboard(products, category=None):
    """Products list keyboard"""
    keyboard = []
    for product_id, product in products.items():
        keyboard.append([InlineKeyboardButton(
            f"{product['name']} - {product['price']:,} تومان",
            callback_data=f"product_{product_id}"
        )])
    
    if category:
        keyboard.append([InlineKeyboardButton("🔙 بازگشت به دسته‌بندی‌ها", callback_data="back_to_categories")])
    else:
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(keyboard)

def product_detail_keyboard(product_id, category=None):
    """Product detail keyboard"""
    keyboard = [
        [InlineKeyboardButton("🛒 افزودن به سبد خرید", callback_data=f"add_to_cart_{product_id}")],
        [InlineKeyboardButton("💳 خرید فوری", callback_data=f"buy_now_{product_id}")]
    ]
    
    if category:
        keyboard.append([InlineKeyboardButton("🔙 بازگشت به محصولات", callback_data=f"category_{category}")])
    else:
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(keyboard)

def payment_methods_keyboard(product_id):
    """Payment methods keyboard"""
    keyboard = []
    for method_id, method_name in PAYMENT_METHODS.items():
        keyboard.append([InlineKeyboardButton(
            method_name,
            callback_data=f"payment_{method_id}_{product_id}"
        )])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data=f"product_{product_id}")])
    return InlineKeyboardMarkup(keyboard)

def admin_keyboard():
    """Admin panel keyboard"""
    keyboard = [
        [KeyboardButton("➕ افزودن محصول"), KeyboardButton("📊 آمار فروش")],
        [KeyboardButton("📋 مدیریت سفارشات"), KeyboardButton("👥 مدیریت کاربران")],
        [KeyboardButton("🔙 بازگشت به منوی اصلی")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def order_status_keyboard(order_id):
    """Order status management keyboard"""
    keyboard = [
        [InlineKeyboardButton("✅ تأیید", callback_data=f"confirm_order_{order_id}")],
        [InlineKeyboardButton("❌ لغو", callback_data=f"cancel_order_{order_id}")],
        [InlineKeyboardButton("📦 ارسال شده", callback_data=f"shipped_order_{order_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

