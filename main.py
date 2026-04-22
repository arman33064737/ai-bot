import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
import threading
import urllib.request
from io import BytesIO

# ================= কনফিগারেশন =================
BOT_TOKEN = '8620762862:AAESIXZOh7Hi8pRNezOnzdeoxre8ejIfOIo'
CHANNEL_ID = '@aviator_signal3467' 
BUTTON_LINK = 'https://1wezue.com/casino' 
PROMO_CODE = 'BLACK110' 

# প্রোমোশনাল ছবির লিংক
PROMO_IMAGE_URL = 'https://i.ibb.co.com/yMwPHDC/file-00000000c728720b9c651adba13f4851.png'
# ===============================================

bot = telebot.TeleBot(BOT_TOKEN)

# গ্লোবাল ভেরিয়েবল
active_image_id = None
is_running = False

# সিগন্যাল খেলার বাটন তৈরি
def get_inline_button():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Play Here 🚀", url=BUTTON_LINK)
    markup.add(btn)
    return markup

# প্রোমোশনাল "Create Account" বাটন তৈরি
def get_promo_button():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Create Account", url=BUTTON_LINK)
    markup.add(btn)
    return markup

# প্রোমোশনাল মেসেজ পাঠানোর ফাংশন
def send_promo_message():
    promo_text = f"""
<b>Create an Account on 1WIN</b>

Use my promo code - <b>{PROMO_CODE}</b>
Get 500% Bonus 💪🔥

After creating your account, send your UID to @SUNNY_BRO1

⚠️ Don't forget to use promo: <b>{PROMO_CODE}</b>
"""
    try:
        req = urllib.request.Request(PROMO_IMAGE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_bytes = BytesIO(response.read())
            
        bot.send_photo(
            CHANNEL_ID, 
            photo=img_bytes, 
            caption=promo_text, 
            parse_mode='HTML', 
            reply_markup=get_promo_button()
        )
        print("✅ Promo message sent successfully!")
        
    except Exception as e:
        print(f"⚠️ Failed to send image: {e}")
        print("✅ Sending message without image...")
        try:
            bot.send_message(
                CHANNEL_ID, 
                text=promo_text, 
                parse_mode='HTML', 
                reply_markup=get_promo_button()
            )
        except Exception as ex:
            print(f"❌ Failed to send text message: {ex}")

# AI-স্টাইল অটোমেটিক সিগন্যাল লুপ
def auto_signal_loop():
    global is_running, active_image_id
    
    signal_count = 0
    target_signals_for_promo = 2 
    
    while is_running:
        try:
            if not active_image_id:
                time.sleep(2)
                continue

            multiplier = f"{random.uniform(1.20, 3.50):.2f}"
            
            caption_text = f"""
🎯 <b>Entry Confirmed</b> 🎯

🌐 Site: 👉 <a href="{BUTTON_LINK}">Click Here To Play</a> 👈
🚪 Exit at: <b>{multiplier}x</b>

USE PROMO: <b>{PROMO_CODE}</b> and get 500% Bonus
"""
            sent_msg = bot.send_photo(
                CHANNEL_ID, 
                photo=active_image_id, 
                caption=caption_text, 
                parse_mode='HTML', 
                reply_markup=get_inline_button()
            )
            print("➡️ Signal sent.")
            
            time.sleep(20)
            
            result = random.choices(['WIN', 'LOSS'], weights=[80, 20])[0]
            if result == 'WIN':
                bot.send_message(CHANNEL_ID, "✅ <b>WIN</b> 💸", parse_mode='HTML', reply_to_message_id=sent_msg.message_id)
                bot.send_message(CHANNEL_ID, "🤑") 
            else:
                bot.send_message(CHANNEL_ID, "❌ <b>LOSS</b> 💔", parse_mode='HTML', reply_to_message_id=sent_msg.message_id)
            
            signal_count += 1
            time.sleep(2)

            if signal_count >= target_signals_for_promo:
                send_promo_message()
                signal_count = 0 
                target_signals_for_promo = random.randint(5, 7) 
                time.sleep(3) 
            
            checking_msg = bot.send_message(CHANNEL_ID, "⏳ <b>Checking new signal...</b> 👁", parse_mode='HTML')
            time.sleep(5)
            
            try:
                bot.delete_message(CHANNEL_ID, checking_msg.message_id)
            except Exception:
                pass
                
        except Exception as e:
            print(f"❌ Error in loop: {e}")
            time.sleep(5)


# ================== নতুন এডমিন এবং কাস্টম পোস্ট সিস্টেম ==================

@bot.message_handler(commands=['admin', 'start', 'help'])
def admin_panel(message):
    help_text = """
👑 <b>Admin Control Panel</b> 👑

<b>Auto Signal Commands:</b>
🖼 <b>Send any Photo:</b> Starts the auto-signal loop.
🛑 <code>/stop</code>: Stops the auto-signals.

<b>Custom Channel Posting (Menu Builder Style):</b>
If you want to post a custom designed message to your channel (with Bold, Links, Colors, etc.):
1️⃣ Type and design your message in the bot.
2️⃣ Send it to the bot.
3️⃣ Reply to your own message with <code>/send</code>
✅ The bot will post it exactly as you designed it to the channel!
"""
    bot.reply_to(message, help_text, parse_mode='HTML')

# কাস্টম পোস্ট চ্যানেলে পাঠানোর কমান্ড
@bot.message_handler(commands=['send'])
def send_custom_post(message):
    if message.reply_to_message:
        try:
            # Menu Builder এর মত হুবহু মেসেজ চ্যানেলে ফরোয়ার্ড/কপি করবে (সব ডিজাইন সহ)
            bot.copy_message(CHANNEL_ID, message.chat.id, message.reply_to_message.message_id)
            bot.reply_to(message, "✅ <b>Message successfully posted to the channel!</b>", parse_mode='HTML')
        except Exception as e:
            bot.reply_to(message, f"❌ <b>Error posting message:</b>\n{e}", parse_mode='HTML')
    else:
        bot.reply_to(message, "⚠️ <b>Please reply to the message you want to post to the channel with</b> <code>/send</code>", parse_mode='HTML')

# ======================================================================


# ছবি রিসিভ করার হ্যান্ডলার
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global active_image_id, is_running
    
    active_image_id = message.photo[-1].file_id
    
    if not is_running:
        is_running = True
        threading.Thread(target=auto_signal_loop, daemon=True).start()
        bot.reply_to(message, "✅ <b>Image successfully set!</b>\n\nAutomatic signals have started.\n(For testing, promo will appear after 2 signals, then every 5-7 signals)", parse_mode='HTML')
    else:
        bot.reply_to(message, "✅ <b>New image updated!</b>\n\nThe next signal will use this new image.", parse_mode='HTML')

# বটকে থামানোর কমান্ড
@bot.message_handler(commands=['stop'])
def stop_loop(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 <b>Auto signals stopped!</b>\n\nSend a new photo to the bot to start again.", parse_mode='HTML')

# বট চালু রাখা 
if __name__ == '__main__':
    print("🚀 Bot started successfully! Send an image to the bot's inbox.")
    
    while True: 
        try:
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Connection issue or crash: {e}")
            print("🔄 Reconnecting in 5 seconds...")
            time.sleep(5)
