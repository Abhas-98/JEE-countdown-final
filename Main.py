import os
import telebot
from datetime import datetime
import time
import threading
from flask import Flask

# --- TRICK TO KEEP RENDER ONLINE 24/7 ---
# This creates a dummy webpage so Render never hits a port timeout crash
app = Flask('')

@app.route('/')
def home():
    return "Bot is running online 24/7!"

def run_dummy_server():
    # Safely fetches port from Render or uses 8080 as backup
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT LOGIC ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 🔴 CRUCIAL: Put your exact negative group ID inside the single quotes below!
GROUP_CHAT_ID = '-1003636395458'

def get_countdown_text():
    today = datetime.now()
    target = datetime(2028, 1, 20) # Target Exam Date: 20th January 2028
    
    difference = target - today
    days_left = difference.days
    weeks_left = days_left // 7
    extra_days = days_left % 7
    
    today_str = today.strftime("%dth %B, %Y")
    
    return (
        "⏳ JEE Main 2028 Countdown\n\n"
        f"📅 Today: {today_str}\n"
        "🎯 Estimated Target: 20th January 2028\n"
        f"⏳ Days Left: {days_left}\n"
        f"📅 Weeks Left: {weeks_left} weeks + {extra_days} days\n\n"
        "Keep going. 🔥"
    )

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Your daily dose of motivation and reality check for JEE Main 2028.\n\n"
        "Use /countdown anytime to get the live countdown instantly.\n\n"
        "Stay consistent. Every day counts. 🔥"
    )
    bot.send_message(message.chat.id, welcome_text)

# --- 100% FIXED STABLE HANDLER FOR PLAIN GROUP COMMANDS ---
@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith('/countdown'))
def send_countdown(message):
    response = get_countdown_text()
    bot.send_message(message.chat.id, response)

# --- AUTOMATIC MORNING SCHEDULER SYSTEM ---
def automatic_scheduler():
    while True:
        # 7:00 AM IST is exactly 1:30 AM UTC time on Render
        current_time = datetime.utcnow()
        
        if current_time.hour == 1 and current_time.minute == 30:
            if GROUP_CHAT_ID != '-1001234567890':
                try:
                    response = get_countdown_text()
                    bot.send_message(chat_id=int(GROUP_CHAT_ID), text=f"📢 DAILY MORNING ALERTS\n\n{response}")
                except Exception as e:
                    print("Error sending automatic message:", e)
            time.sleep(60)
        time.sleep(10)

# --- START EVERYTHING SAFELY ---
if __name__ == "__main__":
    # 1. Start the web server in the background for Render
    t1 = threading.Thread(target=run_dummy_server, daemon=True)
    t1.start()
    
    # 2. Start the 7:00 AM clock tracker in the background
    t2 = threading.Thread(target=automatic_scheduler, daemon=True)
    t2.start()
    
    # 3. Start the Telegram Bot listener live
    bot.infinity_polling()
