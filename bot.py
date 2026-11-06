import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# قراءة التوكن من إعدادات الاستضافة بأمان
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# قائمة المنتجات (رابط الصورة حالياً تجريبي، يمكنك تغييره لاحقاً)
PRODUCTS = {
    "1": {"name": "منتج تجريبي 1", "price": "10$", "desc": "وصف المنتج الأول", "image": "https://via.placeholder.com/300"},
    "2": {"name": "منتج تجريبي 2", "price": "20$", "desc": "وصف المنتج الثاني", "image": "https://via.placeholder.com/300"},
    "3": {"name": "منتج تجريبي 3", "price": "30$", "desc": "وصف المنتج الثالث", "image": "https://via.placeholder.com/300"},
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في متجرنا! أرسل كلمة 'منتجات' لعرض القائمة.")

@bot.message_handler(func=lambda message: message.text == "منتجات")
def show_products(message):
    markup = InlineKeyboardMarkup()
    for pid, info in PRODUCTS.items():
        markup.add(InlineKeyboardButton(f"{info['name']} - {info['price']}", callback_data=f"prod_{pid}"))
    bot.send_message(message.chat.id, "اختر منتجاً:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def show_product_details(call):
    pid = call.data.split('_')[1]
    product = PRODUCTS.get(pid)
    if product:
        text = f"*{product['name']}*\nالسعر: {product['price']}\nالوصف: {product['desc']}"
        bot.answer_callback_query(call.id)
        # إرسال الصورة مع النص
        bot.send_photo(
            chat_id=call.message.chat.id, 
            photo=product.get('image'), 
            caption=text, 
            parse_mode='Markdown'
        )

print("البوت يعمل الآن...")
bot.polling(none_stop=True)
