import os
import telebot
from datetime import datetime
import time
import threading
from flask import Flask

# --- TRICK TO KEEP RENDER ONLINE 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running online 24/7!"

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT LOGIC ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 🔴 CRUCIAL: Put your exact negative group ID number inside the single quotes below!
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
        "📖 Available Commands:\n"
        "• /countdown - Get the live dynamic exam timer\n"
        "• /physics - View Class 11 & 12 Physics syllabus\n"
        "• /chemistry - View Class 11 & 12 Chemistry syllabus\n"
        "• /maths - View Class 11 & 12 Mathematics syllabus\n\n"
        "Stay consistent. Every day counts. 🔥"
    )
    bot.send_message(message.chat.id, welcome_text)

# --- STABLE HANDLER FOR PLAIN GROUP COUNTDOWN COMMAND ---
@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith('/countdown'))
def send_countdown(message):
    response = get_countdown_text()
    bot.send_message(message.chat.id, response)

# --- NEW: PHYSICS COMMAND ---
@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith('/physics'))
def send_physics(message):
    physics_text = (
        "📚 **Syllabus for JEE Physics (Mains + Advanced)** 📚\n\n"
        "📌 **Class 11:**\n"
        "• Physical World & Measurement\n"
        "• Kinematics & Laws of Motion\n"
        "• Work, Energy & Power\n"
        "• System of Particles & Rigid Body (Rotation)\n"
        "• Gravitation & Bulk Matter Properties\n"
        "• Thermodynamics & Kinetic Theory\n"
        "• Oscillations & Waves (SHM)\n\n"
        "📌 **Class 12:**\n"
        "• Electrostatics & Current Electricity\n"
        "• Magnetic Effects of Current & Magnetism\n"
        "• EMI & Alternating Currents (AC)\n"
        "• Electromagnetic Waves\n"
        "• Optics (Ray & Wave)\n"
        "• Dual Nature of Matter\n"
        "• Atoms & Nuclei (Modern Physics)\n"
        "• Electronic Devices (Semiconductors)"
    )
    bot.send_message(message.chat.id, physics_text)

# --- NEW: CHEMISTRY COMMAND ---
@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith('/chemistry'))
def send_chemistry(message):
    chemistry_text = (
        "📚 **Syllabus for JEE Chemistry (Mains + Advanced)** 📚\n\n"
        "📌 **Class 11:**\n"
        "• Some Basic Concepts (Mole Concept)\n"
        "• Structure of Atom\n"
        "• Classification of Elements (Periodic Table)\n"
        "• Chemical Bonding & Molecular Structure\n"
        "• Chemical Thermodynamics\n"
        "• Equilibrium (Chemical & Ionic)\n"
        "• Redox Reactions\n"
        "• Organic Chemistry: Basic Principles & Techniques (GOC)\n"
        "• Hydrocarbons\n\n"
        "📌 **Class 12:**\n"
        "• Solutions\n"
        "• Electrochemistry\n"
        "• Chemical Kinetics\n"
        "• d & f Block Elements\n"
        "• Coordination Compounds\n"
        "• Haloalkanes & Haloarenes\n"
        "• Alcohols, Phenols & Ethers\n"
        "• Aldehydes, Ketones & Carboxylic Acids\n"
        "• Amines (Nitrogen Compounds)\n"
        "• Biomolecules"
    )
    bot.send_message(message.chat.id, chemistry_text)

# --- NEW: MATHEMATICS COMMAND ---
@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith('/maths'))
def send_maths(message):
    maths_text = (
        "📚 **Syllabus for JEE Mathematics (Mains + Advanced)** 📚\n\n"
        "📌 **Class 11:**\n"
        "• Sets, Relations & Functions\n"
        "• Trigonometric Functions\n"
        "• Complex Numbers & Quadratic Equations\n"
        "• Permutations & Combinations (P&C)\n"
        "• Binomial Theorem\n"
        "• Sequences & Series (AP/GP)\n"
        "• Straight Lines & Conic Sections\n"
        "• Limits & Derivatives\n"
        "• Statistics & Probability\n\n"
        "📌 **Class 12:**\n"
        "• Relations & Functions & Inverse Trig (ITF)\n"
        "• Matrices & Determinants\n"
        "• Continuity, Differentiability & AOD\n"
        "• Integrals (Definite & Indefinite)\n"
        "• Applications of Integrals (Area)\n"
        "• Differential Equations\n"
        "• Vector Algebra\n"
        "• Three Dimensional Geometry (3D)\n"
        "• Probability"
    )
    bot.send_message(message.chat.id, maths_text)

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
    t1 = threading.Thread(target=run_dummy_server, daemon=True)
    t1.start()
    
    t2 = threading.Thread(target=automatic_scheduler, daemon=True)
    t2.start()
    
    bot.infinity_polling()
