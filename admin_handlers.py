import uuid
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards import admin_keyboard, order_status_keyboard
from config import ADMIN_IDS, PRODUCT_CATEGORIES

def is_admin(user_id):
    """Check if user is admin"""
    return user_id in ADMIN_IDS

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("شما دسترسی به پنل مدیریت ندارید.")
        return
    
    message = """
🔧 پنل مدیریت

خوش آمدید! از منوی زیر برای مدیریت فروشگاه استفاده کنید:
    """
    
    await update.message.reply_text(message, reply_markup=admin_keyboard())

async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start adding product process"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("شما دسترسی به این بخش ندارید.")
        return
    
    context.user_data['adding_product'] = True
    context.user_data['product_data'] = {}
    
    message = """
➕ افزودن محصول جدید

لطفاً نام محصول را وارد کنید:
    """
    
    await update.message.reply_text(message)

async def sales_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show sales statistics"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("شما دسترسی به این بخش ندارید.")
        return
    
    orders = db.get_orders()
    total_orders = len(orders)
    total_revenue = sum(order['price'] for order in orders.values() if order['status'] == 'confirmed')
    
    pending_orders = len([o for o in orders.values() if o['status'] == 'pending'])
    confirmed_orders = len([o for o in orders.values() if o['status'] == 'confirmed'])
    
    message = f"""
📊 آمار فروش

📋 کل سفارشات: {total_orders}
⏳ در انتظار تأیید: {pending_orders}
✅ تأیید شده: {confirmed_orders}
💰 کل درآمد: {total_revenue:,} تومان

📈 آمار به‌روز شده
    """
    
    await update.message.reply_text(message)

async def manage_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show orders management"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("شما دسترسی به این بخش ندارید.")
        return
    
    orders = db.get_orders()
    pending_orders = {k: v for k, v in orders.items() if v['status'] == 'pending'}
    
    if pending_orders:
        message = "📋 سفارشات در انتظار تأیید:\n\n"
        
        for order_id, order in list(pending_orders.items())[:5]:  # Show first 5 orders
            user = db.get_user(order['user_id'])
            user_name = user['first_name'] if user else 'نامشخص'
            
            message += f"🆔 {order_id}\n"
            message += f"👤 {user_name}\n"
            message += f"📦 {order['product_name']}\n"
            message += f"💰 {order['price']:,} تومان\n"
            message += f"💳 {order['payment_method']}\n\n"
        
        await update.message.reply_text(message)
        
        # Send management options for first order
        if pending_orders:
            first_order_id = list(pending_orders.keys())[0]
            await update.message.reply_text(
                f"مدیریت سفارش {first_order_id}:",
                reply_markup=order_status_keyboard(first_order_id)
            )
    else:
        await update.message.reply_text("سفارش جدیدی در انتظار تأیید نیست.")

async def manage_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show users management"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("شما دسترسی به این بخش ندارید.")
        return
    
    users = db.data['users']
    total_users = len(users)
    
    message = f"""
👥 مدیریت کاربران

📊 کل کاربران: {total_users}

آخرین کاربران:
    """
    
    # Show last 5 users
    recent_users = list(users.items())[-5:]
    for user_id, user_data in recent_users:
        message += f"\n👤 {user_data['first_name']} (@{user_data.get('username', 'بدون نام کاربری')})"
    
    await update.message.reply_text(message)

async def handle_order_status_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle order status changes"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await query.edit_message_text("شما دسترسی به این بخش ندارید.")
        return
    
    data_parts = query.data.split('_')
    action = data_parts[0]
    order_id = data_parts[2]
    
    status_map = {
        'confirm': 'confirmed',
        'cancel': 'cancelled',
        'shipped': 'shipped'
    }
    
    new_status = status_map.get(action)
    if new_status and db.update_order_status(order_id, new_status):
        status_text = {
            'confirmed': 'تأیید شد',
            'cancelled': 'لغو شد',
            'shipped': 'ارسال شد'
        }[new_status]
        
        await query.edit_message_text(f"✅ وضعیت سفارش {order_id} به '{status_text}' تغییر یافت.")
        
        # Notify customer
        order = db.data['orders'].get(order_id)
        if order:
            try:
                customer_message = f"""
📦 به‌روزرسانی سفارش

🆔 شماره سفارش: {order_id}
📋 وضعیت جدید: {status_text}
📦 محصول: {order['product_name']}

{"✅ سفارش شما تأیید شد!" if new_status == 'confirmed' else 
 "📦 سفارش شما ارسال شد!" if new_status == 'shipped' else 
 "❌ متأسفانه سفارش شما لغو شد."}
                """
                await context.bot.send_message(order['user_id'], customer_message)
            except:
                pass
    else:
        await query.edit_message_text("خطا در تغییر وضعیت سفارش.")

async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin messages"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if not is_admin(user_id):
        return
    
    if text == "➕ افزودن محصول":
        await add_product_start(update, context)
    elif text == "📊 آمار فروش":
        await sales_stats(update, context)
    elif text == "📋 مدیریت سفارشات":
        await manage_orders(update, context)
    elif text == "👥 مدیریت کاربران":
        await manage_users(update, context)
    elif text == "🔙 بازگشت به منوی اصلی":
        from handlers import start
        await start(update, context)
    elif context.user_data.get('adding_product'):
        await handle_product_addition(update, context)

async def handle_product_addition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle product addition process"""
    text = update.message.text
    product_data = context.user_data.get('product_data', {})
    
    if 'name' not in product_data:
        product_data['name'] = text
        context.user_data['product_data'] = product_data
        await update.message.reply_text("✅ نام محصول ثبت شد.\n\nحالا توضیحات محصول را وارد کنید:")
    
    elif 'description' not in product_data:
        product_data['description'] = text
        context.user_data['product_data'] = product_data
        await update.message.reply_text("✅ توضیحات ثبت شد.\n\nحالا قیمت محصول را به تومان وارد کنید:")
    
    elif 'price' not in product_data:
        try:
            price = int(text.replace(',', ''))
            product_data['price'] = price
            context.user_data['product_data'] = product_data
            
            categories_text = "\n".join([f"{k}: {v}" for k, v in PRODUCT_CATEGORIES.items()])
            await update.message.reply_text(f"✅ قیمت ثبت شد.\n\nدسته‌بندی محصول را انتخاب کنید:\n\n{categories_text}")
        except ValueError:
            await update.message.reply_text("❌ قیمت نامعتبر است. لطفاً عدد وارد کنید:")
    
    elif 'category' not in product_data:
        if text in PRODUCT_CATEGORIES:
            product_data['category'] = text
            
            # Generate product ID and save
            product_id = str(uuid.uuid4())[:8]
            db.add_product(
                product_id,
                product_data['name'],
                product_data['description'],
                product_data['price'],
                product_data['category']
            )
            
            await update.message.reply_text(
                f"✅ محصول با موفقیت اضافه شد!\n\n"
                f"🆔 شناسه: {product_id}\n"
                f"📦 نام: {product_data['name']}\n"
                f"💰 قیمت: {product_data['price']:,} تومان\n"
                f"🏷️ دسته: {PRODUCT_CATEGORIES[product_data['category']]}"
            )
            
            # Clear user data
            context.user_data['adding_product'] = False
            context.user_data['product_data'] = {}
        else:
            categories_text = "\n".join([f"{k}: {v}" for k, v in PRODUCT_CATEGORIES.items()])
            await update.message.reply_text(f"❌ دسته‌بندی نامعتبر است. لطفاً یکی از موارد زیر را انتخاب کنید:\n\n{categories_text}")

