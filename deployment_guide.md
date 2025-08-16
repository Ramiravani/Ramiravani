# راهنمای کامل استقرار ربات تلگرام

## مقدمه

این راهنمای جامع برای استقرار ربات تلگرام فروش منابع دیجیتال بر روی سرویس‌های میزبانی ابری مختلف تهیه شده است. در ادامه، روش‌های مختلف استقرار و تنظیمات لازم را بررسی خواهیم کرد.

## گزینه‌های استقرار

### 1. Render (پیشنهادی)
Render یکی از بهترین گزینه‌های رایگان برای استقرار اپلیکیشن‌های Python است.

**مزایا:**
- رایگان تا 750 ساعت در ماه
- پشتیبانی کامل از Python و Flask
- تنظیمات آسان webhook
- SSL رایگان

**مراحل استقرار:**

1. **ایجاد حساب کاربری**
   - به [render.com](https://render.com) مراجعه کنید
   - حساب کاربری ایجاد کنید

2. **آپلود فایل‌ها**
   - فایل‌های ربات را در یک repository در GitHub قرار دهید
   - یا از طریق رابط وب Render آپلود کنید

3. **تنظیمات سرویس**
   - نوع سرویس: Web Service
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python webhook_server.py`

4. **متغیرهای محیطی**
   - `BOT_TOKEN`: توکن ربات تلگرام شما
   - `PORT`: 5000 (پیش‌فرض)

### 2. Railway
Railway سرویس میزبانی مدرن و قدرتمند است.

**مزایا:**
- رایگان تا 500 ساعت در ماه
- استقرار خودکار از GitHub
- پشتیبانی عالی از Python

**مراحل استقرار:**

1. **ایجاد حساب**
   - به [railway.app](https://railway.app) مراجعه کنید
   - با GitHub وارد شوید

2. **ایجاد پروژه جدید**
   - "New Project" را انتخاب کنید
   - "Deploy from GitHub repo" را انتخاب کنید

3. **تنظیمات**
   - متغیر `BOT_TOKEN` را اضافه کنید
   - Railway به طور خودکار `PORT` را تنظیم می‌کند

### 3. Heroku
Heroku یکی از قدیمی‌ترین و معتبرترین سرویس‌های میزبانی ابری است.

**توجه:** Heroku دیگر پلن رایگان ندارد، اما همچنان گزینه مناسبی برای استقرار حرفه‌ای است.

**مراحل استقرار:**

1. **نصب Heroku CLI**
   ```bash
   # در سیستم‌های Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **ورود به حساب**
   ```bash
   heroku login
   ```

3. **ایجاد اپلیکیشن**
   ```bash
   heroku create your-bot-name
   ```

4. **تنظیم متغیرها**
   ```bash
   heroku config:set BOT_TOKEN=YOUR_BOT_TOKEN
   ```

5. **استقرار**
   ```bash
   git push heroku main
   ```

## تنظیم Webhook

پس از استقرار موفق ربات، باید webhook را تنظیم کنید:

### روش 1: از طریق مرورگر
به آدرس زیر مراجعه کنید:
```
https://YOUR_APP_URL/set_webhook?url=https://YOUR_APP_URL
```

### روش 2: از طریق Telegram API
```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://YOUR_APP_URL/webhook"}'
```

## نکات مهم

### امنیت
- هرگز توکن ربات خود را در کد قرار ندهید
- همیشه از متغیرهای محیطی استفاده کنید
- فایل `.env` را در `.gitignore` قرار دهید

### نظارت
- لاگ‌های اپلیکیشن را بررسی کنید
- از سرویس‌های monitoring استفاده کنید
- پاسخ‌دهی ربات را به طور منظم تست کنید

### بک‌آپ
- به طور منظم از پایگاه داده JSON بک‌آپ تهیه کنید
- کدهای خود را در Git نگهداری کنید


