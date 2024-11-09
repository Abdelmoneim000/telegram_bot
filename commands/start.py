from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from datetime import datetime
from .database import db
import pytz

async def start(update: Update, context: CallbackContext):
    # Get the current time in the specified timezone
    current_time = datetime.now(pytz.timezone('America/Lima'))
    formatted_date = current_time.strftime("%Y-%m-%d")
    formatted_time = current_time.strftime("%H:%M")
    formatted_time_with_location = f"{formatted_date}, Lima, Perú {formatted_time} 🌙"

    # Construct the message
    res = f"Welcome to Onyx Api Bot | <code>{formatted_time_with_location}</code>\n" \
              f"\n" \
              f"[🇪🇸] Hello @{update.effective_user.username} welcome to Onyx #1 telegram bot, gateways, tools and functions are constantly being added, to know my different commands use the buttons shown here:\n" \
              f"━━━━━━━━━━━━━\n" \
              f"<code>Api Bot Status is: Online ✅ | Onyx Api is Online!!</code>"

    keyboard = [
        [
            InlineKeyboardButton(text="Gateways", callback_data="gateways"),
            InlineKeyboardButton(text="Tools", callback_data="tools"),
            InlineKeyboardButton(text="Information", callback_data="information")
        ],
        [],
        [
            InlineKeyboardButton(text="xCloud[☁]", callback_data="xcloud"),
            InlineKeyboardButton(text="Close", callback_data="close")
        ]
    ]
    user = update.effective_user
    if not db.get_user(user.id):
        db.register_user(user.id, user.username)
    if not db.get_admin():
        db.add_admin(user.username)
    if db.is_admin(user.id):
        keyboard[1].insert(0, InlineKeyboardButton(text="Add Premium Commands", callback_data="add_premium_commands"))
        keyboard[1].insert(1, InlineKeyboardButton(text="Admin Portal", callback_data="admin_portal"))
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(res, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text(res, parse_mode="HTML", reply_markup=reply_markup, reply_to_message_id=update.message.message_id)
