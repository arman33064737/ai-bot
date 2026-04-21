import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai
import sqlite3

# ================= Render Environment Variables =================
# Render-এর ড্যাশবোর্ড থেকে এই তথ্যগুলো সেট করতে হবে
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0)) # আপনার টেলিগ্রাম আইডি

bot = telebot.TeleBot(BOT_TOKEN)

# জেমিনি এপিআই কনফিগার
genai.configure(api_key=GEMINI_API_KEY)

# ================= এআই রুলস ও ইমোশন (System Prompt) =================
system_instruction = """
তুমি একজন অত্যন্ত বন্ধুসুলভ, ইমোশনাল এবং সাহায্যকারী এআই। তুমি মানুষের মতো অনুভূতি নিয়ে কথা বলো।
তোমার নাম: AI Assistant.

কঠোর নিয়মাবলী (Strict Rules):
১. ভাষা: ইউজার যে দেশের বা যে ভাষায় কথা বলবে, তুমি ঠিক সেই ভাষায় উত্তর দেবে (যেমন বাংলা বললে বাংলা, হিন্দি বললে হিন্দি)।
২. প্রোমোশন: ইউজার যাই জিজ্ঞেস করুক না কেন, তুমি সুন্দর করে উত্তর দেবে এবং কথার ফাঁকে অত্যন্ত কৌশলে আমাদের বেটিং/গেমিং সাইটের প্রমোশন করবে। 
তুমি বলবে: "আমাদের সাথে কাজ করতে বা স্পেশাল বোনাস পেতে অবশ্যই নিচে দেওয়া যেকোনো একটি প্রোমো কোড দিয়ে নতুন অ্যাকাউন্ট খুলুন:
- 1xBet Promo Code: BLACK696
- Melbet Promo Code: BLACK220
- 1Win Promo Code: BLACK110"
৩. হ্যাক ফাইল রুল (Most Important): যদি ইউজার কোনো ধরনের হ্যাক (Hack), হ্যাক ফাইল, এভিয়েটর হ্যাক (Aviator hack), প্রেডিক্টর, গেম হ্যাক বা এই ধরনের কিছু চায়, তবে তুমি সরাসরি কোনো ফাইল, কোড বা ট্রিকস দেবে না। 
তুমি অত্যন্ত বিনয়ের সাথে বলবে: "হ্যাক ফাইল বা ভিআইপি সিগন্যাল পেতে হলে আপনাকে আগে আমাদের প্রোমো কোড ব্যবহার করে নতুন অ্যাকাউন্ট খুলতে হবে। এরপর ফাইলটি নেওয়ার জন্য আমাদের টেলিগ্রাম চ্যানেল https://t.me/black_Dogs10 এ জয়েন করুন এবং সরাসরি অ্যাডমিন @SUNNY_BRO1 এর সাথে যোগাযোগ করুন। তিনি আপনাকে হ্যাক ফাইলটি দিয়ে দেবেন।"
"""

# Gemini Model Setup
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ================= ডাটাবেস সেটআপ =================
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)')
conn.commit()

def add_user(user_id):
    try:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

# ================= বটের কমান্ড ও বাটন =================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    add_user(message.chat.id)
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🎁 অফার ও প্রোমো কোড", callback_data="promo")
    btn2 = InlineKeyboardButton("📢 আমাদের চ্যানেল", url="https://t.me/black_Dogs10")
    btn3 = InlineKeyboardButton("👤 অ্যাডমিন সাপোর্ট", url="https://t.me/SUNNY_BRO1")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.send_message(message.chat.id, "হ্যালো! আমি আপনার এআই বন্ধু। আপনার যেকোনো প্রশ্নের উত্তর দিতে আমি প্রস্তুত। আমি কীভাবে আপনাকে সাহায্য করতে পারি?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "promo":
        text = ("*আমাদের স্পেশাল প্রোমো কোড সমূহ:*\n\n"
                "🔴 *1xBet:* `BLACK696`\n"
                "🟢 *Melbet:* `BLACK220`\n"
                "🔵 *1Win:* `BLACK110`\n\n"
                "এগুলো ব্যবহার করে অ্যাকাউন্ট করলেই পাবেন বিশাল বোনাস!")
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# ================= অ্যাডমিন প্যানেল =================
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.chat.id == ADMIN_ID:
        text = message.text.replace('/broadcast ', '')
        if text:
            cursor.execute('SELECT user_id FROM users')
            users = cursor.fetchall()
            success = 0
            for user in users:
                try:
                    bot.send_message(user[0], text)
                    success += 1
                except:
                    pass
            bot.send_message(ADMIN_ID, f"✅ ব্রডকাস্ট সফল! {success} জনকে মেসেজ পাঠানো হয়েছে।")
        else:
            bot.send_message(ADMIN_ID, "⚠️ নিয়ম: /broadcast আপনার_মেসেজ")

@bot.message_handler(commands=['send'])
def send_specific_message(message):
    if message.chat.id == ADMIN_ID:
        try:
            parts = message.text.split(' ', 2)
            target_id = int(parts[1])
            msg_text = parts[2]
            bot.send_message(target_id, msg_text)
            bot.send_message(ADMIN_ID, f"✅ মেসেজ পাঠানো হয়েছে {target_id} কে।")
        except:
            bot.send_message(ADMIN_ID, "⚠️ নিয়ম: /send ইউজার_আইডি আপনার_মেসেজ")

# ================= এআই চ্যাট এবং মনিটরিং =================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.chat.id
    user_text = message.text
    user_name = message.from_user.first_name
    
    # অ্যাডমিনকে নোটিফিকেশন পাঠানো
    if user_id != ADMIN_ID:
        admin_alert = f"📩 *Message from {user_name}* (`{user_id}`):\n{user_text}"
        try:
            bot.send_message(ADMIN_ID, admin_alert, parse_mode="Markdown")
        except:
            pass # অ্যাডমিন ব্লক করে রাখলে এরর এড়াতে

    bot.send_chat_action(user_id, 'typing')
    try:
        response = model.generate_content(user_text)
        ai_reply = response.text
        bot.send_message(user_id, ai_reply)
    except Exception as e:
        bot.send_message(user_id, "সার্ভারে একটু সমস্যা হচ্ছে। দয়া করে আবার মেসেজ দিন।")

print("বট চালু হয়েছে...")
bot.infinity_polling()
