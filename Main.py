import os
import telebot
from datetime import datetime

# Safe automatic token pickup from Render settings
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Your daily dose of motivation and reality check for JEE Main 2028.\n\n"
        "Every morning at 7:00 AM IST, this bot reminds you exactly how many days "
        "and weeks are left for the estimated JEE Main January 2028 exam.\n\n"
        "📅 Daily reminder — every day at 7:00 AM IST\n"
        "📅 Weekly check-in — every Monday at 7:00 AM IST\n\n"
        "Use /countdown anytime to get the live countdown instantly.\n\n"
        "Stay consistent. Every day counts. 🔥"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['countdown'])
def send_countdown(message):
    today = datetime.now()
    target = datetime(2028, 1, 20) # Estimated Exam Target Date: 20th January 2028
    
    difference = target - today
    days_left = difference.days
    weeks_left = days_left // 7
    extra_days = days_left % 7
    
    today_str = today.strftime("%dth %B, %Y")
    
    response = (
        "⏳ JEE Main 2028 Countdown\n\n"
        f"📅 Today: {today_str}\n"
        "🎯 Estimated Target: 20th January 2028\n"
        f"⏳ Days Left: {days_left}\n"
        f"📅 Weeks Left: {weeks_left} weeks + {extra_days} days\n\n"
        "Keep going. 🔥"
    )
    bot.reply_to(message, response)

bot.infinity_polling()
