import uuid
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards import *
from config import ADMIN_IDS, PRODUCT_CATEGORIES

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    
    # Add user to database
    db.add_user(user.id, user.username, user.first_name)
    
    welcome_message = f"""
🌟 سلام {user.first_name}!

به ربات فروشگاه منابع دیجیتال خوش آمدید!

🛍️ در اینجا می‌توانید:
• محصولات دیجیتال با کیفیت را مشاهده کنید
• سفارش دهید و پرداخت کنید
• سفارشات خود را پیگیری کنید

برای شروع، از منوی زیر استفاده کنید:
    """
    
    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product categories"""
    message = "🛍️ دسته‌بندی محصولات:\n\nلطفاً دسته مورد نظر خود را انتخاب کنید:"
    
    if update.message:
        await update.message.reply_text(message, reply_markup=categories_keyboard())
    else:
        await update.callback_query.edit_message_text(message, reply_markup=categories_keyboard())

async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products in a category"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[1]
    category_name = PRODUCT_CATEGORIES.get(category, 'نامشخص')
    
    products = db.get_products(category)
    
    if products:
        message = f"📦 محصولات دسته {category_name}:\n\nمحصول مورد نظر خود را انتخاب کنید:"
        await query.edit_message_text(message, reply_markup=products_keyboard(products, category))
    else:
        message = f"متأسفانه در دسته {category_name} محصولی موجود نیست."
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_categories")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product details"""
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.split('_')[1]
    product = db.get_product(product_id)
    
    if product:
        message = f"""
📦 {product['name']}

📝 توضیحات:
{product['description']}

💰 قیمت: {product['price']:,} تومان

🏷️ دسته‌بندی: {PRODUCT_CATEGORIES.get(product['category'], 'نامشخص')}
        """
        
        await query.edit_message_text(
            message, 
            reply_markup=product_detail_keyboard(product_id, product['category'])
        )
    else:
        await query.edit_message_text("محصول مورد نظر یافت نشد.")

async def buy_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle buy now action"""
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.split('_')[2]
    product = db.get_product(product_id)
    
    if product:
        message = f"""
🛒 خرید فوری: {product['name']}
💰 قیمت: {product['price']:,} تومان

لطفاً روش پرداخت خود را انتخاب کنید:
        """
        await query.edit_message_text(message, reply_markup=payment_methods_keyboard(product_id))
    else:
        await query.edit_message_text("محصول مورد نظر یافت نشد.")

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process payment"""
    query = update.callback_query
    await query.answer()
    
    data_parts = query.data.split('_')
    payment_method = data_parts[1]
    product_id = data_parts[2]
    
    product = db.get_product(product_id)
    user_id = update.effective_user.id
    
    if product:
        # Generate order ID
        order_id = str(uuid.uuid4())[:8]
        
        # Add order to database
        db.add_order(order_id, user_id, product_id, payment_method)
        
        payment_method_name = PAYMENT_METHODS.get(payment_method, 'نامشخص')
        
        message = f"""
✅ سفارش شما ثبت شد!

🆔 شماره سفارش: {order_id}
📦 محصول: {product['name']}
💰 مبلغ: {product['price']:,} تومان
💳 روش پرداخت: {payment_method_name}

📞 برای تکمیل پرداخت، لطفاً با پشتیبانی تماس بگیرید.
وضعیت سفارش شما به‌زودی به‌روزرسانی خواهد شد.

شماره سفارش خود را یادداشت کنید.
        """
        
        # Notify admins
        for admin_id in ADMIN_IDS:
            try:
                admin_message = f"""
🔔 سفارش جدید!

🆔 شماره سفارش: {order_id}
👤 کاربر: {update.effective_user.first_name} (@{update.effective_user.username})
📦 محصول: {product['name']}
💰 مبلغ: {product['price']:,} تومان
💳 روش پرداخت: {payment_method_name}
                """
                await context.bot.send_message(admin_id, admin_message)
            except:
                pass
        
        keyboard = [[InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_main")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_text("خطا در ثبت سفارش. لطفاً دوباره تلاش کنید.")

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user orders"""
    user_id = update.effective_user.id
    orders = db.get_orders(user_id)
    
    if orders:
        message = "📋 سفارشات شما:\n\n"
        for order_id, order in orders.items():
            status_emoji = {
                'pending': '⏳',
                'confirmed': '✅',
                'shipped': '📦',
                'cancelled': '❌'
            }.get(order['status'], '❓')
            
            message += f"{status_emoji} {order_id}\n"
            message += f"📦 {order['product_name']}\n"
            message += f"💰 {order['price']:,} تومان\n"
            message += f"📅 {order['created_at'][:10]}\n\n"
    else:
        message = "شما هنوز سفارشی ندارید.\n\n🛍️ برای مشاهده محصولات از منو استفاده کنید."
    
    await update.message.reply_text(message)

async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about us information"""
    message = """
ℹ️ درباره ما

🌟 ما ارائه‌دهنده منابع دیجیتال با کیفیت هستیم.

📚 محصولات ما شامل:
• دوره‌های آموزشی
• کتاب‌های الکترونیکی
• نرم‌افزارها
• قالب‌ها و منابع طراحی

🎯 هدف ما ارائه بهترین کیفیت با قیمت مناسب است.

📞 برای سوالات خود با ما در تماس باشید.
    """
    await update.message.reply_text(message)

async def contact_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact information"""
    message = """
📞 تماس با ما

💬 برای پشتیبانی و سوالات خود می‌توانید:

📧 ایمیل: support@example.com
📱 تلگرام: @support_username
⏰ ساعات کاری: 9 صبح تا 6 عصر

🔔 پاسخگویی در کمترین زمان ممکن
    """
    await update.message.reply_text(message)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    
    if query.data.startswith('category_'):
        await show_category_products(update, context)
    elif query.data.startswith('product_'):
        await show_product_detail(update, context)
    elif query.data.startswith('buy_now_'):
        await buy_now(update, context)
    elif query.data.startswith('payment_'):
        await process_payment(update, context)
    elif query.data == 'back_to_main':
        await query.edit_message_text("منوی اصلی:", reply_markup=InlineKeyboardMarkup([]))
    elif query.data == 'back_to_categories':
        await show_products(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    text = update.message.text
    
    if text == "🛍️ مشاهده محصولات":
        await show_products(update, context)
    elif text == "📋 سفارشات من":
        await my_orders(update, context)
    elif text == "ℹ️ درباره ما":
        await about_us(update, context)
    elif text == "📞 تماس با ما":
        await contact_us(update, context)
    elif text == "🛒 سبد خرید":
        await update.message.reply_text("قابلیت سبد خرید به‌زودی اضافه خواهد شد.")
    else:
        await update.message.reply_text("لطفاً از منوی موجود استفاده کنید.")

